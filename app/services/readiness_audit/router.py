from __future__ import annotations
import uuid
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.core.config import settings
from . import scoring, recommendations as rec, narrative, report
from .schemas import AuditRequest, AuditResult

router = APIRouter()
OUT = settings.outputs_dir / "readiness_audit"
OUT.mkdir(parents=True, exist_ok=True)

@router.get("/tiers")
def tiers():
    """Audit product tiers, question counts and benchmarks."""
    t = scoring.load_tiers()
    for tid, spec in t["tiers"].items():
        spec["question_count"] = scoring.questionnaire(tid)["question_count"]
    return t

@router.get("/framework")
def framework():
    """Framework outline: domains, capabilities, question counts per tier (for the website / proposals)."""
    bank = scoring.load_bank()
    return {"version": bank["version"], "last_reviewed": bank["last_reviewed"],
            "domains": [{"id": d["id"], "title": d["title"], "weight": d["weight"],
                         "capabilities": [{"id": c["id"], "title": c["title"], "questions": len(c["questions"])} for c in d["capabilities"]]}
                        for d in bank["domains"]],
            "industry_modules": [{"id": m["id"], "title": m["title"], "questions": len(m["questions"])} for m in bank["industry_modules"]],
            "tiers": {tid: scoring.questionnaire(tid)["question_count"] for tid in scoring.load_tiers()["tiers"]}}

@router.get("/questionnaire")
def questionnaire(tier: str = "free", industries: str = Query("", description="comma-separated industry module ids")):
    try:
        return scoring.questionnaire(tier, [i for i in industries.split(",") if i])
    except ValueError as e:
        raise HTTPException(400, str(e))

def run_audit(req: AuditRequest) -> AuditResult:
    try:
        qn = scoring.questionnaire(req.tier, req.industries)
    except ValueError as e:
        raise HTTPException(400, str(e))
    valid = {q["id"] for d in qn["domains"] for c in d["capabilities"] for q in c["questions"]} | \
            {q["id"] for m in qn["industry_modules"] for q in m["questions"]}
    bad = [k for k, v in req.answers.items() if k not in valid or not 0 <= v <= 4]
    if bad:
        raise HTTPException(400, f"Invalid answers for tier '{req.tier}': {bad[:10]}")
    tier_spec = qn["tier_info"]; feats = tier_spec["features"]
    dims, modules, flags = scoring.score(qn, req.answers)
    total = scoring.overall(dims)
    level, summary = scoring.band(qn["maturity_bands"], total)
    recs = rec.recommend(dims, feats["recommendations"])
    bench = scoring.load_tiers()["benchmarks"].get(req.organisation.size) if feats["benchmark"] else None
    hint = None
    if req.tier == "free":
        hint = ("This free snapshot covers 25 of 348 framework questions. A Bronze audit adds 60 questions, capability-level "
                "recommendations and a PDF report; Silver and above add interviews, benchmarks and industry modules.")
    result = AuditResult(audit_id=uuid.uuid4().hex[:10], framework_version=qn["version"], tier=req.tier,
                         organisation=req.organisation, question_count=qn["question_count"], answered_count=len(req.answers),
                         overall_score=total, maturity_level=level, maturity_summary=summary, benchmark=bench,
                         red_flags=flags, dimensions=dims, industry_modules=modules, recommendations=recs,
                         roadmap=rec.roadmap(recs), narrative="", narrative_source="rules", upgrade_hint=hint)
    result.narrative, result.narrative_source = narrative.build(result)
    return result

@router.post("/run", response_model=AuditResult)
def run(req: AuditRequest):
    result = run_audit(req)
    base = OUT / result.audit_id
    base.with_suffix(".json").write_text(result.model_dump_json(indent=2))
    base.with_suffix(".md").write_text(report.to_markdown(result))
    result.report_markdown_url = f"/api/readiness_audit/report/{result.audit_id}.md"
    if result.tier != "free":
        report.to_pdf(result, base.with_suffix(".pdf"))
        result.report_pdf_url = f"/api/readiness_audit/report/{result.audit_id}.pdf"
    return result

@router.get("/report/{filename}")
def get_report(filename: str):
    p = OUT / filename
    if not p.exists() or p.suffix not in {".md", ".pdf", ".json"}:
        raise HTTPException(404, "report not found")
    return FileResponse(p)

@router.get("/sample")
def sample(tier: str = "bronze", industries: str = ""):
    """Deterministic demo answers for any tier — pattern: realistic SMB (weak governance/finance, mid platform)."""
    qn = scoring.questionnaire(tier, [i for i in industries.split(",") if i])
    profile = {"strategy": 2, "value": 2, "data": 1, "platform": 2, "genai": 1, "people": 1, "delivery": 1, "governance": 0, "security": 1, "finance": 1}
    answers = {}
    for d in qn["domains"]:
        for c in d["capabilities"]:
            for i, q in enumerate(c["questions"]):
                answers[q["id"]] = max(0, min(4, profile[d["id"]] + ((i + 1) % 3) - 1))
    for m in qn["industry_modules"]:
        for i, q in enumerate(m["questions"]):
            answers[q["id"]] = (i % 3)
    return {"tier": tier, "industries": [i for i in industries.split(",") if i],
            "organisation": {"name": "Acme Logistics", "industry": "Logistics", "size": "medium",
                             "top_goal": "Cut back-office processing cost by 30% within a year"}, "answers": answers}
