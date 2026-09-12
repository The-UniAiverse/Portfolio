"""Capability-level recommendations. Remediation text lives in question_bank.yaml (low_action / mid_action)."""
from __future__ import annotations
from .schemas import DimensionResult, Recommendation

HORIZONS = ["30 days", "60 days", "90 days", "6 months"]

def recommend(dims: list[DimensionResult], limit: int) -> list[Recommendation]:
    recs = []
    for d in dims:
        for c in d.capabilities:
            gap = 100 - c.score
            if c.score < 40:
                action, horizon = c.low_action, "30 days" if c.score < 20 else "60 days"
            elif c.score <= 70:
                action, horizon = c.mid_action, "90 days"
            else:
                action, horizon = f"Sustain and optimise: review {c.title.lower()} quarterly and share practices across teams.", "6 months"
            recs.append(Recommendation(priority=0, domain=d.title, capability=c.title, action=action,
                                       horizon=horizon, impact=round(d.weight * gap, 2)))
    recs.sort(key=lambda r: (HORIZONS.index(r.horizon), -r.impact))
    recs = recs[:limit]
    for i, r in enumerate(recs, 1):
        r.priority = i
    return recs

def roadmap(recs: list[Recommendation]) -> dict[str, list[str]]:
    out = {h: [f"[{r.domain} › {r.capability}] {r.action}" for r in recs if r.horizon == h] for h in HORIZONS}
    return {k: v for k, v in out.items() if v}
