"""Integrated monitoring (v2.7): one call returns everything the operator needs — services, tenants, LLM/gateway metering, free pool,
audit, provisioning, denials, founder/mentor hours — so the console is one click, not a hunt across pages."""
from __future__ import annotations
import datetime as dt
from app.core import db
from app.core.config import settings
from app.core.registry import SERVICES
from . import engine

def _month(): return dt.date.today().strftime("%Y-%m")

def log_hours(person: str, day: str, activity: str, hours: float, note: str = "", tenant_id: str | None = None) -> dict:
    with db.conn() as c: c.execute("INSERT INTO founder_hours (person, day, activity, hours, note, tenant_id, created_at) VALUES (?,?,?,?,?,?,?)", (person, day, activity, hours, note, tenant_id, db.now()))
    return {"ok": True}

def hours(month: str | None = None) -> dict:
    m = month or _month(); rates = {"Sarfi": 2500, "Sachin": 1500, "Harsh": 500}
    with db.conn() as c:
        rows = [dict(r) for r in c.execute("SELECT * FROM founder_hours WHERE substr(day,1,7)=? ORDER BY day DESC, id DESC", (m,)).fetchall()]
        by_person = [dict(r) for r in c.execute("SELECT person, SUM(hours) hours FROM founder_hours WHERE substr(day,1,7)=? GROUP BY person", (m,)).fetchall()]
        by_activity = [dict(r) for r in c.execute("SELECT activity, SUM(hours) hours FROM founder_hours WHERE substr(day,1,7)=? GROUP BY activity ORDER BY hours DESC", (m,)).fetchall()]
    ceiling = {"Sarfi": 120, "Sachin": 60, "Harsh": 80}
    for p in by_person: p["ceiling"] = ceiling.get(p["person"]); p["over"] = bool(p["ceiling"]) and p["hours"] > p["ceiling"]; p["opportunity_cost_inr"] = round(p["hours"] * rates.get(p["person"], 1000))
    return {"month": m, "entries": rows[:200], "by_person": by_person, "by_activity": by_activity, "total_hours": round(sum(p["hours"] for p in by_person), 1)}

