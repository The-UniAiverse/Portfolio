from __future__ import annotations
from pydantic import BaseModel, Field

class Override(BaseModel):
    field: str = Field(..., description="tier | contingency_pct | pattern | effort_factor")
    value: str | float
    reason: str = Field(..., min_length=5, description="Every override carries its reason; it is printed in the pack.")
    by: str = "delivery lead"

class Intake(BaseModel):
    """M1 — the engagement record. Captured once; every module reads from it."""
    client: str
    industry: str = "General"
    company_size: str = Field("medium", description="professional | startup | small | medium | large | enterprise")
    project: str
    sponsor: str = ""
    product_owner: str = ""
    problem: str = Field(..., description="The pain, in the client's words")
    success_metric: str = ""
    baseline: str = ""
    target: str = ""
    in_scope: list[str] = Field(default_factory=list)
    out_of_scope: list[str] = Field(default_factory=list)
    pattern: str | None = Field(None, description="assistant | rag | extraction | classical_ml | agent | multi_agent. Leave empty and the engine selects from the hints below.")
    answer_in_documents: bool = False
    needs_actions_in_systems: bool = False
    structured_prediction: bool = False
    extract_from_documents: bool = False
    sizing: dict[str, int] = Field(..., description="eight dimensions from /api/delivery/config, each 1..3")
    use_cases: int = Field(1, ge=1, le=30)
    integrations: int = Field(2, ge=0, le=40)
    data_sources: int = Field(3, ge=0, le=60)
    target_stage: str = Field("production", description="poc | mvp | production | scale")
    # risk pre-screen (same attributes the Governance engine uses)
    affects_individuals_rights: bool = False
    uses_biometrics_or_surveillance: bool = False
    safety_critical: bool = False
    interacts_with_public: bool = False
    generates_content: bool = True
    processes_personal_data: bool = False
    fully_automated_decisions: bool = False
    manipulative_or_social_scoring: bool = False
    writes_to_production_systems: bool = False
    jurisdictions: list[str] = Field(default_factory=lambda: ["India (DPDP)"])
    readiness_score: float | None = Field(None, ge=0, le=100, description="overall score from the Readiness Audit, if done")
    data_readiness_score: float | None = Field(None, ge=0, le=100)
    # M7
    requests_per_day: int = Field(1000, ge=0)
    model: str = "mid"
    cheap_route_share: float = Field(0.0, ge=0, le=1, description="share of requests a router can send to the cheap model")
    cache_system_prompt: bool = True
    monthly_growth_pct: float = Field(2.0, ge=0, le=20, description="compounded monthly over 36 months — 2% a month is +100% in three years")
    tokens: dict[str, int] | None = Field(None, description="override the pattern's token profile: system, context, history, question, answer, steps")
    # M8
    annual_benefit_usd: float = Field(0, ge=0)
    currency: str = "USD"
    risk_profile: str | None = Field(None, description="low | medium | high — leave empty for the engine to derive it")
    overrides: list[Override] = Field(default_factory=list)

class GateDecision(BaseModel):
    met: list[str] = Field(default_factory=list, description="criterion ids evidenced, e.g. ['G1-01','G1-03']")
    evidence: dict[str, str] = Field(default_factory=dict, description="criterion id -> link or note")
    attendees: list[str] = Field(default_factory=list)
    decided_by: str
    decision: str | None = Field(None, description="go | conditional_go | no_go | pivot — leave empty for the engine's recommendation to be recorded")
    conditions: str = ""
    risks_carried: str = ""
