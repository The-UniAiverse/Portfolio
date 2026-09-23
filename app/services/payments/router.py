"""Payments — Razorpay (India: cards, UPI, netbanking, NEFT/RTGS/IMPS bank transfer).

Method rule (configurable, UPI_LIMIT_INR): UPI is offered only below the limit; above it, cards / netbanking / bank transfer.
Works in TEST MODE without keys (orders are simulated) so the site can be wired end-to-end before the merchant account is live.
Never handles card data — Razorpay Checkout collects it; we only create orders and verify signatures.
"""
from __future__ import annotations
import hashlib, hmac, json, uuid
import httpx, yaml
from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from app.core import db
from app.core.config import settings

router = APIRouter()
RZP = "https://api.razorpay.com/v1"

def _catalog() -> dict:
    """Every purchasable thing, built from pricing/tiers.yaml + quest tiers so prices live in one place."""
    tiers = yaml.safe_load((settings.pricing_dir / "tiers.yaml").read_text())
    quest = yaml.safe_load((settings.materials_dir.parent / "app/services/quest/quest_tiers.yaml").read_text())
    items = {}
    for tid, t in quest["tiers"].items():
        if t["price_inr"]:
            items[f"quest.{tid}"] = {"title": f"uniAI Quest — {t['title']} (monthly)", "amount_inr": t["price_inr"], "amount_usd": t["price_usd"], "grants_tier": tid, "kind": "subscription"}
    for sid, s in tiers["services"].items():
        for tid, t in s["tiers"].items():
            if t["price_usd"]:
                items[f"{sid}.{tid}"] = {"title": f"{s['title']} — {tid.title()}", "amount_usd": t["price_usd"], "amount_inr": round(t["price_usd"] * 84), "kind": "service"}
    if "platform" in settings.enabled_services:
        plans = yaml.safe_load((settings.materials_dir.parent / "app/services/platform/content/plans.yaml").read_text())["plans"]
        for pid, p in plans.items():
            if p.get("classroom"): continue
            items[f"platform.{pid}"] = {"title": f"{p['title']} — monthly platform fee", "amount_inr": p["platform_fee_inr"], "amount_usd": round(p["platform_fee_inr"] / 84), "kind": "subscription", "note": f"+ infrastructure ₹{p['infra_estimate_inr']:,}/month at cost + 15% (invoiced) · setup ₹{p['setup_fee_inr']:,} once"}
            items[f"platform.{pid}.setup"] = {"title": f"{p['title']} — one-time setup", "amount_inr": p["setup_fee_inr"], "amount_usd": round(p["setup_fee_inr"] / 84), "kind": "service"}
    return items

def method_rule(amount_inr: int) -> dict:
    below = amount_inr < settings.upi_limit_inr
    return {"upi": below, "card": True, "netbanking": True, "bank_transfer": not below,
            "note": (f"UPI available for amounts under ₹{settings.upi_limit_inr:,}." if below
                     else f"Amounts of ₹{settings.upi_limit_inr:,} and above: card, netbanking or NEFT/RTGS/IMPS bank transfer.")}

def _auth(): return (settings.razorpay_key_id, settings.razorpay_key_secret)
def _live() -> bool: return bool(settings.razorpay_key_id and settings.razorpay_key_secret)

@router.get("/catalog")
def catalog(): return {"upi_limit_inr": settings.upi_limit_inr, "items": _catalog(), "live": _live()}

class OrderRequest(BaseModel):
    product_id: str
    currency: str = Field("INR", pattern="^(INR|USD)$")
    customer_name: str
    customer_email: EmailStr
    user_id: str | None = Field(None, description="Quest user id to upgrade on payment")
    tenant_id: str | None = Field(None, description="Platform tenant (TEN-…) waiting for payment — provisioned on success")

