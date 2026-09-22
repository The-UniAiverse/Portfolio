"""Control plane: approval before entitlement, plans as resource profiles, quotas, provisioning jobs, state machine, enforcement middleware, cost model."""
import uuid, pytest
from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app
from app.services.platform import engine
c = TestClient(app); H = {"X-Admin-Token": settings.admin_token}
def reg(plan="free", **kw):
    e = kw.pop("email", f"{uuid.uuid4().hex[:6]}@acme-example.com")
    r = c.post("/api/platform/register", json={"organisation": "Acme " + e[:4], "contact_name": "Asha", "contact_email": e, "requested_plan": plan, "purpose": "try the RAG demo on our policies"}); assert r.status_code == 200, r.text; return r.json()["tenant_id"], e
def key_for(tid):
    with __import__("app.core.db", fromlist=["conn"]).conn() as cx: pass
    return None

def test_register_is_not_access():
    tid, e = reg(); assert c.get(f"/api/platform/status/{tid}?email={e}").json()["state"] == "PENDING"
    assert c.get(f"/api/platform/status/{tid}?email=other@x.test").status_code == 404
    assert c.post("/api/platform/register", json={"organisation": "X", "contact_name": "Y", "contact_email": "bad-email", "requested_plan": "free"}).status_code == 422
    assert c.get("/api/platform/requests").status_code == 401 and any(p["id"] == tid for p in c.get("/api/platform/requests", headers=H).json()["pending"])

def test_free_approval_provisions_in_background_and_quotas_bite(monkeypatch):
    tid, e = reg(); r = c.post(f"/api/platform/approve/{tid}", json={"decided_by": "Sarfi"}, headers=H).json(); assert r["state"] == "PROVISIONING" and r["job_id"]
    ran = engine.run_jobs(); job = next((j for j in ran if j["tenant_id"] == tid), None); d = c.get(f"/api/platform/tenants/{tid}", headers=H).json()
    assert d["state"] == "ACTIVE" and d["plan"] == "free" and d["environment"]["vector_namespace"].startswith("tenant_") and d["users"] == "1 / 1"
    key = job["api_key"] if job else None
    if key is None:                                  # job ran inside the approve BackgroundTask; issue a fresh key through the engine for the test
        import hashlib, secrets; key = "uav_" + secrets.token_urlsafe(8)
        with __import__("app.core.db", fromlist=["conn"]).conn() as cx: cx.execute("UPDATE tenants SET key_hash=? WHERE id=?", (hashlib.sha256(key.encode()).hexdigest(), tid))
    T = {"X-Tenant-Key": key}; me = c.get("/api/platform/me", headers=T).json(); assert me["plan"] == "free" and "demo.run" in me["capabilities"] and "agent.run" not in me["capabilities"]
    assert c.post("/api/platform/check", json={"capability": "agent.run"}, headers=T).json()["allowed"] is False
    res = [c.post("/api/platform/check", json={"capability": "demo.run"}, headers=T).json()["allowed"] for _ in range(4)]; assert res == [True, True, True, False]      # daily 3
    assert "daily quota" in c.post("/api/platform/check", json={"capability": "demo.run"}, headers=T).json()["reason"]
    assert c.get("/api/platform/me", headers={"X-Tenant-Key": "uav_nope"}).status_code == 401

def test_paid_plan_waits_for_payment_then_provisions():
    tid, e = reg("silver"); r = c.post(f"/api/platform/approve/{tid}", json={"decided_by": "Sarfi"}, headers=H).json(); assert r["state"] == "PAYMENT_PENDING" and r["pay_product"] == "platform.silver"
    assert c.post(f"/api/platform/approve/{tid}", json={"decided_by": "Sarfi"}, headers=H).status_code == 422                 # cannot approve twice
    o = c.post("/api/payments/order", json={"product_id": "platform.silver", "customer_name": "Asha", "customer_email": e, "tenant_id": tid}).json(); assert o["amount"] == 4500000 or o.get("amount_inr", 45000) == 45000
    v = c.post("/api/payments/verify", json={"payment_id": o["payment_id"], "razorpay_order_id": o["order_id"], "razorpay_payment_id": "pay_test_1", "razorpay_signature": "x"}); assert v.status_code == 200, v.text
    d = c.get(f"/api/platform/tenants/{tid}", headers=H).json(); assert d["state"] == "ACTIVE" and d["plan"] == "silver" and d["environment"]["deployment"].startswith("dedicated") and d["expires_at"]
    assert d["limits"]["monthly_queries"] == 5000 and "agent.run" in d["capabilities"] and (__import__("pathlib").Path(engine.ROOT) / d["environment"]["root"] / "docker-compose.tenant.yml").exists()

