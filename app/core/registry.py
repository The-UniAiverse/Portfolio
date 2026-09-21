"""Service registry — the ONE place to add or remove a service.

To add a new service:
  1. create app/services/<id>/router.py exposing `router = APIRouter()`
  2. add a ServiceSpec below
  3. add <id> to ENABLED_SERVICES in .env
Nothing else needs to change.
"""
from __future__ import annotations
from dataclasses import dataclass
from importlib import import_module

@dataclass(frozen=True)
class ServiceSpec:
    id: str
    title: str
    owner: str
    priority: int          # from the Role & Task Ownership doc
    module: str            # dotted path to the router module
    status: str            # "ready" | "beta" | "planned"

SERVICES: list[ServiceSpec] = [
    ServiceSpec("readiness_audit", "AI Readiness Audit", "Sarfi", 1, "app.services.readiness_audit.router", "ready"),
    ServiceSpec("training",        "Training & Mentorship", "Sarfi", 2, "app.services.training.router", "ready"),
    ServiceSpec("strategy",        "AI Transformation, Strategy & Roadmap", "Sarfi", 3, "app.services.strategy.router", "ready"),
    ServiceSpec("governance",      "AI Governance, Safety & Compliance", "Sarfi", 3, "app.services.governance.router", "ready"),
    ServiceSpec("automation",      "AI Automation & Workflow Optimisation", "Sarfi", 4, "app.services.automation.router", "ready"),
    ServiceSpec("pricing",         "Service Tiers & Pricing", "Sarfi", 0, "app.services.pricing.router", "ready"),
    ServiceSpec("quest",           "uniAI Quest — Interview Playground & Knowledge Hub", "Sarfi", 2, "app.services.quest.router", "ready"),
    ServiceSpec("bot",             "uniAI website assistant", "Harsh", 0, "app.services.bot.router", "ready"),
    ServiceSpec("demos",           "Demo Hub — runnable demos for the website", "Sarfi", 0, "app.services.demos.router", "ready"),
    ServiceSpec("discovery",       "Discovery kit — enquiry → discovery questions document", "Sarfi", 0, "app.services.discovery.router", "ready"),
    ServiceSpec("delivery",        "AI Delivery Framework — tiered estimates, costs, governance, security, gates and document packs", "Sarfi", 1, "app.services.delivery.router", "ready"),
    ServiceSpec("payments",        "Payments (Razorpay: cards, UPI < limit, netbanking, NEFT/RTGS/IMPS)", "Sarfi", 0, "app.services.payments.router", "ready"),
]

def load(enabled: list[str]):
    """Yield (spec, router) for every enabled service."""
    for spec in SERVICES:
        if spec.id in enabled:
            yield spec, import_module(spec.module).router