@router.post("/order")
def create_order(o: OrderRequest):
    items = _catalog(); p = items.get(o.product_id)
    if not p: raise HTTPException(404, f"unknown product; see /api/payments/catalog")
    amount = p["amount_inr"] if o.currency == "INR" else p["amount_usd"]
    minor = amount * 100
    rule = method_rule(p["amount_inr"])
    pid = uuid.uuid4().hex[:12]
    if _live():
        r = httpx.post(f"{RZP}/orders", auth=_auth(), timeout=15, json={"amount": minor, "currency": o.currency, "receipt": pid,
                        "notes": {"product_id": o.product_id, "email": o.customer_email, "user_id": o.user_id or ""}})
        if r.status_code >= 300: raise HTTPException(502, f"gateway error: {r.text[:200]}")
        order = r.json(); order_id = order["id"]
    else:
        order_id = f"order_test_{pid}"
    with db.conn() as c:
        c.execute("INSERT INTO payments (id, provider, order_id, product_id, amount, currency, method_rule, status, customer, user_id, created_at, raw) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (pid, "razorpay", order_id, o.product_id, minor, o.currency, json.dumps(rule), "created",
                   json.dumps({"name": o.customer_name, "email": o.customer_email, "tenant_id": o.tenant_id}), o.user_id, db.now(), "{}"))
    hide = [] if rule["upi"] else [{"method": "upi"}]
    return {"payment_id": pid, "order_id": order_id, "amount": minor, "currency": o.currency, "title": p["title"],
            "key_id": settings.razorpay_key_id or "rzp_test_PLACEHOLDER", "test_mode": not _live(), "methods": rule,
            "checkout": {"key": settings.razorpay_key_id or "rzp_test_PLACEHOLDER", "amount": minor, "currency": o.currency, "name": "uniAIverse",
                         "description": p["title"], "order_id": order_id, "prefill": {"name": o.customer_name, "email": o.customer_email},
                         "config": {"display": {"hide": hide}}, "theme": {"color": "#0f766e"}}}

class Verify(BaseModel):
    payment_id: str; razorpay_order_id: str; razorpay_payment_id: str; razorpay_signature: str

def _grant(pid: str):
    with db.conn() as c:
        row = c.execute("SELECT * FROM payments WHERE id=?", (pid,)).fetchone()
    if not row: return
    p = _catalog().get(row["product_id"], {})
    if p.get("grants_tier") and row["user_id"]:
        db.set_tier(row["user_id"], p["grants_tier"], json.loads(row["customer"]).get("email"))
    if row["product_id"].startswith("platform.") and "platform" in settings.enabled_services:        # v2.6: paid plan → provisioning job (background)
        from app.services.platform import engine as _pe
        cust = json.loads(row["customer"]); _pe.on_payment(cust.get("tenant_id"), cust.get("email"), row["product_id"]); _pe.run_jobs()

