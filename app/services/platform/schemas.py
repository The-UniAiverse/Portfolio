from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field

class Register(BaseModel):
    """A visitor asks for access. Nothing is provisioned until an admin approves."""
    organisation: str = Field(..., min_length=2, max_length=120)
    contact_name: str = Field(..., min_length=2, max_length=80)
    contact_email: EmailStr
    requested_plan: str = Field("free", description="free | bronze | silver | gold")
    purpose: str = Field("", max_length=600, description="What they want to do — admins read this before approving")

class Approve(BaseModel):
    plan: str | None = Field(None, description="plan to assign; defaults to the requested plan")
    note: str = ""
    decided_by: str = "admin"

class Limits(BaseModel):
    """Override any limit of the plan for one tenant, without a redeploy. Only known keys are accepted."""
    users: int | None = None; concurrency: int | None = None; monthly_queries: int | None = None; daily_queries: int | None = None
    max_context_tokens: int | None = None; storage_gb: float | None = None; vector_gb: float | None = None; knowledge_bases: int | None = None
    agent_max_tool_calls: int | None = None; doc_generation_per_month: int | None = None; monthly_spend_limit_inr: float | None = None
    per_user_daily_queries: int | None = None; per_user_cohort_queries: int | None = None; per_user_spend_limit_inr: float | None = None; max_output_tokens: int | None = None
    capabilities_add: list[str] = Field(default_factory=list); capabilities_remove: list[str] = Field(default_factory=list)
    reason: str = Field(..., min_length=5); by: str = "admin"

class Check(BaseModel):
    capability: str
    units: int | None = None
    user_email: str | None = None
