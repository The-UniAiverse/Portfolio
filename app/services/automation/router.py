"""AI Automation & Workflow Optimisation — inventory → ROI → approach → current/future state → implementation plan → PDF."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings
from . import engine
from .engine import AutomationRequest, Workflow, Step

router = APIRouter()

@router.get("/playbook")
def playbook(): return engine.playbook()

@router.post("/assess")
def assess(req: AutomationRequest): return engine.run(req)

@router.post("/roi")
def roi(req: AutomationRequest):
    """Quick numbers only (website calculator) — no report files."""
    a = engine.analyse(req); return {"workflows": a["workflows"], "totals": a["totals"]}

@router.get("/report/{filename}")
def report(filename: str):
    p = settings.outputs_dir / "automation" / filename
    if not p.exists() or p.suffix not in {".md", ".pdf"}: raise HTTPException(404, "not found")
    return FileResponse(p)

@router.get("/sample")
def sample():
    return AutomationRequest(organisation="Acme Logistics", industry="Logistics", workflows=[
        Workflow(name="Supplier invoice processing", function="Finance", owner="AP lead", trigger="Invoice email", volume_per_month=2200, minutes_per_item=7, people_involved=3, hourly_cost=22, error_rate_pct=4, cost_per_error=35, turnaround_hours=72, rule_based=False, needs_judgement=True, data_access="api",
                 steps=[Step(name="Receive invoice email", kind="receive", minutes=0.5), Step(name="Read and key fields", kind="read", minutes=3), Step(name="Match to PO in ERP", kind="lookup", minutes=1.5, system="ERP"), Step(name="Decide on mismatch", kind="decide", minutes=1), Step(name="Post to ERP", kind="update", minutes=0.5, system="ERP"), Step(name="Notify supplier", kind="notify", minutes=0.5)]),
        Workflow(name="Delivery exception emails", function="Customer service", owner="CS lead", trigger="Carrier exception", volume_per_month=1500, minutes_per_item=9, people_involved=4, hourly_cost=18, error_rate_pct=3, cost_per_error=25, turnaround_hours=6, needs_judgement=True, multi_step=True, cross_system=True, data_access="api",
                 steps=[Step(name="Read exception", kind="read", minutes=2), Step(name="Look up shipment + customer", kind="lookup", minutes=2, system="TMS/CRM"), Step(name="Decide action", kind="decide", minutes=2), Step(name="Write customer email", kind="write", minutes=2), Step(name="Update TMS", kind="update", minutes=1, system="TMS")]),
        Workflow(name="Driver onboarding documents", function="HR", owner="HR ops", trigger="New hire", volume_per_month=60, minutes_per_item=45, people_involved=1, hourly_cost=20, error_rate_pct=5, cost_per_error=80, turnaround_hours=96, needs_judgement=True, data_access="export"),
        Workflow(name="Weekly KPI report compilation", function="Operations", owner="Ops analyst", trigger="Monday", volume_per_month=4, minutes_per_item=240, people_involved=1, hourly_cost=30, error_rate_pct=10, cost_per_error=50, turnaround_hours=24, rule_based=True, needs_judgement=False, data_access="api"),
        Workflow(name="Ad-hoc customs queries", function="Compliance", owner="Customs lead", trigger="Email", volume_per_month=12, minutes_per_item=60, people_involved=1, hourly_cost=35, error_rate_pct=2, cost_per_error=500, turnaround_hours=48, needs_judgement=True, data_access="none")]).model_dump()
