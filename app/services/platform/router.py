"""Control plane API. Public: plans, register, entitlement check (with X-Tenant-Key). Admin (X-Admin-Token): requests, approve, tenants, limits, provisioning, sandbox, cost model."""
from __future__ import annotations
import json
from fastapi import APIRouter, BackgroundTasks, Header, HTTPException
from app.core import db
from app.core.config import settings
from . import engine
from .schemas import Register, Approve, Limits, Check

router = APIRouter()
def _admin(token):
    if not settings.admin_token or token != settings.admin_token: raise HTTPException(401, "admin token required")
def _tenant(key):
    if not key: return None
    t = engine.by_key(key)
    if not t: raise HTTPException(401, "unknown tenant key")
    return t

@router.get("/plans")
def plans():
    """Public price page data: every plan as a resource profile. Website reads this — never hard-code limits in the UI."""
    P = engine.content("plans"); return {"currency": P["currency"], "free_sandbox": P["free_sandbox"], "plans": P["plans"], "status": "PLACEHOLDER commercial values until confirmed", "version": P["version"]}
@router.get("/capabilities")
def capabilities(): return engine.content("capabilities")["capabilities"]
@router.post("/register")
def register(r: Register):
    try: return engine.register(r.organisation, r.contact_name, r.contact_email, r.requested_plan, r.purpose)
    except ValueError as e: raise HTTPException(422, str(e))
@router.get("/me")
def me(x_tenant_key: str | None = Header(None)):
    """What am I allowed to do, and how much is left? The website calls this after sign-in."""
    t = _tenant(x_tenant_key)
    if not t: raise HTTPException(401, "X-Tenant-Key required")
    lim = engine.effective_limits(t); us = engine.usage(t["id"]); return {"tenant_id": t["id"], "organisation": t["name"], "plan": t["plan"], "state": t["state"], "capabilities": lim["capabilities"], "limits": {k: lim.get(k) for k in ("users", "monthly_queries", "daily_queries", "max_context_tokens", "storage_gb", "knowledge_bases", "agent_max_tool_calls")}, "usage": us, "expires_at": t["expires_at"]}
@router.post("/check")
def check(c: Check, x_tenant_key: str | None = Header(None)):
    """The entitlement engine: may this caller do this capability now? Records usage. Anonymous callers get the public sandbox rules."""
    return engine.check(_tenant(x_tenant_key), c.capability, c.units)
@router.get("/sandbox")
def sandbox(): return engine.sandbox_status()
@router.get("/status/{tenant_id}")
def status(tenant_id: str, email: str):
    """A requester checks their own request (needs the email they registered with)."""
    try: t = engine.load(tenant_id)
    except KeyError: raise HTTPException(404, "not found")
    if t["contact_email"].lower() != email.lower(): raise HTTPException(404, "not found")
    return {"tenant_id": t["id"], "state": t["state"], "plan": t["plan"] or t["requested_plan"], "next": {"PENDING": "waiting for admin approval", "APPROVED": "approved", "PAYMENT_PENDING": f"pay at {settings.public_url}/pay?product=platform.{t['plan']}&tenant={t['id']}", "PROVISIONING": "environment being created (minutes)", "ACTIVE": "active — your admin has the API key", "SUSPENDED": "suspended — contact support", "QUOTA_EXCEEDED": "monthly quota reached — resets next month or upgrade", "EXPIRED": "renew to reactivate", "REJECTED": "not approved", "CANCELLED": "cancelled"}.get(t["state"], "")}

