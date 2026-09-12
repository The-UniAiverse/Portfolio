"""Executive narrative: LLM if configured, otherwise a templated summary. Never blocks a deliverable."""
from __future__ import annotations
from app.core import llm
from .schemas import AuditResult

def _rules(r: AuditResult) -> str:
    dims = sorted(r.dimensions, key=lambda d: d.score)
    weakest, strongest = dims[0], dims[-1]
    caps = sorted((c for d in r.dimensions for c in d.capabilities), key=lambda c: c.score)[:3]
    top = "; ".join(f"{c.title.lower()} ({c.score})" for c in caps)
    bench = (f" Against the {r.organisation.size}-company benchmark of {r.benchmark['overall']}, "
             f"{r.organisation.name} is {'ahead' if r.overall_score >= r.benchmark['overall'] else 'behind'}.") if r.benchmark else ""
    flags = f" {len(r.red_flags)} critical controls are absent and should be treated as immediate priorities." if r.red_flags else ""
    return (f"{r.organisation.name} scores {r.overall_score}/100 on the uniAIverse AI Readiness Framework v{r.framework_version} "
            f"({r.tier} audit, {r.answered_count} questions), placing it at the '{r.maturity_level}' level. {r.maturity_summary}{bench} "
            f"The strongest domain is {strongest.title} ({strongest.score}); the weakest is {weakest.title} ({weakest.score}). "
            f"The lowest-scoring capabilities — {top} — are where the first 90 days should focus.{flags} "
            "AI value scales only as fast as the weakest of strategy, data, platform, skills, delivery and governance; "
            "closing these gaps in order unlocks the rest of the portfolio.")

def build(r: AuditResult) -> tuple[str, str]:
    prompt = ("Write a 200-250 word executive summary of this AI readiness audit for the client's leadership. "
              "Three paragraphs: current state, what is holding them back, the 90-day plan. Plain, specific, no bullets.\n\n"
              f"Organisation: {r.organisation.model_dump()}\nTier: {r.tier}. Overall: {r.overall_score} ({r.maturity_level}).\n"
              f"Benchmark: {r.benchmark}\nRed flags: {r.red_flags}\n"
              f"Domains: {[(d.title, d.score) for d in r.dimensions]}\n"
              f"Weakest capabilities: {[(c.title, c.score) for d in r.dimensions for c in d.capabilities if c.score < 40][:8]}\n"
              f"Top actions: {[(x.horizon, x.action) for x in r.recommendations[:6]]}")
    text = llm.complete(prompt)
    return (text.strip(), "llm") if text else (_rules(r), "rules")
