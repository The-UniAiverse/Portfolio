"""AI Transformation, Strategy & Roadmap — use-case prioritisation + phased roadmap.
Feed it an audit result (optional) plus candidate use cases; it returns a ranked backlog and a 3-phase plan."""
from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.core import llm

router = APIRouter()

class UseCase(BaseModel):
    name: str
    value: int = Field(..., ge=1, le=5, description="business value 1-5")
    feasibility: int = Field(..., ge=1, le=5, description="data + tech readiness 1-5")
    risk: int = Field(..., ge=1, le=5, description="regulatory/operational risk 1-5 (5 = highest)")
    effort_weeks: int = Field(4, ge=1)
    function: str = "General"

class RoadmapRequest(BaseModel):
    organisation: str
    readiness_score: float | None = Field(None, description="overall score from the readiness audit")
    use_cases: list[UseCase]

def _score(u: UseCase) -> float:
    # value and feasibility up, risk down; effort lightly penalised
    return round(u.value * 2 + u.feasibility * 1.5 - u.risk * 1.2 - u.effort_weeks * 0.1, 2)

@router.post("/roadmap")
def roadmap(req: RoadmapRequest):
    ranked = sorted(req.use_cases, key=_score, reverse=True)
    backlog = [{"rank": i, "name": u.name, "function": u.function, "score": _score(u),
                "quadrant": ("Quick win" if u.value >= 3 and u.feasibility >= 4 else
                             "Strategic bet" if u.value >= 4 else
                             "Fill-in" if u.feasibility >= 4 else "Deprioritise")}
               for i, u in enumerate(ranked, 1)]
    quick = [b["name"] for b in backlog if b["quadrant"] == "Quick win"][:3]
    strategic = [b["name"] for b in backlog if b["quadrant"] == "Strategic bet"][:3]
    foundations = []
    if req.readiness_score is not None and req.readiness_score < 40:
        foundations = ["Data access + classification for chosen use cases", "Approved LLM route and AI policy",
                       "AI literacy training for affected teams"]
    phases = {
        "Phase 1 — Foundations & quick wins (0-3 months)": foundations + [f"Pilot: {q}" for q in quick],
        "Phase 2 — Scale what works (3-6 months)": [f"Productionise: {q}" for q in quick] + [f"Design: {s}" for s in strategic],
        "Phase 3 — Strategic bets & operating model (6-12 months)": [f"Deliver: {s}" for s in strategic] +
            ["MLOps + governance operating rhythm", "AI portfolio review cadence"],
    }
    text = llm.complete(
        f"Write a 150-word rationale for this AI roadmap for {req.organisation}. Readiness score: {req.readiness_score}. "
        f"Ranked backlog: {backlog}. Phases: {phases}. Plain prose.") or (
        f"The backlog for {req.organisation} is ranked by value and feasibility with risk and effort as penalties. "
        f"Quick wins ({', '.join(quick) or 'none identified'}) go first to prove value within a quarter; strategic bets "
        f"({', '.join(strategic) or 'none identified'}) follow once foundations and delivery rhythm exist.")
    return {"organisation": req.organisation, "backlog": backlog, "phases": phases, "rationale": text}
