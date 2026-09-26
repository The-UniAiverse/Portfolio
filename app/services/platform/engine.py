"""Control plane: tenants, approval, plans as resource profiles, entitlements, quotas, provisioning jobs, audit.
ACCOUNT ≠ ACCESS ≠ PLAN ≠ ENTITLEMENT ≠ RESOURCE. A feature existing is never the same as a tenant being allowed to use it."""
from __future__ import annotations
import hashlib, json, secrets, uuid, datetime as dt
from pathlib import Path
import yaml
from app.core import db
from app.core.config import settings, ROOT

CONTENT = Path(__file__).parent / "content"
def content(name: str) -> dict: return yaml.safe_load((CONTENT / f"{name}.yaml").read_text())
def _month() -> str: return dt.date.today().strftime("%Y-%m")
def _day() -> str: return dt.date.today().isoformat()
def _tenants_dir() -> Path:
    p = Path(getattr(settings, "tenants_dir", "outputs/tenants")); p = p if p.is_absolute() else ROOT / p; p.mkdir(parents=True, exist_ok=True); return p

# ── plans and limits ──────────────────────────────────────────────────────────────────────────────────────────────────
def plan_profile(plan: str) -> dict:
    P = content("plans")
    if plan == "free":
        f = P["free_sandbox"]; return {"id": "free", "title": f["title"], **f["per_user"], "capabilities": list(f["capabilities"]), "denied": list(f["denied"]), "platform_fee_inr": 0, "setup_fee_inr": 0, "infra_estimate_inr": 0}
    if plan in P.get("classroom", {}): p = dict(P["classroom"][plan]); p["id"] = plan; p.setdefault("daily_queries", None); p.setdefault("denied", []); return p
    if plan not in P["plans"]: raise ValueError(f"unknown plan '{plan}' — one of free, {', '.join(P['plans'])}")
    p = dict(P["plans"][plan]); p["id"] = plan; p.setdefault("daily_queries", None); p.setdefault("denied", []); return p

def effective_limits(t: dict) -> dict:
    base = plan_profile(t["plan"] or t["requested_plan"] or "free"); ov = json.loads(t.get("limits") or "{}")
    caps = set(base["capabilities"]) | set(ov.pop("capabilities_add", [])); caps -= set(ov.pop("capabilities_remove", [])); caps -= set(base.get("denied", []))
    out = {**base, **{k: v for k, v in ov.items() if v is not None and k not in ("reason", "by")}}; out["capabilities"] = sorted(caps); return out

# ── audit and state machine ───────────────────────────────────────────────────────────────────────────────────────────
def audit(tenant_id: str | None, actor: str, action: str, detail: str = ""):
    with db.conn() as c: c.execute("INSERT INTO platform_audit (tenant_id, actor, action, detail, created_at) VALUES (?,?,?,?,?)", (tenant_id, actor, action, detail[:2000], db.now()))

def load(tenant_id: str) -> dict:
    with db.conn() as c: row = c.execute("SELECT * FROM tenants WHERE id=?", (tenant_id,)).fetchone()
    if not row: raise KeyError(f"tenant {tenant_id} not found")
    return dict(row)

def transition(tenant_id: str, to: str, actor: str, detail: str = "") -> dict:
    t = load(tenant_id); allowed = content("plans")["transitions"].get(t["state"], [])
    if to not in allowed:
        audit(tenant_id, actor, "transition_refused", f"{t['state']} → {to}: {detail}"); raise ValueError(f"cannot move {t['state']} → {to} (allowed: {', '.join(allowed) or 'none'})")
    with db.conn() as c: c.execute("UPDATE tenants SET state=?, updated_at=? WHERE id=?", (to, db.now(), tenant_id))
    audit(tenant_id, actor, "transition", f"{t['state']} → {to}. {detail}"); t["state"] = to; return t

