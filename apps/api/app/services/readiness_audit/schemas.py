from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field, field_validator
from app.core.llm import Mode

CompanySize = Literal["small", "medium", "large", "enterprise"]

class Organisation(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, examples=["Acme Logistics"])
    industry: str = Field("General", max_length=80, examples=["Logistics"])
    size: CompanySize = Field("small", description="small (<50) | medium (50-250) | large (250-1000) | enterprise (1000+)")
    contact: str | None = Field(None, max_length=200)
    top_goal: str | None = Field(None, max_length=500, description="One sentence: what does leadership want from AI?")

class AuditRequest(BaseModel):
    organisation: Organisation
    answers: dict[str, int] = Field(..., description="question_id -> score 0..4")
    notes: dict[str, str] = Field(default_factory=dict, description="optional free text per question_id")
    mode: Mode = Field("auto", description="rules = deterministic only · ai = require the configured LLM · auto = LLM if configured")

    @field_validator("answers")
    @classmethod
    def _answers_bounded(cls, v: dict[str, int]) -> dict[str, int]:
        if len(v) > 200:
            raise ValueError("too many answers")
        return v

    @field_validator("notes")
    @classmethod
    def _notes_bounded(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) > 200 or any(len(x) > 2000 for x in v.values()):
            raise ValueError("notes too long (max 200 entries, 2000 characters each)")
        return v

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
    narrative_notice: str | None = None  # set when AI was requested but rules text was returned
    mode: Mode = "auto"
    report_markdown_url: str | None = None
    report_pdf_url: str | None = None
