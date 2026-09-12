"""Rule-based recommendation engine. Deterministic, explainable, editable.

PLAYBOOK maps dimension -> band -> list of (action, why, horizon, owner_hint).
Bands: "low" (<40), "mid" (40-70), "high" (>70).
"""
from __future__ import annotations
from .schemas import DimensionResult, Recommendation

PLAYBOOK: dict[str, dict[str, list[tuple[str, str, str, str]]]] = {
    "strategy": {
        "low": [
            ("Run a 2-hour leadership AI alignment workshop and agree 3 business outcomes AI must serve",
             "Without leadership-owned outcomes, pilots stay pilots.", "30 days", "CEO / COO + uniAIverse"),
            ("Name a single accountable AI sponsor with a ring-fenced budget line",
             "Ownership is the strongest predictor of AI pilots reaching production.", "30 days", "CEO"),
            ("Build a one-page use-case backlog scored on value × feasibility × risk",
             "Turns enthusiasm into a ranked, defendable investment list.", "60 days", "AI sponsor + uniAIverse"),
        ],
        "mid": [
            ("Convert the AI strategy into a 12-month roadmap with quarterly checkpoints and KPIs",
             "Strategy exists but is not yet a managed plan.", "60 days", "AI sponsor"),
            ("Define an AI ROI template (baseline, target, measurement owner) for every initiative",
             "Makes value visible to the board and protects budget.", "60 days", "Finance + AI sponsor"),
        ],
        "high": [
            ("Move to portfolio management: review the AI backlog quarterly, retire low-value initiatives",
             "Keeps investment flowing to what works.", "90 days", "AI steering group"),
        ],
    },
    "data": {
        "low": [
            ("Inventory the 10 data sources behind your top 3 use cases; record owner, location, quality, access",
             "You cannot build on data you cannot find or trust.", "30 days", "Data owner + uniAIverse"),
            ("Fix access for those sources (API / export / warehouse) so no use case needs manual extraction",
             "Manual data pulls kill every automation on day one.", "60 days", "IT"),
            ("Introduce data classification (confidential / internal / public) before any AI ingestion",
             "Prevents the classic failure: an assistant that leaks HR or salary data.", "60 days", "IT + Compliance"),
        ],
        "mid": [
            ("Automate the pipelines feeding AI use cases and add basic quality monitoring (freshness, nulls, volume)",
             "Pilots built on hand-refreshed data break when they scale.", "90 days", "Data engineering"),
            ("Stand up a lightweight data catalogue with named stewards",
             "Reduces discovery time and duplicate effort across teams.", "90 days", "Data steward"),
        ],
        "high": [
            ("Adopt data contracts and SLAs per source; add lineage for regulated data",
             "Protects production AI from silent upstream changes.", "6 months", "Data platform lead"),
        ],
    },
    "technology": {
        "low": [
            ("Approve one company-standard LLM route (API + policy) so teams stop using personal accounts",
             "Shadow AI usage is a data-leak and compliance risk today.", "30 days", "IT + Security"),
            ("Expose your 3 most important systems via API or scheduled export",
             "Integration, not models, is the bottleneck in most AI projects.", "90 days", "IT / Engineering"),
        ],
        "mid": [
            ("Define a reference architecture for GenAI apps (RAG, chatbot, automation) with reusable components",
             "Cuts delivery time per use case by 30-50%.", "90 days", "Engineering lead + uniAIverse"),
            ("Introduce MLOps basics: model/prompt versioning, monitoring, rollback",
             "Production AI without monitoring degrades silently.", "90 days", "MLOps / Engineering"),
        ],
        "high": [
            ("Add cost, latency and quality dashboards per AI service; set budgets and alerts",
             "Unit cost drifts unnoticed behind flat traffic.", "90 days", "Platform team"),
        ],
    },
    "people": {
        "low": [
            ("Deliver 'AI for All' literacy training to managers and front-line teams",
             "Teams that understand hallucination and limits adopt AI safely and faster.", "30 days", "HR + uniAIverse"),
            ("Identify 3-5 internal AI champions and give them a build track (e.g. no-code RAG course)",
             "Creates internal capability instead of permanent vendor dependence.", "60 days", "HR / AI sponsor"),
        ],
        "mid": [
            ("Define AI roles and RACI: product owner, data steward, model owner, reviewer",
             "Unclear roles are why pilots stall after handover.", "60 days", "AI sponsor + HR"),
            ("Launch a monthly AI community-of-practice with show-and-tell",
             "Spreads learnings and surfaces new use cases cheaply.", "60 days", "AI champions"),
        ],
        "high": [
            ("Create tiered learning paths (business / engineer / GenAI engineer) with certification",
             "Sustains capability as tools change every quarter.", "6 months", "L&D"),
        ],
    },
    "process": {
        "low": [
            ("Document your 5 highest-volume manual workflows with volumes, time per item and error cost",
             "Automation candidates must be measured before they are automated.", "30 days", "Ops lead + uniAIverse"),
            ("Define a simple idea → pilot → production gate with entry/exit criteria",
             "Gives every initiative a known path and a known end.", "60 days", "AI sponsor"),
        ],
        "mid": [
            ("Add human-in-the-loop and escalation design to every AI workflow before launch",
             "Protects customers and staff when the model is wrong.", "60 days", "Process owner"),
            ("Track adoption and outcome metrics for 90 days after each rollout",
             "Delivery is not value; usage is.", "90 days", "Process owner"),
        ],
        "high": [
            ("Institutionalise continuous improvement: quarterly review of automated workflows and their KPIs",
             "Automations decay as processes change.", "6 months", "Ops excellence"),
        ],
    },
    "governance": {
        "low": [
            ("Publish a one-page responsible-AI policy: allowed tools, prohibited data, review requirement",
             "A short enforced policy beats a long ignored one.", "30 days", "Compliance + uniAIverse"),
            ("Create an inventory of all AI systems and third-party AI tools currently in use",
             "You cannot govern what you have not listed; regulators ask for this first.", "30 days", "IT + Compliance"),
        ],
        "mid": [
            ("Risk-classify every use case (prohibited / high / limited / minimal) and set controls per class",
             "Aligns with EU AI Act style obligations and focuses effort on real risk.", "60 days", "Compliance"),
            ("Add a pre-production AI review checkpoint (privacy, bias, security, explainability)",
             "Catches issues before customers do.", "60 days", "Compliance + Engineering"),
        ],
        "high": [
            ("Adopt a formal framework (NIST AI RMF / ISO 42001) and run an internal audit",
             "Procurement and enterprise clients increasingly demand it.", "6 months", "Compliance"),
        ],
    },
}

HORIZON_ORDER = {"30 days": 0, "60 days": 1, "90 days": 2, "6 months": 3}

def _band(score: float) -> str:
    return "low" if score < 40 else "mid" if score <= 70 else "high"

def recommend(dims: list[DimensionResult]) -> list[Recommendation]:
    # Weakest, most-weighted dimensions first
    ranked = sorted(dims, key=lambda d: (d.score, -d.weight))
    recs: list[Recommendation] = []
    for d in ranked:
        for action, why, horizon, owner in PLAYBOOK.get(d.id, {}).get(_band(d.score), []):
            recs.append(Recommendation(priority=0, dimension=d.title, action=action, why=why,
                                       horizon=horizon, owner_hint=owner))
    recs.sort(key=lambda r: HORIZON_ORDER[r.horizon])
    for i, r in enumerate(recs, 1):
        r.priority = i
    return recs

def roadmap(recs: list[Recommendation]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {h: [] for h in HORIZON_ORDER}
    for r in recs:
        out[r.horizon].append(f"[{r.dimension}] {r.action}")
    return {k: v for k, v in out.items() if v}
