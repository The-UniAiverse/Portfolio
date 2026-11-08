from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field, field_validator
from app.core.llm import Mode

SLUG = r"^[a-z0-9][a-z0-9-]{0,199}$"


class Education(BaseModel):
    degree: str = Field(..., min_length=1, max_length=120)
    institution: str = Field("", max_length=120)
    period: str = Field("", max_length=40, description="e.g. 2022-2026 or 'final year'")


class Language(BaseModel):
    language: str = Field(..., min_length=1, max_length=40)
    level: str = Field("", max_length=40, description="Native, fluent, conversational, B2…")


class WorkEntry(BaseModel):
    """One role, shaped after upstream's "Professional Experience" section."""
    title: str = Field(..., min_length=1, max_length=100)
    company: str = Field("", max_length=100)
    period: str = Field("", max_length=40, description="e.g. 2021-2024 or 2023-present")
    highlights: str = Field("", max_length=800, description="What you did and achieved")


class CandidateProfile(BaseModel):
    """A job seeker's profile at any career stage, shaped after upstream's 01-candidate-profile.md. Not stored."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field("", max_length=120)
    phone: str = Field("", max_length=40)
    link: str = Field("", max_length=200, description="LinkedIn, GitHub or portfolio URL")
    city: str = Field("", max_length=80)
    open_to_relocation: bool = False
    current_title: str = Field("", max_length=100, description="Current or most recent job title")
    years_experience: float | None = Field(None, ge=0, le=60, description="Total years of professional experience")
    work_history: list[WorkEntry] = Field(default_factory=list, max_length=6)
    education: list[Education] = Field(default_factory=list, max_length=5)
    skills: list[str] = Field(default_factory=list, max_length=40)
    experience: str = Field("", max_length=3000, description="Projects, internships, certifications, other achievements — free text")
    target_roles: list[str] = Field(default_factory=list, max_length=8)
    career_goals: str = Field("", max_length=600)
    languages: list[Language] = Field(default_factory=list, max_length=8)

    @field_validator("skills", "target_roles")
    @classmethod
    def _short_items(cls, v: list[str]) -> list[str]:
        v = [x.strip() for x in v if x.strip()]
        if any(len(x) > 60 for x in v):
            raise ValueError("each item must be 60 characters or fewer")
        return v


class MatchRequest(BaseModel):
    profile: CandidateProfile
    job_id: str = Field(..., pattern=SLUG)
    mode: Mode = "rules"


class CoverLetterRequest(BaseModel):
    profile: CandidateProfile
    job_id: str = Field(..., pattern=SLUG)
    notes: str = Field("", max_length=600, description="Anything the candidate wants emphasised")


class Letter(BaseModel):
    salutation: str = Field(..., min_length=1, max_length=120)
    paragraphs_before_bullets: list[str] = Field(..., min_length=1, max_length=4)
    bullets: list[str] = Field(default_factory=list, max_length=6)
    paragraphs_after_bullets: list[str] = Field(default_factory=list, max_length=4)
    sign_off: str = Field("Kind regards,", max_length=60)

    @field_validator("paragraphs_before_bullets", "bullets", "paragraphs_after_bullets")
    @classmethod
    def _bounded(cls, v: list[str]) -> list[str]:
        if any(len(x) > 1500 for x in v):
            raise ValueError("paragraph too long")
        return v


class LetterPdfRequest(BaseModel):
    """Re-render a (possibly edited) letter to PDF. No AI involved."""
    profile: CandidateProfile
    letter: Letter


GateVerdict = Literal["PASS", "FAIL", "FLAG"]
