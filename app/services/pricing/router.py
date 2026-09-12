from __future__ import annotations
import yaml
from fastapi import APIRouter, HTTPException
from app.core.config import settings

router = APIRouter()

def _tiers() -> dict:
    return yaml.safe_load((settings.pricing_dir / "tiers.yaml").read_text())

@router.get("/tiers")
def tiers(service: str | None = None):
    data = _tiers()
    if service:
        if service not in data["services"]:
            raise HTTPException(404, f"unknown service; choose from {list(data['services'])}")
        return {"currency_note": data["currency_note"], "service": service, **data["services"][service]}
    return data

@router.get("/quote")
def quote(service: str, tier: str, company_size: str = "small"):
    data = _tiers()
    svc = data["services"].get(service)
    if not svc or tier not in svc["tiers"]:
        raise HTTPException(404, "unknown service or tier")
    t = svc["tiers"][tier]
    mult = data["size_multiplier"].get(company_size, 1.0)
    return {"service": service, "tier": tier, "company_size": company_size, "base_price_usd": t["price_usd"],
            "quoted_price_usd": round(t["price_usd"] * mult), "includes": t["includes"], "duration": t["duration"]}

@router.get("/blueprint")
def blueprint(service: str | None = None, tier: str | None = None):
    """Engagement blueprint: phases, activities, outputs, team and deliverables per service/tier."""
    data = yaml.safe_load((settings.pricing_dir / "blueprints.yaml").read_text())
    if not service:
        return data
    svc = data["services"].get(service)
    if not svc:
        raise HTTPException(404, f"unknown service; choose from {list(data['services'])}")
    if tier:
        if tier not in svc["tiers"]:
            raise HTTPException(404, f"unknown tier; choose from {list(svc['tiers'])}")
        return {"service": service, "tier": tier, "common": data["common"], "title": svc["title"], "methodology": svc["methodology"], **svc["tiers"][tier]}
    return {"service": service, "common": data["common"], **svc}

@router.get("/proposal")
def proposal(service: str, tier: str, company_size: str = "small", client_name: str = "Client"):
    """One-call proposal skeleton: price, duration, scope, phases, deliverables, team — ready to paste into a document."""
    q = quote(service, tier, company_size)
    bp = blueprint(service, tier)
    return {"client": client_name, "service": bp["title"], "tier": tier, "methodology": bp["methodology"],
            "price_usd": q["quoted_price_usd"], "duration": q["duration"], "weeks": bp.get("weeks"),
            "team": bp.get("team"), "phases": bp.get("phases"), "deliverables": bp.get("deliverables"),
            "governance": bp["common"]["governance"], "roles": bp["common"]["roles"]}
