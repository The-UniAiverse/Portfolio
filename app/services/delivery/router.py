"""AI Delivery Framework — one engagement record in; tier, plan, estimates, costs, governance, security, gates and a document pack out.
Open endpoints are stateless calculators (safe for the website). Anything that STORES client data needs the admin token (X-Admin-Token)."""
from __future__ import annotations
import json, uuid
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import FileResponse
from app.core import db
from app.core.config import settings
from . import documents, engine
from .schemas import GateDecision, Intake

router = APIRouter(); OUT = settings.outputs_dir / "delivery"

def _admin(token: str | None):
    if not settings.admin_token or token != settings.admin_token: raise HTTPException(401, "admin token required (X-Admin-Token)")
def _run(i: Intake) -> dict:
    try: return engine.run(i)
    except (ValueError, KeyError) as e: raise HTTPException(422, str(e))

SIZ = {"bronze": dict(org_size=1, use_cases=1, users=1, data_sensitivity=1, integrations=1, autonomy=1, regulatory=1, end_state=1), "silver": dict(org_size=2, use_cases=2, users=2, data_sensitivity=2, integrations=2, autonomy=2, regulatory=2, end_state=2),
       "gold": dict(org_size=3, use_cases=3, users=3, data_sensitivity=3, integrations=3, autonomy=2, regulatory=3, end_state=3)}
SAMPLES = {
    "bronze": dict(client="Lotus Dental Clinics", industry="Healthcare services", company_size="small", project="Front-desk drafting assistant", sponsor="Dr. Mehta", product_owner="Clinic manager", problem="Reception staff across six clinics each spend two hours a day rewriting appointment and follow-up messages.",
                   success_metric="minutes per message", baseline="6", target="2", in_scope=["Drafting assistant for appointment and follow-up messages", "Saved prompts and staff training"], out_of_scope=["Clinical advice", "Access to patient records"], sizing=SIZ["bronze"], use_cases=1, integrations=1, data_sources=1,
                   target_stage="mvp", requests_per_day=150, model="cheap", annual_benefit_usd=30000, readiness_score=55, currency="INR"),
    "silver": dict(client="Acme Logistics", industry="Logistics", company_size="medium", project="Shipment-status assistant", sponsor="Head of Customer Service", product_owner="CS operations lead", problem="Agents spend 11 minutes answering each 'where is my shipment' email, 900 a week.",
                   success_metric="median handling time (min)", baseline="11", target="5.5", in_scope=["Grounded assistant on tracking data and 14 policy documents", "Agent-facing drafting inside the ticket tool", "Evaluation set of 120 real emails"], out_of_scope=["Pricing, legal or HR questions", "Autonomous sending"], answer_in_documents=True,
                   sizing=SIZ["silver"], use_cases=2, integrations=3, data_sources=4, target_stage="production", interacts_with_public=True, processes_personal_data=True, jurisdictions=["India (DPDP)", "EU (GDPR, AI Act)"], requests_per_day=1500, model="mid", cheap_route_share=0.3,
                   annual_benefit_usd=210000, readiness_score=33, data_readiness_score=38),
    "gold": dict(client="Meridian Finance", industry="Financial services", company_size="enterprise", project="SME credit-operations agent platform", sponsor="Chief Risk Officer", product_owner="Head of SME Lending Ops", problem="Credit analysts spend 60% of their time gathering documents and re-keying data across six systems before a decision.",
                 success_metric="time to decision (days)", baseline="9", target="3", in_scope=["Document intake and extraction", "Agent that assembles the credit file across six systems", "Analyst review workbench — the human decides"], out_of_scope=["Automated credit decisions", "Retail lending"], needs_actions_in_systems=True,
                 sizing={**SIZ["gold"], "autonomy": 3}, use_cases=5, integrations=7, data_sources=9, target_stage="scale", affects_individuals_rights=True, processes_personal_data=True, writes_to_production_systems=True, jurisdictions=["India (DPDP)", "EU (GDPR, AI Act)"],
                 requests_per_day=4000, model="mid", cheap_route_share=0.4, monthly_growth_pct=2, annual_benefit_usd=2400000, readiness_score=62, data_readiness_score=55)}

@router.get("/config")
def config():
    """Everything a form needs: sizing dimensions, tiers, patterns, models, the 26-deliverable catalogue and content warnings."""
    t = engine.content("tiers"); return {"dimensions": t["dimensions"], "bands": t["bands"], "tiers": t["tiers"], "risk_floors": t["risk_floors"], "patterns": {k: {"title": v["title"], "choose_when": v["choose_when"]} for k, v in engine.content("patterns")["patterns"].items()},
            "models": {k: v["title"] for k, v in engine.content("llm_rates")["models"].items()}, "catalogue": engine.content("deliverables")["catalogue"], "stale_content": engine.staleness(), "stamp": engine.stamp()}
