"""AI Governance, Safety & Compliance — use-case risk classification + control checklist.
Tiers mirror the EU AI Act structure (prohibited / high / limited / minimal). This is guidance, not legal advice."""
from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RiskInput(BaseModel):
    use_case: str
    affects_individuals_rights: bool = False   # employment, credit, education, access to services
    uses_biometrics_or_surveillance: bool = False
    safety_critical: bool = False              # medical, transport, infrastructure
    interacts_with_public: bool = False        # chatbots, generated content
    processes_personal_data: bool = False
    fully_automated_decisions: bool = False
    manipulative_or_social_scoring: bool = False

CONTROLS = {
    "prohibited": ["Do not deploy. Redesign the use case or drop it."],
    "high": ["Risk management system & documented risk assessment", "Data governance: quality, bias testing, provenance",
             "Technical documentation and logging / audit trail", "Human oversight with ability to override",
             "Accuracy, robustness and cybersecurity testing", "Pre-deployment review sign-off (Compliance + Engineering)",
             "Post-market monitoring and incident reporting"],
    "limited": ["Transparency: tell users they are interacting with AI / content is AI-generated",
                "Grounding + citations for any factual assistant", "Escalation path to a human",
                "Basic monitoring: refusal rate, complaints, drift"],
    "minimal": ["Inventory entry (system, owner, purpose, data used)", "Follow company responsible-AI policy",
                "Periodic review (annual)"],
}

@router.post("/classify")
def classify(x: RiskInput):
    if x.manipulative_or_social_scoring:
        tier = "prohibited"
    elif x.affects_individuals_rights or x.uses_biometrics_or_surveillance or x.safety_critical or (
            x.fully_automated_decisions and x.processes_personal_data):
        tier = "high"
    elif x.interacts_with_public:
        tier = "limited"
    else:
        tier = "minimal"
    extras = []
    if x.processes_personal_data:
        extras += ["DPIA / privacy assessment", "PII redaction at ingestion and on outputs", "Retention & deletion propagation"]
    return {"use_case": x.use_case, "risk_tier": tier, "controls": CONTROLS[tier] + extras,
            "note": "Framework-aligned guidance (EU AI Act structure, NIST AI RMF). Not legal advice."}

@router.get("/policy-template")
def policy_template():
    return {"title": "Responsible AI Policy (one page)", "sections": [
        "Purpose and scope", "Approved AI tools and how to request new ones",
        "Data you may / may not put into AI tools (classification table)",
        "Required review before any AI system reaches customers or affects staff",
        "Transparency: disclosure of AI use", "Human oversight and escalation",
        "Incident reporting", "Roles: policy owner, reviewers, system owners", "Review cadence"]}