@router.post("/verify")
def verify(v: Verify):
    """Called by the browser after Checkout succeeds. Verifies Razorpay's HMAC signature, marks paid, grants the tier."""
    if _live():
        expected = hmac.new(settings.razorpay_key_secret.encode(), f"{v.razorpay_order_id}|{v.razorpay_payment_id}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, v.razorpay_signature): raise HTTPException(400, "signature mismatch")
    elif not v.razorpay_order_id.startswith("order_test_"): raise HTTPException(400, "test mode: order id must be order_test_*")
    with db.conn() as c:
        c.execute("UPDATE payments SET status='paid', paid_at=?, raw=? WHERE id=? AND order_id=?", (db.now(), v.model_dump_json(), v.payment_id, v.razorpay_order_id))
    _grant(v.payment_id)
    return {"payment_id": v.payment_id, "status": "paid"}

@router.post("/webhook")
async def webhook(request: Request, x_razorpay_signature: str | None = Header(None)):
    """Razorpay → server. Source of truth for paid status (covers closed browsers, bank transfers)."""
    body = await request.body()
    if settings.razorpay_webhook_secret:
        expected = hmac.new(settings.razorpay_webhook_secret.encode(), body, hashlib.sha256).hexdigest()
        if not x_razorpay_signature or not hmac.compare_digest(expected, x_razorpay_signature): raise HTTPException(400, "bad signature")
    evt = json.loads(body or b"{}")
    if evt.get("event") in {"payment.captured", "order.paid", "virtual_account.credited"}:
        ent = evt.get("payload", {}); order_id = (ent.get("order", {}).get("entity", {}) or ent.get("payment", {}).get("entity", {})).get("id") or \
                   ent.get("payment", {}).get("entity", {}).get("order_id")
        with db.conn() as c:
            row = c.execute("SELECT id FROM payments WHERE order_id=?", (order_id,)).fetchone()
            if row: c.execute("UPDATE payments SET status='paid', paid_at=?, raw=? WHERE id=?", (db.now(), body.decode()[:4000], row["id"]))
        if row: _grant(row["id"])
    return {"ok": True}

class BankTransfer(BaseModel):
    product_id: str; customer_name: str; customer_email: EmailStr; user_id: str | None = None

@router.post("/bank-transfer")
def bank_transfer(b: BankTransfer):
    """NEFT / RTGS / IMPS: creates a Razorpay Smart Collect virtual account (live) or returns the configured bank details (test)."""
    p = _catalog().get(b.product_id)
    if not p: raise HTTPException(404, "unknown product")
    pid = uuid.uuid4().hex[:12]; amount = p["amount_inr"]
    if _live():
        r = httpx.post(f"{RZP}/virtual_accounts", auth=_auth(), timeout=15, json={"receivers": {"types": ["bank_account"]}, "description": p["title"],
                        "customer_id": None, "notes": {"product_id": b.product_id, "email": b.customer_email, "user_id": b.user_id or ""}, "close_by": None})
        if r.status_code >= 300: raise HTTPException(502, f"gateway error: {r.text[:200]}")
        va = r.json(); acct = va["receivers"][0]; order_id = va["id"]
        details = {"account_number": acct["account_number"], "ifsc": acct["ifsc"], "name": acct["name"], "bank": acct.get("bank_name")}
    else:
        order_id = f"va_test_{pid}"
        details = {"instructions": settings.bank_details or "Set BANK_TRANSFER_DETAILS in .env (account name, number, IFSC).", "reference": pid}
    with db.conn() as c:
        c.execute("INSERT INTO payments (id, provider, order_id, product_id, amount, currency, method_rule, status, customer, user_id, created_at, raw) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (pid, "razorpay_va" if _live() else "manual_bank", order_id, b.product_id, amount * 100, "INR", json.dumps({"bank_transfer": True}), "awaiting_transfer",
                   json.dumps({"name": b.customer_name, "email": b.customer_email}), b.user_id, db.now(), "{}"))
    return {"payment_id": pid, "amount_inr": amount, "title": p["title"], "transfer_to": details, "methods": ["NEFT", "RTGS", "IMPS"],
            "reference_to_quote": pid, "status": "awaiting_transfer", "test_mode": not _live()}

@router.get("/status/{payment_id}")
def status(payment_id: str):
    with db.conn() as c:
        row = c.execute("SELECT id, product_id, amount, currency, status, created_at, paid_at FROM payments WHERE id=?", (payment_id,)).fetchone()
    if not row: raise HTTPException(404, "not found")
    return dict(row)

@router.post("/admin/mark-paid/{payment_id}")
def admin_mark_paid(payment_id: str, x_admin_token: str | None = Header(None)):
    """Manual confirmation for bank transfers received outside Razorpay."""
    if not settings.admin_token or x_admin_token != settings.admin_token: raise HTTPException(401, "admin token required")
    with db.conn() as c:
        c.execute("UPDATE payments SET status='paid', paid_at=? WHERE id=?", (db.now(), payment_id))
    _grant(payment_id); return {"payment_id": payment_id, "status": "paid"}
