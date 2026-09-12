"""AI Automation & Workflow Optimisation — workflow inventory scoring + ROI calculator."""
from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

class Workflow(BaseModel):
    name: str
    volume_per_month: int = Field(..., ge=1)
    minutes_per_item: float = Field(..., ge=0.1)
    people_involved: int = Field(1, ge=1)
    hourly_cost: float = Field(25.0, description="fully loaded cost per hour, in your currency")
    error_rate_pct: float = Field(2.0, ge=0, le=100)
    cost_per_error: float = Field(20.0, ge=0)
    automation_potential_pct: float = Field(60.0, ge=0, le=100, description="share of the work AI can absorb")
    rule_based: bool = Field(False, description="True if steps are deterministic (RPA/scripts fit)")
    needs_judgement: bool = Field(True, description="True if reading/writing/deciding is involved (LLM fit)")

class ROIRequest(BaseModel):
    currency: str = "USD"
    build_cost: float = Field(15000, description="one-off implementation cost")
    monthly_run_cost: float = Field(300, description="LLM/API + hosting per month")
    workflows: list[Workflow]

@router.post("/roi")
def roi(req: ROIRequest):
    rows, total_saving = [], 0.0
    for w in req.workflows:
        hours = w.volume_per_month * w.minutes_per_item / 60
        labour = hours * w.hourly_cost
        errors = w.volume_per_month * w.error_rate_pct / 100 * w.cost_per_error
        saving = (labour + errors) * w.automation_potential_pct / 100
        total_saving += saving
        approach = ("LLM agent / GenAI workflow" if w.needs_judgement and not w.rule_based else
                    "RPA / scripted automation" if w.rule_based and not w.needs_judgement else
                    "Hybrid: scripts + LLM for judgement steps")
        rows.append({"workflow": w.name, "hours_per_month": round(hours, 1), "labour_cost": round(labour, 2),
                     "error_cost": round(errors, 2), "monthly_saving": round(saving, 2), "recommended_approach": approach,
                     "priority_score": round(saving / max(1, w.people_involved), 1)})
    rows.sort(key=lambda r: r["monthly_saving"], reverse=True)
    net = total_saving - req.monthly_run_cost
    payback = round(req.build_cost / net, 1) if net > 0 else None
    return {"currency": req.currency, "workflows": rows, "total_monthly_saving": round(total_saving, 2),
            "net_monthly_benefit": round(net, 2), "payback_months": payback,
            "year_one_roi_pct": round(100 * (net * 12 - req.build_cost) / req.build_cost, 1) if req.build_cost else None}
