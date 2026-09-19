"""AI Transformation, Strategy & Roadmap — end to end: intake → scored portfolio → business cases → phased roadmap → operating model → PDF/MD report."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings
from . import engine
from .schemas import StrategyRequest

router = APIRouter()

@router.get("/config")
def config(): return engine.cfg()

@router.post("/roadmap")
def roadmap(req: StrategyRequest):
    r = engine.build(req)
    md, pdf = engine.render(r)
    r["report_markdown_url"] = f"/api/strategy/report/{md}"; r["report_pdf_url"] = f"/api/strategy/report/{pdf}"
    return r

@router.get("/report/{filename}")
def get_report(filename: str):
    p = settings.outputs_dir / "strategy" / filename
    if not p.exists() or p.suffix not in {".md", ".pdf"}: raise HTTPException(404, "not found")
    return FileResponse(p)

@router.get("/sample")
def sample():
    return {"organisation": "Acme Logistics", "company_size": "medium", "top_goal": "Cut back-office cost 30% in 12 months", "readiness_score": 33,
            "use_cases": [
                {"name": "Invoice & POD document extraction", "function": "Finance", "description": "Extract fields from supplier invoices and proof-of-delivery scans", "owner": "Finance lead", "value": 4, "feasibility": 5, "strategic_fit": 4, "risk": 2, "effort_weeks": 4, "data_ready": 4, "monthly_benefit_usd": 9000},
                {"name": "Customer support assistant", "function": "Customer service", "description": "Grounded chatbot over SOPs and shipment FAQs with escalation", "owner": "CS manager", "value": 4, "feasibility": 4, "strategic_fit": 4, "risk": 3, "effort_weeks": 6, "data_ready": 3, "monthly_benefit_usd": 6000},
                {"name": "Demand forecasting for fleet planning", "function": "Operations", "description": "Weekly demand forecast per lane to plan fleet capacity", "owner": "Ops head", "value": 5, "feasibility": 2, "strategic_fit": 5, "risk": 3, "effort_weeks": 14, "data_ready": 2, "monthly_benefit_usd": 20000},
                {"name": "HR policy knowledge assistant", "function": "HR", "description": "Answer leave, travel and expense policy questions", "owner": "HR lead", "value": 2, "feasibility": 5, "strategic_fit": 2, "risk": 2, "effort_weeks": 3, "data_ready": 4, "monthly_benefit_usd": 1500},
                {"name": "Dynamic pricing engine", "function": "Sales", "description": "AI-suggested quotes per lane and customer", "owner": None, "value": 5, "feasibility": 1, "strategic_fit": 4, "risk": 5, "effort_weeks": 20, "data_ready": 1, "monthly_benefit_usd": None}]}
