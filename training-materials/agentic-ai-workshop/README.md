# Agentic AI & LLM Economics — Workshop kit (ready to deliver)

| What | Where | Edit it |
|---|---|---|
| Slide deck with speaker notes (41 slides) | `Agentic-AI-LLM-Economics.pptx` — built from `slides.yaml` | edit `slides.yaml`, run `node scripts/build_slides.js training-materials/agentic-ai-workshop/slides.yaml` |
| Trainer's plan (timings, modules, 1-day cut) | `WORKSHOP.md` | edit directly |
| Working demos (offline; richer with an LLM key) | `demos/01…07_*.py`, `demos/run_all.py` | plain Python; shared toolkit in `demos/common.py` |
| Sample documents for demos & Lab 2 fallback | `demos/sample_docs/*.md` | add/replace `.md` files (headings `##` drive chunking) |
| Exercise sheets (Labs 1–5) | `exercises.md` | edit directly |
| Handout cards | `handouts/01…05.md` | edit directly; print A5 |
| Cost calculator for Lab 1 | `demos/../cost_calculator.py` | edit `RATES` |

## Run of show
**One week before:** client sends 20 curated documents; tool logins created; run `python demos/run_all.py` — it must print `ALL DEMOS OK`; verify model names/prices and update `RATES` in `demos/common.py` and slide 10.
**Room:** projector · every participant has a laptop and a browser · Dify/n8n instance tested · printed handouts · the flipchart.
**Day 1:** slides 1–22 · demos 2, 1, 3, 4 · Labs 0, 1, 2.  **Day 2:** slides 23–41 · demos 5, 6, 7 · Labs 3, 4, 5.
**Demos:** `cd training-materials/agentic-ai-workshop/demos && python NN_*.py` — each prints trainer cues at the end.
**Live mode:** set `LLM_PROVIDER` + key in the repo's `.env`; demos 2 and 5 then run against a real model (demo 2: ask about the client's own policies).

## Adapting for a client
- Replace `demos/sample_docs/` with 4–6 of the client's real policies (keep `##` section headings) — every demo and Lab 2 then run on their material.
- Change `deck.brand`/`footer` in `slides.yaml` for co-branding; rebuild.
- One-day version: see `WORKSHOP.md §8`; delete the slides you cut from `slides.yaml`.
