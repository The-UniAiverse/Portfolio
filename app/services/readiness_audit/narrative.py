"""Executive narrative: LLM if configured, otherwise a solid templated summary."""
from __future__ import annotations
from app.core import llm
from .schemas import AuditResult

def _rules(r: AuditResult) -> str:
    dims = sorted(r.dimensions, key=lambda d: d.score)
    weakest, strongest = dims[0], dims[-1]
    top3 = "; ".join(x.action for x in r.recommendations[:3])
    return (
        f"{r.organisation.name} scores {r.overall_score}/100 — maturity level '{r.maturity_level}'. "
        f"{r.maturity_summary} The strongest area is {strongest.title} ({strongest.score}); "
        f"the biggest constraint is {weakest.title} ({weakest.score}). "
        f"Over the next 90 days the priorities are: {top3}. "
        "Closing the weakest dimension first unlocks the others: AI value scales only as fast as "
        "the slowest of strategy, data, technology, people, process and governance."
    )

def build(r: AuditResult) -> tuple[str, str]:
    prompt = (
        "Write a 180-220 word executive summary of this AI readiness audit for the client's leadership. "
        "Structure: current state (1 para), what is holding them back (1 para), the 90-day plan (1 para). "
        "Plain language, specific, no bullet points.\n\n"
        f"Organisation: {r.organisation.model_dump()}\n"
        f"Overall: {r.overall_score} ({r.maturity_level}: {r.maturity_summary})\n"
        f"Dimensions: {[(d.title, d.score, d.gaps) for d in r.dimensions]}\n"
        f"Top recommendations: {[(x.horizon, x.action) for x in r.recommendations[:6]]}"
    )
    text = llm.complete(prompt)
    if text:
        return text.strip(), "llm"
    return _rules(r), "rules"