@router.get("/sample")
def sample(tier: str = "silver"):
    if tier not in SAMPLES: raise HTTPException(400, f"tier must be one of {list(SAMPLES)}")
    return SAMPLES[tier]

# ── stateless calculators ───────────────────────────────────────────────────────────────────────────────────────────
@router.post("/size")
def size(i: Intake):
    try: r = engine.risk(i); s = engine.size(i, r)
    except ValueError as e: raise HTTPException(422, str(e))
    return {**s, "risk_tier": r["risk_tier"], "risk_drivers": r["drivers"]}
@router.post("/plan")
def plan(i: Intake): R = _run(i); return R if R["stop"] else {"tier": R["tier"], "readiness": R["readiness"], "plan": R["plan"]}
@router.post("/estimate")
def estimate(i: Intake): R = _run(i); return R if R["stop"] else {"tier": R["tier"], "estimate": R["estimate"]}
@router.post("/llm-cost")
def llm_cost(i: Intake): R = _run(i); return R if R["stop"] else {"tier": R["tier"], "pattern": R["plan"]["pattern"], "llm_cost": R["llm_cost"]}
@router.post("/project-cost")
def project_cost(i: Intake): R = _run(i); return R if R["stop"] else {"tier": R["tier"], "project_cost": R["project_cost"], "estimate_total_days": R["estimate"]["total_days"]}
@router.post("/governance-plan")
def governance_plan(i: Intake): R = _run(i); return R if R["stop"] else {"tier": R["tier"], "governance": R["governance"]}
@router.post("/security-plan")
def security_plan(i: Intake): R = _run(i); return R if R["stop"] else {"tier": R["tier"], "security": R["security"]}
@router.post("/run")
def run(i: Intake):
    """All modules in one call (no storage, no files)."""
    return _run(i)

@router.post("/pack")
def pack(i: Intake, only: str | None = None):
    """M12 — assemble the tier pack: one PDF, one Word file, Markdown and JSON. `only` = comma-separated deliverable ids for a partial pack."""
    R = _run(i)
    if R["stop"]: return R
    stem = f"pack-{uuid.uuid4().hex[:10]}"; f = documents.assemble(i, R, OUT, stem, [x.strip() for x in only.split(",")] if only else None)
    return {"tier": R["tier"], "documents": f["documents"], "deliverables": R["deliverables"], "status": R["status"], "stale_content": R["stale_content"], "stamp": R["stamp"], **{f"{k}_url": f"/api/delivery/file/{v}" for k, v in f["files"].items()},
            "headline": {"score": R["sizing"]["score"], "pattern": R["plan"]["pattern_title"], "total_days": R["estimate"]["total_days"], "build_range": R["project_cost"]["build_range"], "run_monthly": R["project_cost"]["run_monthly"]["total"], "currency": R["project_cost"]["currency"], "risk_tier": R["governance"]["risk_tier"]}}
@router.get("/file/{filename}")
def file(filename: str):
    p = OUT / filename
    if "/" in filename or not p.exists() or p.suffix not in {".md", ".pdf", ".docx", ".json"}: raise HTTPException(404, "not found")
    return FileResponse(p)

# ── stored engagements (admin token) — M1 record, versions, M11 gate records ────────────────────────────────────────
def _summary(R: dict) -> dict:
    return {"stop": True} if R["stop"] else {"tier": R["tier"], "score": R["sizing"]["score"], "pattern": R["plan"]["pattern"], "total_days": R["estimate"]["total_days"], "build_expected": R["project_cost"]["build_expected"], "run_monthly": R["project_cost"]["run_monthly"]["total"], "currency": R["project_cost"]["currency"]}
@router.post("/intake")
def intake(i: Intake, engagement_id: str | None = None, x_admin_token: str | None = Header(None)):
    """Create an engagement, or (with engagement_id) save a new version. Every version keeps its intake, its numbers and the content hash that produced them."""
    _admin(x_admin_token); R = _run(i); now = db.now(); h = R["stamp"]["content_hash"]
    with db.conn() as c:
        if engagement_id:
            row = c.execute("SELECT version FROM delivery_engagements WHERE id=?", (engagement_id,)).fetchone()
            if not row: raise HTTPException(404, "engagement not found")
            v = row["version"] + 1; c.execute("UPDATE delivery_engagements SET client=?, project=?, tier=?, version=?, content_hash=?, intake=?, result=?, updated_at=? WHERE id=?", (i.client, i.project, R.get("tier"), v, h, i.model_dump_json(), json.dumps(R, default=str), now, engagement_id))
        else:
            engagement_id = "ENG-" + uuid.uuid4().hex[:8].upper(); v = 1
            c.execute("INSERT INTO delivery_engagements (id, client, project, tier, version, content_hash, intake, result, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)", (engagement_id, i.client, i.project, R.get("tier"), v, h, i.model_dump_json(), json.dumps(R, default=str), now, now))
        c.execute("INSERT INTO delivery_versions (engagement_id, version, content_hash, intake, summary, created_at) VALUES (?,?,?,?,?,?)", (engagement_id, v, h, i.model_dump_json(), json.dumps(_summary(R)), now))
    return {"engagement_id": engagement_id, "version": v, "summary": _summary(R), "stamp": R["stamp"]}
