# Facilitator guide — Agentic AI & LLM Economics — Enterprise edition
**Audience:** Mixed enterprise room: function heads, product owners, analysts, engineers (up to 25)  ·  **Duration:** 2 day(s)  ·  **Deck:** `deck-corporate.pptx` (43 slides, speaker notes on every slide)

## Tone
Formal, evidence-led. Every claim has a number. Use the client's own use cases from discovery.

## Platform
Client tenant preferred: Azure OpenAI / Copilot Studio, Vertex AI / Gemini, Bedrock, or Databricks. Ours as fallback.

## Before the day
- 20 curated documents a week before
- Accounts provisioned and tested
- Two named use cases from discovery
- Security sign-off on tools used in labs
- Run `python ../../demos/run_all.py` on the delivery laptop — it must print ALL DEMOS OK
- Replace `demos/sample_docs/` with the client's documents where allowed

## Run of show
Follow the master run sheet (`../../facilitator-guide.md`) for timing and demo cues, using only the slides in this deck. Variant-specific modules below are inserted where their heading says.

### Where this sits in your operating model (20 min, after “Model generations”)
Map the ladder to their landscape: which questions today are simple / normal / complex; which systems the router would need; who owns the eval set. Pull the readiness domains on screen: data, platform, governance, skills. Ask the sponsor which one blocks scale.

### Governance you can defend (25 min, after “safety rails”)
Risk tiers in EU AI Act language, the pre-production review gate, the inventory. Show the governance engine classify one of their use cases live. 'Regulators ask for the inventory first.'


## Labs in this variant
- **LAB0** — Hour-one win on the client's documents
- **LAB1** — Cost the two discovery use cases: best / expected / worst
- **LAB2** — Grounded assistant on client documents in the client tenant; before/after score
- **LAB3** — Agent with three tools drawn from their systems (read-only), cap + approval gate
- **LAB4** — Apply three cost controls to Lab 1
- **LAB5** — 90-day plan per table, presented to the sponsor


## Done when
Each table shows a scored assistant and a capped agent on client material; sponsor holds five costed 90-day plans; a risk tier is recorded for each.

## Follow-up offers
- Readiness audit (Silver+) within 30 days
- Pilot charter for the top plan
- Governance quick-start