# ── admin ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
@router.get("/requests")
def requests(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    sb = engine.sandbox_status()
    with db.conn() as c: pend = [dict(r) for r in c.execute("SELECT id, name, contact_name, contact_email, requested_plan, purpose, created_at FROM tenants WHERE state='PENDING' ORDER BY created_at").fetchall()]
    return {"sandbox": sb, "pending": pend}
@router.post("/approve/{tenant_id}")
def approve(tenant_id: str, a: Approve, bg: BackgroundTasks, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    try: r = engine.approve(tenant_id, a.plan, a.decided_by, a.note)
    except KeyError: raise HTTPException(404, "tenant not found")
    except ValueError as e: raise HTTPException(422, str(e))
    if r.get("job_id"): bg.add_task(engine.run_jobs)
    return r
@router.post("/reject/{tenant_id}")
def reject(tenant_id: str, a: Approve, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    try: return {"state": engine.reject(tenant_id, a.decided_by, a.note)["state"]}
    except KeyError: raise HTTPException(404, "tenant not found")
    except ValueError as e: raise HTTPException(422, str(e))
@router.get("/tenants")
def tenants(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    with db.conn() as c: rows = [dict(r) for r in c.execute("SELECT id, name, contact_email, plan, state, requested_plan, expires_at, updated_at FROM tenants WHERE state!='PENDING' ORDER BY updated_at DESC").fetchall()]
    for r in rows: u = engine.usage(r["id"]); lim = engine.effective_limits(r | {"limits": engine.load(r["id"])["limits"]}); r["queries"] = f"{u['units']} / {lim.get('monthly_queries')}"; r["spend_inr"] = u["cost_inr"]
    return rows
@router.get("/tenants/{tenant_id}")
def tenant(tenant_id: str, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    try: return engine.dashboard(tenant_id)
    except KeyError: raise HTTPException(404, "tenant not found")
@router.patch("/tenants/{tenant_id}/limits")
def limits(tenant_id: str, l: Limits, x_admin_token: str | None = Header(None)):
    """Change any limit or capability for one tenant. Takes effect on the next request. No redeploy."""
    _admin(x_admin_token)
    try: return {"tenant_id": tenant_id, "effective_limits": engine.set_limits(tenant_id, l.model_dump(), l.by)}
    except KeyError: raise HTTPException(404, "tenant not found")
@router.post("/tenants/{tenant_id}/state/{to}")
def set_state(tenant_id: str, to: str, a: Approve, bg: BackgroundTasks, x_admin_token: str | None = Header(None)):
    """Manual transition (suspend, reactivate, cancel). Refused and audited when the state machine does not allow it."""
    _admin(x_admin_token)
    try: t = engine.transition(tenant_id, to.upper(), a.decided_by, a.note)
    except KeyError: raise HTTPException(404, "tenant not found")
    except ValueError as e: raise HTTPException(422, str(e))
    if to.upper() == "PROVISIONING": engine.enqueue(tenant_id); bg.add_task(engine.run_jobs)
    return {"tenant_id": tenant_id, "state": t["state"]}
@router.post("/tenants/{tenant_id}/mark-paid")
def mark_paid(tenant_id: str, a: Approve, bg: BackgroundTasks, x_admin_token: str | None = Header(None)):
    """Bank transfer arrived outside Razorpay: same path as a verified payment."""
    _admin(x_admin_token); t = engine.load(tenant_id); r = engine.on_payment(tenant_id, t["contact_email"], f"platform.{t['plan']}", a.decided_by)
    if not r: raise HTTPException(422, "tenant is not waiting for payment")
    bg.add_task(engine.run_jobs); return r
@router.post("/provision/run")
def provision_run(x_admin_token: str | None = Header(None)):
    """Worker tick: run queued provisioning jobs now (the worker container and cron call this too)."""
    _admin(x_admin_token); return {"ran": engine.run_jobs()}
@router.post("/scheduler/nightly")
def nightly(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token); return {"expired_or_reset": engine.expire_due(), "provisioned": engine.run_jobs()}
@router.post("/sandbox/pause")
def sandbox_pause(paused: bool = True, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    with db.conn() as c: c.execute("INSERT OR REPLACE INTO platform_settings (key, value) VALUES ('free_approvals_paused', ?)", ("1" if paused else "0",))
    engine.audit(None, "admin", "free_approvals_paused" if paused else "free_approvals_resumed"); return engine.sandbox_status()
@router.get("/cost-model")
def cost_model(bronze: int = 4, silver: int = 2, gold: int = 0, x_admin_token: str | None = Header(None)):
    """Unit economics per plan and the P&L for a tenant mix — the same numbers as docs/COST_ANALYSIS.md."""
    _admin(x_admin_token); return engine.cost_model({"bronze": bronze, "silver": silver, "gold": gold})
@router.get("/audit")
def audit(limit: int = 100, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    with db.conn() as c: return [dict(r) for r in c.execute("SELECT * FROM platform_audit ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]
