from __future__ import annotations
from pydantic import BaseModel, Field

class Organisation(BaseModel):
    name: str = Field(..., examples=["Acme Logistics"])
    industry: str = Field("General", examples=["Logistics"])
    size: str = Field("small", description="small (<50) | medium (50-250) | large (250-1000) | enterprise (1000+)")
    contact: str | None = None
    top_goal: str | None = Field(None, description="One sentence: what does leadership want from AI?")

class AuditRequest(BaseModel):
    organisation: Organisation
    answers: dict[str, int] = Field(..., description="question_id -> score 0..4")
    notes: dict[str, str] = Field(default_factory=dict, description="optional free text per question_id")

class DimensionResult(BaseModel):
    id: str
    title: str
    weight: float
    score: float           # 0-100
    answered: int
    total: int
    strengths: list[str]
    gaps: list[str]

class Recommendation(BaseModel):
    priority: int
    dimension: str
    action: str
    why: str
    horizon: str           # "30 days" | "60 days" | "90 days" | "6 months"
    owner_hint: str

class AuditResult(BaseModel):
    audit_id: str
    organisation: Organisation
    overall_score: float
    maturity_level: str
    maturity_summary: str
    dimensions: list[DimensionResult]
    recommendations: list[Recommendation]
    roadmap: dict[str, list[str]]   # "30 days" -> actions
    narrative: str
    narrative_source: str           # "llm" | "rules"
    report_markdown_url: str | None = None
    report_pdf_url: str | None = None
