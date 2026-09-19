"""AI Governance, Safety & Compliance — inventory → risk tiers → control gaps → maturity → policy → remediation → PDF."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings
from . import engine
from .engine import GovernanceRequest, AISystem

router = APIRouter()

@router.get("/library")
def library(): return engine.library()

@router.post("/classify")
def classify(s: AISystem):
    """Quick single-system classification (used by the website calculator)."""
    tier = engine.classify(s); lib = engine.library()
    return {"system": s.name, "risk_tier": tier, "label": lib["risk_tiers"][tier]["label"],
            "required_controls": [c for c in lib["controls"] if tier in c["tiers"]] if tier != "prohibited" else [], "note": "Framework-aligned guidance, not legal advice."}

@router.post("/assess")
def assess(req: GovernanceRequest): return engine.run(req)

@router.get("/report/{filename}")
def report(filename: str):
    p = settings.outputs_dir / "governance" / filename
    if not p.exists() or p.suffix not in {".md", ".pdf"}: raise HTTPException(404, "not found")
    return FileResponse(p)

@router.get("/sample")
def sample():
    return GovernanceRequest(organisation="Acme Logistics", industry="Logistics", size="medium", policy_owner="Head of Compliance",
        gap_answers={"policy": 0, "inventory": 1, "classification": 0, "review_board": 0, "evaluation": 1, "monitoring": 1, "privacy": 2, "security": 1, "training": 1, "audit": 0},
        systems=[AISystem(name="Customer status chatbot", owner="CS lead", purpose="Answer shipment status queries", vendor_or_model="Claude via API + RAG", data_used="Shipment data, customer names", users_affected="Customers",
                          interacts_with_public=True, processes_personal_data=True, controls_in_place=["C01", "C03"]),
                 AISystem(name="CV screening assistant", owner="HR", purpose="Rank applicants", vendor_or_model="Vendor SaaS", data_used="CVs", users_affected="Job applicants", status="pilot",
                          affects_individuals_rights=True, processes_personal_data=True, fully_automated_decisions=False, controls_in_place=["C01"]),
                 AISystem(name="Invoice extraction", owner="Finance", purpose="Extract fields from supplier invoices", vendor_or_model="Document AI", data_used="Supplier invoices", users_affected="Finance staff", controls_in_place=["C01", "C02", "C03", "C17"]),
                 AISystem(name="Marketing copy generator", owner="Marketing", purpose="Draft campaign copy", vendor_or_model="ChatGPT Team", data_used="Product info", users_affected="Public (content)", generates_content=True),
                 AISystem(name="Driver behaviour scoring", owner="Ops", purpose="Score drivers for incentives", vendor_or_model="In-house ML", data_used="Telematics, driver IDs", users_affected="Employees", status="idea",
                          affects_individuals_rights=True, processes_personal_data=True, fully_automated_decisions=True)]).model_dump()