def overview() -> dict:
    m = _month(); today = dt.date.today().isoformat()
    with db.conn() as c:
        states = {r["state"]: r["n"] for r in c.execute("SELECT state, COUNT(*) n FROM tenants GROUP BY state").fetchall()}
        plans = {str(r["plan"]): r["n"] for r in c.execute("SELECT plan, COUNT(*) n FROM tenants WHERE state='ACTIVE' GROUP BY plan").fetchall()}
        llm = c.execute("SELECT SUM(status='ok') calls, SUM(status!='ok') denied, COALESCE(SUM(tokens_in),0) ti, COALESCE(SUM(tokens_out),0) tout, COALESCE(SUM(CASE WHEN status='ok' THEN cost_inr END),0) cost FROM llm_calls WHERE month=?", (m,)).fetchone()
        llm_today = c.execute("SELECT SUM(status='ok') calls, COALESCE(SUM(CASE WHEN status='ok' THEN cost_inr END),0) cost FROM llm_calls WHERE day=?", (today,)).fetchone()
        by_day = [dict(r) for r in c.execute("SELECT day, SUM(status='ok') calls, COALESCE(SUM(CASE WHEN status='ok' THEN cost_inr END),0) cost FROM llm_calls WHERE month=? GROUP BY day ORDER BY day", (m,)).fetchall()]
        by_tenant = [dict(r) for r in c.execute("SELECT l.tenant_id, t.name, t.plan, SUM(l.status='ok') calls, SUM(l.status!='ok') denied, COALESCE(SUM(CASE WHEN l.status='ok' THEN l.cost_inr END),0) cost FROM llm_calls l LEFT JOIN tenants t ON t.id=l.tenant_id WHERE l.month=? GROUP BY l.tenant_id ORDER BY cost DESC LIMIT 20", (m,)).fetchall()]
        by_model = [dict(r) for r in c.execute("SELECT model_class, provider, SUM(status='ok') calls, COALESCE(SUM(CASE WHEN status='ok' THEN cost_inr END),0) cost FROM llm_calls WHERE month=? GROUP BY model_class, provider", (m,)).fetchall()]
        usage = c.execute("SELECT COUNT(*) n, SUM(allowed=0) denied, COALESCE(SUM(cost_inr),0) cost FROM tenant_usage WHERE month=?", (m,)).fetchone()
        top_caps = [dict(r) for r in c.execute("SELECT capability, COUNT(*) n, SUM(allowed=0) denied FROM tenant_usage WHERE month=? GROUP BY capability ORDER BY n DESC LIMIT 12", (m,)).fetchall()]
        audit = [dict(r) for r in c.execute("SELECT tenant_id, actor, action, detail, created_at FROM platform_audit ORDER BY id DESC LIMIT 50").fetchall()]
        jobs = {r["status"]: r["n"] for r in c.execute("SELECT status, COUNT(*) n FROM provisioning_jobs GROUP BY status").fetchall()}
        failed_jobs = [dict(r) for r in c.execute("SELECT id, tenant_id, error, created_at FROM provisioning_jobs WHERE status='failed' ORDER BY created_at DESC LIMIT 10").fetchall()]
        bot = c.execute("SELECT COUNT(*) n, SUM(answered=0) unanswered FROM bot_log WHERE created_at > ?", (db.now() - 30 * 86400,)).fetchone()
        gcap = c.execute("SELECT value FROM platform_settings WHERE key='llm_global_cap_inr'").fetchone()
        live = [dict(r) for r in c.execute("SELECT id, name, plan, state FROM tenants WHERE state IN ('ACTIVE','QUOTA_EXCEEDED')").fetchall()]
    risky = []                                                  # outside the connection: dashboard() opens its own (the lock is not re-entrant)
    for t in live:
        try:
            d = engine.dashboard(t["id"])
            if d["over_budget_risk"] or t["state"] == "QUOTA_EXCEEDED": risky.append({"id": t["id"], "name": t["name"], "plan": t["plan"], "state": t["state"], "projected": d["projected_spend_inr"], "budget": d["monthly_spend_limit_inr"]})
        except Exception: pass
    pol = engine.content("token_policy")["limits_and_stops"]; gcap_v = float(gcap["value"]) if gcap else float(pol["global_platform_cap_inr"])
    return {"generated": db.now(), "month": m, "version": "2.8.0", "entitlements_mode": settings.entitlements_mode, "llm_provider": settings.llm_provider or "none (offline)",
            "services": [{"id": s.id, "title": s.title, "owner": s.owner, "status": s.status, "enabled": s.id in settings.enabled_services} for s in SERVICES],
            "tenants": {"by_state": states, "active_by_plan": plans, "at_risk": risky, "jobs": jobs, "failed_jobs": failed_jobs},
            "gateway": {"calls": llm["calls"] or 0, "denied": llm["denied"] or 0, "tokens_in": llm["ti"], "tokens_out": llm["tout"], "cost_inr": round(llm["cost"], 2), "today_calls": llm_today["calls"] or 0, "today_cost_inr": round(llm_today["cost"], 2), "global_cap_inr": gcap_v, "pct_of_cap": round(100 * llm["cost"] / gcap_v, 1) if gcap_v else None, "by_day": by_day, "by_tenant": by_tenant, "by_model": by_model},
            "usage": {"events": usage["n"], "denied": usage["denied"] or 0, "cost_inr": round(usage["cost"], 2), "top_capabilities": top_caps}, "free_pool": engine.sandbox_status(), "bot": {"questions_30d": bot["n"], "unanswered": bot["unanswered"] or 0},
            "hours": hours(m), "audit": audit, "cost_model": {k: v for k, v in engine.cost_model().items() if k in ("fixed_monthly_inr", "break_even_tenants", "status")}}

def logs(kind: str = "audit", limit: int = 200) -> list[dict]:
    q = {"audit": "SELECT id, created_at, tenant_id, actor, action, detail FROM platform_audit ORDER BY id DESC LIMIT ?", "gateway": "SELECT id, created_at, tenant_id, user_email, model_class, provider, tokens_in, tokens_out, cost_inr, latency_ms, status, reason, purpose FROM llm_calls ORDER BY id DESC LIMIT ?",
         "usage": "SELECT id, created_at, tenant_id, capability, units, cost_inr, allowed, reason FROM tenant_usage ORDER BY id DESC LIMIT ?", "provisioning": "SELECT id, created_at, tenant_id, status, steps, error, finished_at FROM provisioning_jobs ORDER BY created_at DESC LIMIT ?",
         "bot": "SELECT id, created_at, session, question, intent, answered FROM bot_log ORDER BY id DESC LIMIT ?", "hours": "SELECT id, created_at, person, day, activity, hours, note, tenant_id FROM founder_hours ORDER BY id DESC LIMIT ?"}
    if kind not in q: raise KeyError(kind)
    with db.conn() as c: return [dict(r) for r in c.execute(q[kind], (min(limit, 1000),)).fetchall()]
