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
