# Facilitator guide — AI for <Domain> Teams — no code, your documents (1 day)
**Audience:** Non-technical domain teams: legal, healthcare admin, finance, HR, operations, retail, public sector (up to 20)  ·  **Duration:** 1 day(s)  ·  **Deck:** `deck-domain.pptx` (23 slides, speaker notes on every slide)

## Tone
Plain language, one analogy (the new colleague and the library), zero jargon. Every example rebuilt around their documents and vocabulary.

## Platform
No-code only; hosted by us or in the client's approved tool (Copilot, Gemini, NotebookLM Enterprise) depending on data rules.

## Before the day
- Domain documents cleared for use
- Data rules confirmed (what may be uploaded)
- One domain expert in the room
- Run `python ../../demos/run_all.py` on the delivery laptop — it must print ALL DEMOS OK
- Replace `demos/sample_docs/` with the client's documents where allowed

## Run of show
Follow the master run sheet (`../../facilitator-guide.md`) for timing and demo cues, using only the slides in this deck. Variant-specific modules below are inserted where their heading says.

### What this means in your domain (20 min, after “Demo 2”)
Domain-specific failure stories: the invented clause, the wrong dosage unit, the out-of-date policy. Then the rule: the assistant cites or it doesn't answer. Confidentiality: what may never be uploaded, decided before the lab.

### Human in the loop, by design (20 min, after “safety rails”)
Where the human sits for their workflow: review before send, sampling, escalation. Draft, never decide. Show the governance classify tool: most of their use cases are 'limited' — transparency plus a human path.

### Your 30-day habit (15 min, after “Five things”)
One assistant, one test sheet, one owner. Add every wrong answer to the sheet. Show it to three colleagues. Don't expand the library yet.


## Labs in this variant
- **LAB0** — Hour-one win on their documents
- **LAB2** — Grounded assistant on their documents; 10 real questions from their week; one change at a time
- **LAB5** — Test sheet + owner + escalation path for one real task


## Done when
Every participant has an assistant that answers from their documents with citations and refuses otherwise, a 10-question test sheet, and a named owner.

## Follow-up offers
- Build Your Own AI Bot (4 half-days)
- Domain readiness snapshot
- Bronze automation engagement
