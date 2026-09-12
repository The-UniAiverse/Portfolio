from __future__ import annotations
from pydantic import BaseModel, Field

class Organisation(BaseModel):
    name: str = Field(..., examples=["Acme Logistics"])
    industry: str = Field("General")
    size: str = Field("small", description="small (<50) | medium (50-250) | large (250-1000) | enterprise (1000+)")
    contact: str | None = None
    top_goal: str | None = Field(None, description="One sentence: what does leadership want from AI?")

class AuditRequest(BaseModel):
    tier: str = Field("free", description="free | bronze | silver | gold | platinum")
    industries: list[str] = Field(default_factory=list, description="industry module ids (silver+)")
    organisation: Organisation
    answers: dict[str, int] = Field(..., description="question_id -> score 0..4")
    notes: dict[str, str] = Field(default_factory=dict)

class CapabilityResult(BaseModel):
    id: str
    title: str
    score: float
    answered: int
    total: int
    strengths: list[str]
    gaps: list[str]
    evidence_missing: list[str]
    low_action: str
    mid_action: str

class DimensionResult(BaseModel):
    id: str
    title: str
    weight: float
    score: float
    answered: int
    total: int
    capabilities: list[CapabilityResult]

class Recommendation(BaseModel):
    priority: int
    domain: str
    capability: str
    action: str
    horizon: str
    impact: float = Field(..., description="domain weight × gap — used for ordering")

class AuditResult(BaseModel):
    audit_id: str
    framework_version: str
    tier: str
    organisation: Organisation
    question_count: int
    answered_count: int
    overall_score: float
    maturity_level: str
    maturity_summary: str
    benchmark: dict | None = None
    red_flags: list[str]
    dimensions: list[DimensionResult]
    industry_modules: list[dict]
    recommendations: list[Recommendation]
    roadmap: dict[str, list[str]]
    narrative: str
    narrative_source: str
    upgrade_hint: str | None = None
    report_markdown_url: str | None = None
    report_pdf_url: str | None = None