# ── lifecycle ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def register(organisation: str, contact_name: str, contact_email: str, requested_plan: str, purpose: str) -> dict:
    plan_profile(requested_plan)                       # validates
    with db.conn() as c:
        dup = c.execute("SELECT id, state FROM tenants WHERE contact_email=? AND state NOT IN ('REJECTED','CANCELLED','EXPIRED')", (contact_email,)).fetchone()
        if dup: return {"tenant_id": dup["id"], "state": dup["state"], "note": "an active request already exists for this email"}
        tid = "TEN-" + uuid.uuid4().hex[:8].upper(); now = db.now()
        c.execute("INSERT INTO tenants (id, name, contact_email, contact_name, plan, state, requested_plan, purpose, limits, environment, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (tid, organisation, contact_email, contact_name, None, "PENDING", requested_plan, purpose, "{}", "{}", now, now))
    audit(tid, contact_email, "register", f"requested {requested_plan}: {purpose[:200]}")
    return {"tenant_id": tid, "state": "PENDING", "note": "Approval required. You will be emailed when an admin decides."}

def sandbox_status() -> dict:
    f = content("plans")["free_sandbox"]; m = _month()
    with db.conn() as c:
        users = c.execute("SELECT COUNT(*) n FROM tenants WHERE plan='free' AND state IN ('ACTIVE','PROVISIONING','APPROVED','QUOTA_EXCEEDED')").fetchone()["n"]
        q = c.execute("SELECT COALESCE(SUM(units),0) u, COALESCE(SUM(cost_inr),0) c FROM tenant_usage WHERE month=? AND allowed=1 AND (tenant_id IN (SELECT id FROM tenants WHERE plan='free') OR tenant_id='public')", (m,)).fetchone()
        stop = c.execute("SELECT value FROM platform_settings WHERE key='free_approvals_paused'").fetchone()
    pool = f["pool"]; used_q, used_c = int(q["u"]), float(q["c"]); exhausted = used_q >= pool["monthly_queries"] or used_c >= pool["monthly_budget_inr"]
    return {"month": m, "approved_users": users, "max_approved_users": pool["max_approved_users"], "queries_used": used_q, "monthly_queries": pool["monthly_queries"], "spend_inr": round(used_c, 2), "monthly_budget_inr": pool["monthly_budget_inr"],
            "exhausted": exhausted, "approvals_paused": bool(stop and stop["value"] == "1"), "status": "FREE CAPACITY EXHAUSTED" if exhausted else "ok",
            "can_approve_more": (not exhausted) and users < pool["max_approved_users"] and not (stop and stop["value"] == "1")}

def approve(tenant_id: str, plan: str | None, decided_by: str, note: str = "") -> dict:
    t = load(tenant_id); plan = plan or t["requested_plan"] or "free"; plan_profile(plan)
    if plan == "free" and not sandbox_status()["can_approve_more"]: raise ValueError("free sandbox is at capacity or paused — approve a paid plan or wait for next month")
    with db.conn() as c: c.execute("UPDATE tenants SET plan=?, updated_at=? WHERE id=?", (plan, db.now(), tenant_id))
    transition(tenant_id, "APPROVED", decided_by, f"plan {plan}. {note}")
    if plan == "free": transition(tenant_id, "PROVISIONING", "system", "free plan: no payment"); job = enqueue(tenant_id); return {"tenant_id": tenant_id, "state": "PROVISIONING", "job_id": job}
    transition(tenant_id, "PAYMENT_PENDING", "system", f"awaiting payment for platform.{plan}"); return {"tenant_id": tenant_id, "state": "PAYMENT_PENDING", "pay_product": f"platform.{plan}", "pay_url": f"{settings.public_url}/pay?product=platform.{plan}&tenant={tenant_id}"}

def reject(tenant_id: str, decided_by: str, note: str = ""): return transition(tenant_id, "REJECTED", decided_by, note)

def on_payment(tenant_id: str | None, email: str | None, product_id: str, actor: str = "payments") -> dict | None:
    """Called by the payments service when a platform.* product is paid (Razorpay verify/webhook, or admin mark-paid)."""
    if not product_id.startswith("platform."): return None
    plan = product_id.split(".")[1]
    with db.conn() as c:
        row = c.execute("SELECT * FROM tenants WHERE id=? AND state IN ('PAYMENT_PENDING','EXPIRED')", (tenant_id,)).fetchone() if tenant_id else None
        if not row and email: row = c.execute("SELECT * FROM tenants WHERE contact_email=? AND state IN ('PAYMENT_PENDING','EXPIRED') ORDER BY updated_at DESC", (email,)).fetchone()
    if not row: audit(tenant_id, actor, "payment_unmatched", f"{product_id} paid but no tenant in PAYMENT_PENDING for {email}"); return None
    if row["plan"] != plan:
        with db.conn() as c: c.execute("UPDATE tenants SET plan=? WHERE id=?", (plan, row["id"]))
    if row["state"] == "EXPIRED": transition(row["id"], "PAYMENT_PENDING", actor, "renewal payment")
    transition(row["id"], "PROVISIONING", actor, f"paid {product_id}"); return {"tenant_id": row["id"], "job_id": enqueue(row["id"])}

# ── provisioning (background job, never the browser's wait) ───────────────────────────────────────────────────────────
STEPS = ["create_tenant_dir", "create_database", "create_vector_namespace", "create_storage_namespace", "write_environment", "create_api_credentials", "apply_quotas", "create_admin_user", "activate_subscription"]
def enqueue(tenant_id: str) -> str:
    jid = "JOB-" + uuid.uuid4().hex[:8].upper()
    with db.conn() as c: c.execute("INSERT INTO provisioning_jobs (id, tenant_id, status, steps, created_at) VALUES (?,?,?,?,?)", (jid, tenant_id, "queued", "[]", db.now()))
    audit(tenant_id, "system", "provisioning_queued", jid); return jid

def run_jobs(limit: int = 20) -> list[dict]:
    """The worker tick. Idempotent: every step checks before it creates. Safe to run from a cron, the worker container, or in-process."""
    with db.conn() as c: jobs = [dict(j) for j in c.execute("SELECT * FROM provisioning_jobs WHERE status='queued' ORDER BY created_at LIMIT ?", (limit,)).fetchall()]
    out = []
    for j in jobs:
        with db.conn() as c: c.execute("UPDATE provisioning_jobs SET status='running' WHERE id=?", (j["id"],))
        done = []; api_key = None
        try:
            t = load(j["tenant_id"]); lim = effective_limits(t); prof = plan_profile(t["plan"]); base = _tenants_dir() / t["id"]; env = json.loads(t["environment"] or "{}")
            for step in STEPS:
                if step == "create_tenant_dir": base.mkdir(parents=True, exist_ok=True); env["root"] = str(base.relative_to(ROOT))
                elif step == "create_database":
                    if prof["isolation"]["db"] if isinstance(prof.get("isolation"), dict) else False: pass
                    dbp = base / "db" / "tenant.db"; dbp.parent.mkdir(exist_ok=True); import sqlite3; sqlite3.connect(dbp).execute("CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT)").connection.commit(); env["database"] = str(dbp.relative_to(ROOT)); env["db_isolation"] = (prof.get("isolation") or {}).get("db", "shared-host")
                elif step == "create_vector_namespace": (base / "vector").mkdir(exist_ok=True); env["vector_namespace"] = f"tenant_{t['id'].lower().replace('-', '_')}"
                elif step == "create_storage_namespace": (base / "storage").mkdir(exist_ok=True); env["storage_prefix"] = f"tenants/{t['id']}/"
                elif step == "write_environment":
                    (base / ".env.tenant").write_text("\n".join(f"{k.upper()}={v}" for k, v in {"tenant_id": t["id"], "plan": t["plan"], "db_path": env["database"], "vector_namespace": env["vector_namespace"], "storage_prefix": env["storage_prefix"], "max_users": lim["users"], "monthly_queries": lim["monthly_queries"], "max_context_tokens": lim["max_context_tokens"], "monthly_spend_limit_inr": lim["monthly_spend_limit_inr"]}.items()) + "\n")
                    if t["plan"] in ("silver", "gold"):
                        (base / "docker-compose.tenant.yml").write_text(f"# Dedicated environment for {t['id']} ({t['plan']}). Generated; deploy on the tenant host with: docker compose -f docker-compose.tenant.yml --env-file .env.tenant up -d\nservices:\n  api:\n    build: ../../..\n    env_file: .env.tenant\n    environment: [\"ENABLED_SERVICES=readiness_audit,strategy,governance,automation,demos,delivery\", \"ENTITLEMENTS_MODE=enforce\"]\n    volumes: [\"./storage:/srv/outputs\"]\n    restart: unless-stopped\n    deploy: {{resources: {{limits: {{cpus: '{2 if t['plan']=='silver' else 8}', memory: '{'8G' if t['plan']=='silver' else '32G'}'}}}}}}\n")
                        env["deployment"] = "dedicated compose (generated)"
                    else: env["deployment"] = "shared-isolated slice on the customer host"
                elif step == "create_api_credentials":
                    if not t.get("key_hash"):
                        api_key = "uav_" + secrets.token_urlsafe(24); h = hashlib.sha256(api_key.encode()).hexdigest()
                        with db.conn() as c: c.execute("UPDATE tenants SET key_hash=? WHERE id=?", (h, t["id"]))
                        env["api_key_issued"] = _day()
                elif step == "apply_quotas": env["quotas"] = {k: lim[k] for k in ("users", "concurrency", "monthly_queries", "max_context_tokens", "storage_gb", "vector_gb", "knowledge_bases", "agent_max_tool_calls", "monthly_spend_limit_inr")}
                elif step == "create_admin_user":
                    with db.conn() as c:
                        if not c.execute("SELECT 1 FROM tenant_users WHERE tenant_id=? AND email=?", (t["id"], t["contact_email"])).fetchone(): c.execute("INSERT INTO tenant_users (tenant_id, email, role, created_at) VALUES (?,?,?,?)", (t["id"], t["contact_email"], "admin", db.now()))
                elif step == "activate_subscription":
                    exp = db.now() + 31 * 86400 if t["plan"] != "free" else None
                    with db.conn() as c: c.execute("UPDATE tenants SET environment=?, activated_at=?, expires_at=?, updated_at=? WHERE id=?", (json.dumps(env), db.now(), exp, db.now(), t["id"]))
                    transition(t["id"], "ACTIVE", "provisioner", j["id"])
                done.append(step)
            with db.conn() as c: c.execute("UPDATE provisioning_jobs SET status='done', steps=?, finished_at=? WHERE id=?", (json.dumps(done), db.now(), j["id"]))
            out.append({"job_id": j["id"], "tenant_id": j["tenant_id"], "status": "done", "steps": done, "api_key": api_key})
        except Exception as e:
            with db.conn() as c: c.execute("UPDATE provisioning_jobs SET status='failed', steps=?, error=?, finished_at=? WHERE id=?", (json.dumps(done), str(e)[:500], db.now(), j["id"]))
            audit(j["tenant_id"], "provisioner", "provisioning_failed", f"{j['id']} after {done}: {e}")
            try: transition(j["tenant_id"], "PAYMENT_PENDING", "provisioner", f"job {j['id']} failed: {e}")
            except ValueError: pass
            out.append({"job_id": j["id"], "tenant_id": j["tenant_id"], "status": "failed", "steps": done, "error": str(e)})
    return out

# ── entitlement engine ────────────────────────────────────────────────────────────────────────────────────────────────
def by_key(api_key: str) -> dict | None:
    h = hashlib.sha256(api_key.encode()).hexdigest()
    with db.conn() as c: row = c.execute("SELECT * FROM tenants WHERE key_hash=?", (h,)).fetchone()
    return dict(row) if row else None

def usage(tenant_id: str, month: str | None = None) -> dict:
    m = month or _month()
    with db.conn() as c:
        r = c.execute("SELECT COALESCE(SUM(units),0) u, COALESCE(SUM(cost_inr),0) c, COUNT(*) n FROM tenant_usage WHERE tenant_id=? AND month=? AND allowed=1", (tenant_id, m)).fetchone()
        d = c.execute("SELECT COALESCE(SUM(units),0) u FROM tenant_usage WHERE tenant_id=? AND day=? AND allowed=1", (tenant_id, _day())).fetchone()
        docs = c.execute("SELECT COUNT(*) n FROM tenant_usage WHERE tenant_id=? AND month=? AND allowed=1 AND capability IN ('doc.generate','delivery.pack')", (tenant_id, m)).fetchone()
        users = c.execute("SELECT COUNT(*) n FROM tenant_users WHERE tenant_id=?", (tenant_id,)).fetchone()
    return {"month": m, "units": int(r["u"]), "cost_inr": round(float(r["c"]), 2), "requests": r["n"], "units_today": int(d["u"]), "documents": docs["n"], "users": users["n"]}

def _record(tenant_id: str, capability: str, units: int, cost: float, allowed: bool, reason: str):
    with db.conn() as c: c.execute("INSERT INTO tenant_usage (tenant_id, month, day, capability, units, cost_inr, allowed, reason, created_at) VALUES (?,?,?,?,?,?,?,?,?)", (tenant_id, _month(), _day(), capability, units, cost, int(allowed), reason, db.now()))

def check(tenant: dict | None, capability: str, units: int | None = None, record: bool = True) -> dict:
    """May this tenant do this capability now? One answer for every service. `tenant=None` = anonymous visitor → the public share of the free sandbox."""
    caps = content("capabilities")["capabilities"]; cap = caps.get(capability)
    if not cap: return {"allowed": False, "reason": f"unknown capability '{capability}'", "remaining": 0}
    u = cap["units"] if units is None else units; cost = float(cap["approx_cost_inr"])
    if tenant is None:
        f = content("plans")["free_sandbox"]; s = sandbox_status(); pub_allowed = capability in ("demo.run", "demo.rag_preloaded", "audit.free", "quest.free", "course_finder", "bot")
        ok, why = (False, "sign in with a tenant key: this capability is not in the public sandbox") if not pub_allowed else (False, "FREE CAPACITY EXHAUSTED for this month") if s["exhausted"] else (True, "public sandbox")
        if record: _record("public", capability, u, cost, ok, why)
        return {"allowed": ok, "reason": why, "tenant": "public", "remaining": max(0, f["pool"]["monthly_queries"] - s["queries_used"] - u)}
    lim = effective_limits(tenant); us = usage(tenant["id"]); tid = tenant["id"]; ok, why = True, "ok"
    if tenant["state"] not in content("plans")["serving_states"]: ok, why = False, f"tenant is {tenant['state']}, not ACTIVE"
    elif capability not in lim["capabilities"]: ok, why = False, f"'{capability}' is not in the {lim['id']} plan"
    elif lim.get("monthly_queries") is not None and us["units"] + u > lim["monthly_queries"]: ok, why = False, f"monthly quota {lim['monthly_queries']} reached ({us['units']} used)"
    elif lim.get("daily_queries") and us["units_today"] + u > lim["daily_queries"]: ok, why = False, f"daily quota {lim['daily_queries']} reached"
    elif lim.get("monthly_spend_limit_inr") and lim["monthly_spend_limit_inr"] > 0 and us["cost_inr"] + cost > lim["monthly_spend_limit_inr"]: ok, why = False, f"monthly spend limit ₹{lim['monthly_spend_limit_inr']:,.0f} reached"
    elif capability in ("doc.generate", "delivery.pack") and lim.get("doc_generation_per_month") and us["documents"] + 1 > lim["doc_generation_per_month"]: ok, why = False, f"document generation limit {lim['doc_generation_per_month']}/month reached"
    elif tenant["plan"] == "free" and sandbox_status()["exhausted"]: ok, why = False, "FREE CAPACITY EXHAUSTED for this month"
    if record: _record(tid, capability, u, cost, ok, why)
    if not ok and why.startswith("monthly quota") and tenant["state"] == "ACTIVE":
        try: transition(tid, "QUOTA_EXCEEDED", "entitlements", why)
        except ValueError: pass
    return {"allowed": ok, "reason": why, "tenant": tid, "plan": lim["id"], "remaining": max(0, (lim.get("monthly_queries") or 0) - us["units"] - (u if ok else 0)), "mode": settings.entitlements_mode}

def guarded_capability(path: str) -> str | None:
    """Which capability guards this URL path? From capabilities.yaml `guards` (prefix match with a trailing *)."""
    for cid, cap in content("capabilities")["capabilities"].items():
        for g in cap.get("guards", []):
            if (g.endswith("*") and path.startswith(g[:-1])) or path == g: return cid
    return None

def dashboard(tenant_id: str) -> dict:
    t = load(tenant_id); lim = effective_limits(t); us = usage(tenant_id); env = json.loads(t["environment"] or "{}"); root = ROOT / env["root"] if env.get("root") else None
    size_gb = round(sum(p.stat().st_size for p in root.rglob("*") if p.is_file()) / 1e9, 3) if root and root.exists() else 0.0
    today = dt.date.today(); days_in = (dt.date(today.year + (today.month == 12), today.month % 12 + 1, 1) - dt.date(today.year, today.month, 1)).days
    projected = round(us["cost_inr"] / max(1, today.day) * days_in, 2)
    with db.conn() as c:
        jobs = [dict(j) for j in c.execute("SELECT id, status, steps, error, created_at, finished_at FROM provisioning_jobs WHERE tenant_id=? ORDER BY created_at DESC LIMIT 5", (tenant_id,)).fetchall()]
        log = [dict(a) for a in c.execute("SELECT actor, action, detail, created_at FROM platform_audit WHERE tenant_id=? ORDER BY id DESC LIMIT 20", (tenant_id,)).fetchall()]
        by_cap = [dict(r) for r in c.execute("SELECT capability, SUM(units) units, SUM(cost_inr) cost_inr, SUM(1-allowed) denied FROM tenant_usage WHERE tenant_id=? AND month=? GROUP BY capability", (tenant_id, us["month"])).fetchall()]
    return {"id": tenant_id, "organisation": t["name"], "contact": {"name": t["contact_name"], "email": t["contact_email"]}, "state": t["state"], "plan": t["plan"] or f"(requested {t['requested_plan']})", "purpose": t["purpose"],
            "users": f"{us['users']} / {lim.get('users')}", "queries": f"{us['units']} / {lim.get('monthly_queries')}", "storage_gb": f"{size_gb} / {lim.get('storage_gb')}", "knowledge_bases": f"0 / {lim.get('knowledge_bases')}",
            "capabilities": lim["capabilities"], "monthly_spend_limit_inr": lim.get("monthly_spend_limit_inr"), "spend_inr_month_to_date": us["cost_inr"], "projected_spend_inr": projected,
            "over_budget_risk": bool(lim.get("monthly_spend_limit_inr")) and projected > lim["monthly_spend_limit_inr"], "usage_by_capability": by_cap, "limits": {k: lim.get(k) for k in ("users", "concurrency", "monthly_queries", "daily_queries", "max_context_tokens", "storage_gb", "vector_gb", "knowledge_bases", "agent_max_tool_calls", "doc_generation_per_month")},
            "overrides": json.loads(t["limits"] or "{}"), "environment": env, "expires_at": t["expires_at"], "jobs": jobs, "audit": log}

def set_limits(tenant_id: str, patch: dict, by: str) -> dict:
    t = load(tenant_id); cur = json.loads(t["limits"] or "{}"); reason = patch.pop("reason"); by = patch.pop("by", by)
    for k in ("capabilities_add", "capabilities_remove"):
        if patch.get(k): cur[k] = sorted(set(cur.get(k, [])) | set(patch[k]))
        patch.pop(k, None)
    cur.update({k: v for k, v in patch.items() if v is not None})
    with db.conn() as c: c.execute("UPDATE tenants SET limits=?, updated_at=? WHERE id=?", (json.dumps(cur), db.now(), tenant_id))
    audit(tenant_id, by, "limits_changed", f"{json.dumps({k: v for k, v in patch.items() if v is not None})} — {reason}"); return effective_limits(load(tenant_id))

def expire_due(actor: str = "scheduler") -> list[str]:
    """Nightly: ACTIVE tenants past expires_at → EXPIRED (no resources until renewal). QUOTA_EXCEEDED → ACTIVE on the 1st."""
    out = []
    with db.conn() as c: rows = [dict(r) for r in c.execute("SELECT id, state, expires_at FROM tenants WHERE (state='ACTIVE' AND expires_at IS NOT NULL AND expires_at < ?) OR state='QUOTA_EXCEEDED'", (db.now(),)).fetchall()]
    for r in rows:
        if r["state"] == "ACTIVE": transition(r["id"], "EXPIRED", actor, "subscription expired"); out.append(f"{r['id']} EXPIRED")
        elif dt.date.today().day == 1 and usage(r["id"])["units"] == 0: transition(r["id"], "ACTIVE", actor, "new month"); out.append(f"{r['id']} ACTIVE")
    return out

# ── cost model ────────────────────────────────────────────────────────────────────────────────────────────────────────
def create_cohort(name: str, track: str, contact_email: str, starts: str, ends: str, seats: int | None, created_by: str) -> dict:
    """Admin-created classroom tenant: no self-registration, no payment, provisioned immediately, expires with the cohort."""
    prof = plan_profile("cohort"); tid = "COH-" + uuid.uuid4().hex[:8].upper(); now = db.now()
    lim = {"users": seats} if seats else {}
    with db.conn() as c:
        c.execute("INSERT INTO tenants (id, name, contact_email, contact_name, plan, state, requested_plan, purpose, limits, environment, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (tid, name, contact_email, created_by, "cohort", "APPROVED", "cohort", f"track={track}; {starts} → {ends}", json.dumps(lim), json.dumps({"track": track, "starts": starts, "ends": ends}), now, now))
    audit(tid, created_by, "cohort_created", f"{name} ({track}) {starts} → {ends}, seats {seats or prof['users']}")
    transition(tid, "PROVISIONING", created_by, "cohort"); jid = enqueue(tid); ran = run_jobs(); job = next((r for r in ran if r["job_id"] == jid), None)
    with db.conn() as c: c.execute("UPDATE tenants SET expires_at=? WHERE id=?", (now + prof.get("expires_days", 45) * 86400, tid))
    return {"cohort_id": tid, "state": load(tid)["state"], "api_key": job["api_key"] if job else None, "expires_days": prof.get("expires_days", 45), "note": "Give the key to learners for live labs only. It expires with the cohort. Set the provider console cap before use."}

def add_learners(tenant_id: str, emails: list[str], by: str) -> dict:
    t = load(tenant_id); lim = effective_limits(t); added = []
    with db.conn() as c:
        have = c.execute("SELECT COUNT(*) n FROM tenant_users WHERE tenant_id=? AND role='learner'", (tenant_id,)).fetchone()["n"]
        for e in emails:
            e = e.strip().lower()
            if not e or c.execute("SELECT 1 FROM tenant_users WHERE tenant_id=? AND email=?", (tenant_id, e)).fetchone(): continue
            if have + len(added) >= lim["users"]: break
            c.execute("INSERT INTO tenant_users (tenant_id, email, role, created_at) VALUES (?,?,?,?)", (tenant_id, e, "learner", db.now())); added.append(e)
    audit(tenant_id, by, "learners_added", ", ".join(added)); return {"added": added, "skipped": [e for e in emails if e.strip().lower() not in added], "seats": f"{have + len(added)} / {lim['users']}"}

def llm_rollup(tenant_id: str, month: str | None = None) -> dict:
    m = month or _month()
    with db.conn() as c:
        tot = c.execute("SELECT SUM(status='ok') n, COALESCE(SUM(tokens_in),0) ti, COALESCE(SUM(tokens_out),0) tout, COALESCE(SUM(cost_inr),0) cost, SUM(status!='ok') denied FROM llm_calls WHERE tenant_id=? AND month=?", (tenant_id, m)).fetchone()
        users = [dict(r) for r in c.execute("SELECT user_email, SUM(status='ok') calls, COALESCE(SUM(cost_inr),0) cost_inr, SUM(status!='ok') denied, MAX(created_at) last FROM llm_calls WHERE tenant_id=? AND month=? GROUP BY user_email ORDER BY cost_inr DESC", (tenant_id, m)).fetchall()]
    lim = effective_limits(load(tenant_id)); cap = lim.get("monthly_spend_limit_inr") or 0; pol = content("token_policy")["limits_and_stops"]
    return {"tenant_id": tenant_id, "month": m, "calls": tot["n"], "tokens_in": tot["ti"], "tokens_out": tot["tout"], "cost_inr": round(tot["cost"], 2), "cap_inr": cap, "pct_of_cap": round(100 * tot["cost"] / cap, 1) if cap else None, "alert": bool(cap) and tot["cost"] >= cap * pol["alert_at_pct"] / 100, "denied": tot["denied"], "users": users}

def cost_model(mix: dict | None = None) -> dict:
    """Per-plan unit economics and the platform P&L at a given tenant mix. All inputs are in content/cost_model.yaml and plans.yaml."""
    cm = content("cost_model"); P = content("plans"); fixed = sum(v["inr"] for v in cm["fixed"].values()); plans = {}
    for pid, p in P["plans"].items():
        cost = sum(v["inr"] for v in cm["per_tenant"][pid].values()); infra_cost = sum(v["inr"] for k, v in cm["per_tenant"][pid].items() if k != "support")
        infra_billed = round(p["infra_estimate_inr"] * (1 + cm["variable"]["infra_markup_pct"] / 100)); revenue = p["platform_fee_inr"] + infra_billed; fees = round(revenue * cm["variable"]["razorpay_pct"] / 100)
        margin = revenue - cost - fees; plans[pid] = {"platform_fee_inr": p["platform_fee_inr"], "infra_billed_inr": infra_billed, "setup_fee_inr": p["setup_fee_inr"], "monthly_revenue_inr": revenue, "monthly_cost_inr": cost, "cost_lines": {k: v["inr"] for k, v in cm["per_tenant"][pid].items()},
                      "payment_fees_inr": fees, "gross_margin_inr": margin, "gross_margin_pct": round(100 * margin / revenue, 1) if revenue else 0, "infra_cost_vs_billed": f"cost {infra_cost} vs billed {infra_billed}", "queries": p["monthly_queries"], "cost_per_query_inr": round(cost / p["monthly_queries"], 2), "revenue_per_query_inr": round(revenue / p["monthly_queries"], 2)}
    mix = mix or {"bronze": 4, "silver": 2, "gold": 0}; rev = sum(plans[k]["monthly_revenue_inr"] * n for k, n in mix.items()); cost = sum(plans[k]["monthly_cost_inr"] * n for k, n in mix.items()); fees = sum(plans[k]["payment_fees_inr"] * n for k, n in mix.items())
    setup = sum(plans[k]["setup_fee_inr"] * n for k, n in mix.items()); be = {k: (fixed / plans[k]["gross_margin_inr"] if plans[k]["gross_margin_inr"] > 0 else None) for k in plans}
    people = cm["people"]["founder_time_hours_per_month"] * cm["people"]["hourly_opportunity_cost_inr"]
    return {"currency": "INR", "assumptions": cm, "fixed_monthly_inr": fixed, "fixed_lines": {k: v["inr"] for k, v in cm["fixed"].items()}, "plans": plans, "mix": mix, "monthly": {"revenue": rev, "cost_of_tenants": cost, "fixed": fixed, "payment_fees": fees, "operating_result": rev - cost - fixed - fees, "one_time_setup_fees": setup, "founder_time_inr_not_included": people},
            "break_even_tenants": {k: (max(round(v, 2), 0.01) if v else "never at this price") for k, v in be.items()}, "free_sandbox": {"monthly_cap_inr": cm["fixed"]["free_sandbox_pool"]["inr"], "queries": P["free_sandbox"]["pool"]["monthly_queries"], "max_users": P["free_sandbox"]["pool"]["max_approved_users"]},
            "sensitivity": {"llm_price_x2": {k: plans[k]["gross_margin_inr"] - plans[k]["cost_lines"]["llm"] for k in plans}, "half_quota_used": {k: plans[k]["gross_margin_inr"] + round(plans[k]["cost_lines"]["llm"] / 2) for k in plans}, "gold_with_gpu_75k": plans["gold"]["gross_margin_inr"] - 75000 + round(75000 * (1 + cm["variable"]["infra_markup_pct"] / 100))},
            "status": "PLACEHOLDER assumptions — every number changes when Sarfi confirms prices and hosting."}
