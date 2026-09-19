from __future__ import annotations
from pydantic import BaseModel, Field

class UseCase(BaseModel):
    name: str
    function: str = "General"
    description: str = ""
    owner: str | None = None
    value: int = Field(3, ge=1, le=5, description="business value 1-5")
    feasibility: int = Field(3, ge=1, le=5, description="data + tech + skills readiness 1-5")
    strategic_fit: int = Field(3, ge=1, le=5)
    risk: int = Field(2, ge=1, le=5, description="regulatory / people / operational risk (5 = highest)")
    effort_weeks: int = Field(6, ge=1, le=52)
    data_ready: int = Field(3, ge=1, le=5)
    monthly_benefit_usd: float | None = Field(None, description="quantified monthly benefit if known")

class StrategyRequest(BaseModel):
    organisation: str
    company_size: str = "medium"
    top_goal: str = ""
    readiness_score: float | None = Field(None, description="overall score from the AI Readiness Audit")
    use_cases: list[UseCase]