def _load(eid: str):
    with db.conn() as c: row = c.execute("SELECT * FROM delivery_engagements WHERE id=?", (eid,)).fetchone()
    if not row: raise HTTPException(404, "engagement not found")
    return dict(row)
@router.get("/engagements")
def engagements(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    with db.conn() as c:
        rows = [dict(r) for r in c.execute("SELECT id, client, project, tier, version, content_hash, updated_at FROM delivery_engagements ORDER BY updated_at DESC").fetchall()]
        for r in rows:
            g = c.execute("SELECT gate, decision FROM delivery_gate_records WHERE engagement_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone(); r["last_gate"] = f"{g['gate']}: {g['decision']}" if g else "—"; r["stale"] = r["content_hash"] != engine.stamp()["content_hash"]
    return rows
@router.get("/engagements/{eid}")
def engagement(eid: str, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token); row = _load(eid)
    with db.conn() as c: vers = [dict(v) | {"summary": json.loads(v["summary"])} for v in c.execute("SELECT version, content_hash, summary, created_at FROM delivery_versions WHERE engagement_id=? ORDER BY version", (eid,)).fetchall()]
    cur = engine.stamp()["content_hash"]
    return {"id": eid, "version": row["version"], "intake": json.loads(row["intake"]), "result": json.loads(row["result"]), "versions": vers,
            "stale": row["content_hash"] != cur, "stale_note": "Content files changed since this version was computed — re-save the intake to refresh the numbers." if row["content_hash"] != cur else ""}
@router.post("/engagements/{eid}/pack")
def engagement_pack(eid: str, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token); row = _load(eid); i = Intake(**json.loads(row["intake"])); R = _run(i)
    if R["stop"]: return R
    stem = f"{eid}-v{row['version']}"; f = documents.assemble(i, R, OUT, stem); return {"engagement_id": eid, "version": row["version"], "documents": f["documents"], **{f"{k}_url": f"/api/delivery/file/{v}" for k, v in f["files"].items()}}
@router.get("/gates/{eid}")
def gates(eid: str, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token); row = _load(eid); R = json.loads(row["result"])
    with db.conn() as c: recs = [dict(r) for r in c.execute("SELECT * FROM delivery_gate_records WHERE engagement_id=? ORDER BY id", (eid,)).fetchall()]
    for r in recs:
        for k in ("met", "missing", "evidence", "attendees"): r[k] = json.loads(r[k] or "[]")
    return {"engagement_id": eid, "tier": R.get("tier"), "checklists": R.get("gates", {}), "records": recs}
@router.post("/gates/{eid}/{gate}")
def record_gate(eid: str, gate: str, d: GateDecision, x_admin_token: str | None = Header(None)):
    """Record a gate review. The engine recommends go / conditional go / no-go from the criteria met; a human decision that differs is allowed only with written conditions."""
    _admin(x_admin_token); row = _load(eid); R = json.loads(row["result"]); cl = R.get("gates", {}).get(gate)
    if not cl: raise HTTPException(404, f"gate {gate} is not in this engagement's tier")
    ev = engine.evaluate_gate(cl, d.met); decision = d.decision or ev["recommendation"]
    if decision not in engine.content("gates")["decisions"]: raise HTTPException(422, f"decision must be one of {engine.content('gates')['decisions']}")
    if decision == "go" and ev["blocking_missing"] and not d.conditions.strip(): raise HTTPException(422, f"blocking criteria missing ({', '.join(ev['blocking_missing'])}): a 'go' needs written conditions, or record 'conditional_go' / 'no_go'")
    with db.conn() as c:
        c.execute("INSERT INTO delivery_gate_records (engagement_id, gate, decision, recommendation, met, missing, evidence, attendees, decided_by, conditions, risks_carried, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (eid, gate, decision, ev["recommendation"], json.dumps(d.met), json.dumps(ev["missing"]), json.dumps(d.evidence), json.dumps(d.attendees), d.decided_by, d.conditions, d.risks_carried, db.now()))
    return {"engagement_id": eid, "gate": gate, "decision": decision, "engine_recommendation": ev["recommendation"], "rationale": ev["rationale"], "met": ev["met"], "total": ev["total"], "missing": ev["missing"], "decided_by": d.decided_by}
