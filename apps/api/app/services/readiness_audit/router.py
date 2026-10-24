from __future__ import annotations
import json, uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings
from . import scoring, recommendations as rec, narrative, report
from .schemas import AuditRequest, AuditResult

router = APIRouter()
OUT = settings.outputs_dir / "readiness_audit"
OUT.mkdir(parents=True, exist_ok=True)

@router.get("/questionnaire")
def questionnaire():
    """Questions, scale and dimensions — the frontend renders straight from this."""
    return scoring.load_questionnaire()

def run_audit(req: AuditRequest) -> AuditResult:
    q = scoring.load_questionnaire()
    valid = {x["id"] for d in q["dimensions"] for x in d["questions"]}
    bad = [k for k, v in req.answers.items() if k not in valid or not 0 <= v <= 4]
    if bad:
        raise HTTPException(400, f"Invalid answers: {bad}")
    dims = scoring.score_dimensions(q, req.answers)
    total = scoring.overall(dims)
    level, summary = scoring.band(q, total)
    recs = rec.recommend(dims)
    result = AuditResult(
        audit_id=uuid.uuid4().hex[:10], organisation=req.organisation, overall_score=total,
        maturity_level=level, maturity_summary=summary, dimensions=dims,
        recommendations=recs, roadmap=rec.roadmap(recs), narrative="", narrative_source="rules",
    )
    result.narrative, result.narrative_source = narrative.build(result)
    return result

@router.post("/run", response_model=AuditResult)
def run(req: AuditRequest):
    """Score the answers, generate recommendations, roadmap, narrative, and write MD + PDF reports."""
    result = run_audit(req)
    base = OUT / result.audit_id
    (base.with_suffix(".md")).write_text(report.to_markdown(result))
    report.to_pdf(result, base.with_suffix(".pdf"))
    (base.with_suffix(".json")).write_text(result.model_dump_json(indent=2))
    result.report_markdown_url = f"/api/readiness_audit/report/{result.audit_id}.md"
    result.report_pdf_url = f"/api/readiness_audit/report/{result.audit_id}.pdf"
    return result

@router.get("/report/{filename}")
def get_report(filename: str):
    p = OUT / filename
    if not p.exists() or p.suffix not in {".md", ".pdf", ".json"}:
        raise HTTPException(404, "report not found")
    return FileResponse(p)

@router.get("/sample")
def sample():
    """A ready-made request body for demos and tests."""
    q = scoring.load_questionnaire()
    demo = {"s1": 1, "s2": 2, "s3": 1, "s4": 0, "s5": 1, "d1": 2, "d2": 1, "d3": 1, "d4": 2, "d5": 2,
            "t1": 2, "t2": 3, "t3": 1, "t4": 0, "t5": 2, "p1": 1, "p2": 2, "p3": 0, "p4": 1, "p5": 1,
            "o1": 2, "o2": 1, "o3": 1, "o4": 2, "o5": 1, "g1": 0, "g2": 0, "g3": 1, "g4": 0, "g5": 1}
    return {"organisation": {"name": "Acme Logistics", "industry": "Logistics", "size": "medium",
                             "top_goal": "Cut back-office processing cost by 30% within a year"},
            "answers": {k: v for k, v in demo.items() if k in {x["id"] for d in q["dimensions"] for x in d["questions"]}}}
