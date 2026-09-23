"""LLM gateway (v2.6.1). The only door from classroom or tenant code to a provider:
user → key (tenant) → user email → cohort/plan → entitlement → per-user and per-cohort quotas → budget → rate limit → provider → metering → cost → audit.
Hard stops answer 402 with the reason. Provider-side caps are the second lock and are set by hand in the provider console (registries/providers.yaml)."""
from __future__ import annotations
import time, collections, datetime as dt
from app.core import db, llm
from app.core.config import settings
from . import engine

_rate: dict[str, collections.deque] = collections.defaultdict(collections.deque)
def _limited(key: str, per_minute: int) -> bool:
    q = _rate[key]; now = time.time()
    while q and q[0] < now - 60: q.popleft()
    if len(q) >= per_minute: return True
    q.append(now); return False

def _price(model_class: str, tokens_in: int, tokens_out: int) -> float:
    m = engine.content("registries/models")["classes"][model_class]; return tokens_in / 1e6 * m["in_inr_per_m"] + tokens_out / 1e6 * m["out_inr_per_m"]

def _record(tid, email, provider, model, cls, ti, to, cost, ms, status, reason, purpose):
    with db.conn() as c: c.execute("INSERT INTO llm_calls (tenant_id, user_email, month, day, provider, model, model_class, tokens_in, tokens_out, cost_inr, latency_ms, status, reason, purpose, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                   (tid, email, dt.date.today().strftime("%Y-%m"), dt.date.today().isoformat(), provider, model, cls, ti, to, cost, ms, status, reason, purpose, db.now()))

def _user_usage(tid: str, email: str) -> dict:
    with db.conn() as c:
        d = c.execute("SELECT COUNT(*) n FROM llm_calls WHERE tenant_id=? AND user_email=? AND day=? AND status='ok'", (tid, email, dt.date.today().isoformat())).fetchone()["n"]
        m = c.execute("SELECT COUNT(*) n, COALESCE(SUM(cost_inr),0) cost FROM llm_calls WHERE tenant_id=? AND user_email=? AND month=? AND status='ok'", (tid, email, dt.date.today().strftime("%Y-%m"))).fetchone()
    return {"today": d, "cohort_calls": m["n"], "cohort_cost": float(m["cost"])}

def complete(tenant: dict, email: str | None, prompt: str, max_tokens: int | None, model_class: str | None, purpose: str = "") -> tuple[int, dict]:
    """Returns (http_status, body). 200 = answered; 402 = a limit said no; 403 = identity problem; 429 = rate limited; 503 = provider failed."""
    tid = tenant["id"]; lim = engine.effective_limits(tenant); pol = engine.content("token_policy"); classroom = bool(lim.get("classroom")); email = (email or "").strip().lower()
    cls = model_class or lim.get("default_model_class", "cheap"); allowed_cls = lim.get("allowed_model_classes", ["cheap", "mid"]); mt = min(max_tokens or lim.get("max_output_tokens", 800), lim.get("max_output_tokens", 800))
    def deny(code, reason):
        _record(tid, email, settings.llm_provider, "-", cls, 0, 0, 0.0, 0, "denied", reason, purpose); engine.audit(tid, email or "key", "llm_denied", reason); return code, {"detail": reason, "tenant": tid, "user": email or None}
    if tenant["state"] not in engine.content("plans")["serving_states"]: return deny(402, f"tenant is {tenant['state']}")
    if tenant.get("expires_at") and tenant["expires_at"] < db.now(): return deny(402, "cohort key has expired")
    if "llm.complete" not in lim["capabilities"]: return deny(402, "llm.complete is not in this plan")
    if classroom:
        if not email: return deny(403, "X-User-Email is required for classroom keys")
        with db.conn() as c: known = c.execute("SELECT 1 FROM tenant_users WHERE tenant_id=? AND email=?", (tid, email)).fetchone()
        if not known: return deny(403, "this email is not enrolled in the cohort")
    if cls not in allowed_cls: return deny(402, f"model class '{cls}' is not allowed on this plan (allowed: {', '.join(allowed_cls)})")
    if len(prompt) // 4 > lim.get("max_context_tokens", 6000): return deny(402, f"prompt exceeds {lim.get('max_context_tokens')} tokens")
    us = engine.usage(tid); cap = lim.get("monthly_spend_limit_inr") or 0
    if lim.get("monthly_queries") and us["units"] >= lim["monthly_queries"]: return deny(402, f"cohort/tenant monthly quota {lim['monthly_queries']} reached")
    if cap and us["cost_inr"] >= cap: return deny(402, f"monthly spend limit ₹{cap:,.0f} reached — HARD STOP")
    if classroom:
        uu = _user_usage(tid, email)
        if uu["today"] >= lim.get("per_user_daily_queries", 40): return deny(402, f"your daily limit of {lim.get('per_user_daily_queries', 40)} calls is reached; try tomorrow")
        if uu["cohort_calls"] >= lim.get("per_user_cohort_queries", 400): return deny(402, "your cohort call limit is reached")
        if uu["cohort_cost"] >= lim.get("per_user_spend_limit_inr", 500): return deny(402, f"your cohort spend limit ₹{lim.get('per_user_spend_limit_inr', 500)} is reached")
    with db.conn() as c: g = c.execute("SELECT value FROM platform_settings WHERE key='llm_global_cap_inr'").fetchone()
    gcap = float(g["value"]) if g else float(pol["limits_and_stops"]["global_platform_cap_inr"])
    with db.conn() as c: gsp = c.execute("SELECT COALESCE(SUM(cost_inr),0) s FROM llm_calls WHERE month=? AND status='ok'", (dt.date.today().strftime("%Y-%m"),)).fetchone()["s"]
    if gsp >= gcap: return deny(402, f"platform-wide monthly LLM cap ₹{gcap:,.0f} reached — HARD STOP")
    if _limited(f"{tid}:{email}", pol["limits_and_stops"]["rate_limit_per_user_per_minute"]) or _limited(tid, pol["limits_and_stops"]["rate_limit_per_cohort_per_minute"]): return deny(429, "rate limit: slow down")
    models = engine.content("registries/models")["classes"][cls]; model = models.get(settings.llm_provider) or settings.llm_model; t0 = time.perf_counter()
    r = llm.complete_with_usage(prompt, mt, model=model)
    ms = int((time.perf_counter() - t0) * 1000)
    if r is None:
        if llm.available(): _record(tid, email, settings.llm_provider, model, cls, 0, 0, 0.0, ms, "failed", "provider error", purpose); return 503, {"detail": "provider call failed; nothing was charged"}
        ti, to = len(prompt) // 4 + 50, min(mt, 60); r = {"text": "[offline] No LLM provider is configured on this server. The gateway metered this call at the model's list price so quotas and budgets behave exactly as in live mode.", "tokens_in": ti, "tokens_out": to, "model": model, "provider": "none"}
    cost = _price(cls, r["tokens_in"], r["tokens_out"]); _record(tid, email, r["provider"], r["model"], cls, r["tokens_in"], r["tokens_out"], cost, ms, "ok", "", purpose)
    engine._record(tid, "llm.complete", 1, cost, True, "gateway")                       # one row in tenant_usage so dashboards and quotas see it
    left = {"tenant_spend_left_inr": round(max(0, cap - us["cost_inr"] - cost), 2) if cap else None}
    if classroom: uu = _user_usage(tid, email); left["your_calls_left_today"] = max(0, lim.get("per_user_daily_queries", 40) - uu["today"]); left["your_spend_left_inr"] = round(max(0, lim.get("per_user_spend_limit_inr", 500) - uu["cohort_cost"]), 2)
    return 200, {"text": r["text"], "model": r["model"], "model_class": cls, "provider": r["provider"], "tokens_in": r["tokens_in"], "tokens_out": r["tokens_out"], "cost_inr": round(cost, 4), "latency_ms": ms, **left}