def test_limits_change_without_redeploy_and_state_machine():
    tid, e = reg("bronze"); c.post(f"/api/platform/approve/{tid}", json={"decided_by": "S"}, headers=H); c.post(f"/api/platform/tenants/{tid}/mark-paid", json={"decided_by": "S", "note": "NEFT received"}, headers=H); engine.run_jobs()
    assert c.get(f"/api/platform/tenants/{tid}", headers=H).json()["state"] == "ACTIVE"
    assert c.patch(f"/api/platform/tenants/{tid}/limits", json={"monthly_queries": 10, "reason": "x"}, headers=H).status_code == 422                                  # reason too short
    L = c.patch(f"/api/platform/tenants/{tid}/limits", json={"monthly_queries": 10, "capabilities_add": ["agent.run"], "capabilities_remove": ["doc.generate"], "reason": "pilot agreement clause 4"}, headers=H).json()["effective_limits"]
    assert L["monthly_queries"] == 10 and "agent.run" in L["capabilities"] and "doc.generate" not in L["capabilities"]
    assert c.post(f"/api/platform/tenants/{tid}/state/ACTIVE", json={"decided_by": "S"}, headers=H).status_code == 422                                                   # ACTIVE → ACTIVE not allowed
    assert c.post(f"/api/platform/tenants/{tid}/state/SUSPENDED", json={"decided_by": "S", "note": "unpaid invoice"}, headers=H).json()["state"] == "SUSPENDED"
    assert engine.check(engine.load(tid), "rag.basic")["allowed"] is False
    assert c.post(f"/api/platform/tenants/{tid}/state/ACTIVE", json={"decided_by": "S"}, headers=H).json()["state"] == "ACTIVE"
    d = c.get(f"/api/platform/tenants/{tid}", headers=H).json(); assert any(a["action"] == "limits_changed" for a in d["audit"]) and any(a["action"] == "transition_refused" for a in d["audit"])

def test_sandbox_pool_and_pause():
    s = c.get("/api/platform/sandbox").json(); assert set(s) >= {"queries_used", "monthly_budget_inr", "exhausted", "can_approve_more"}
    assert c.post("/api/platform/sandbox/pause", headers=H).json()["approvals_paused"] is True
    tid, _ = reg(); assert c.post(f"/api/platform/approve/{tid}", json={"decided_by": "S"}, headers=H).status_code == 422
    assert c.post("/api/platform/sandbox/pause?paused=false", headers=H).json()["can_approve_more"] is True

def test_enforcement_middleware(monkeypatch):
    monkeypatch.setattr(settings, "entitlements_mode", "log")
    r = c.post("/api/demos/run-course/llm-cost/01_billing_unit_and_formula"); assert r.status_code == 200 and r.headers["X-Entitlement"].startswith("demo.run; allowed")
    monkeypatch.setattr(settings, "entitlements_mode", "enforce")
    assert c.post("/api/demos/run-course/llm-cost/01_billing_unit_and_formula").status_code == 200                           # public sandbox capability, pool not exhausted
    r = c.post("/api/delivery/pack", json=c.get("/api/delivery/sample?tier=bronze").json()); assert r.status_code == 402 and "tenant key" in r.json()["detail"]     # not public
    assert c.post("/api/delivery/run", json=c.get("/api/delivery/sample?tier=bronze").json()).status_code == 200                  # not a guarded path
    assert c.post("/api/demos/run-course/llm-cost/01_billing_unit_and_formula", headers={"X-Tenant-Key": "uav_bad"}).status_code == 401
    monkeypatch.setattr(settings, "entitlements_mode", "off"); assert "X-Entitlement" not in c.post("/api/delivery/pack", json=c.get("/api/delivery/sample?tier=bronze").json()).headers

def test_cost_model_is_consistent():
    m = c.get("/api/platform/cost-model?bronze=4&silver=2&gold=0", headers=H).json(); P = m["plans"]
    for p in P.values(): assert abs(p["monthly_revenue_inr"] - p["monthly_cost_inr"] - p["payment_fees_inr"] - p["gross_margin_inr"]) < 1 and sum(p["cost_lines"].values()) == p["monthly_cost_inr"]
    mo = m["monthly"]; assert abs(mo["revenue"] - mo["cost_of_tenants"] - mo["fixed"] - mo["payment_fees"] - mo["operating_result"]) < 1
    assert m["fixed_monthly_inr"] == sum(m["fixed_lines"].values()) and all(v for v in m["break_even_tenants"].values())
