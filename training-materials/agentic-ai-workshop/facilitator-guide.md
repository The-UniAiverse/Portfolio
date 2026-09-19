# Facilitator Guide — Agentic AI & LLM Economics (2 days)

This is the run sheet. Slides are in `slides/slides.md` (PDF: `slides/slides.pdf`); demos in `demos/`; exercise sheets in `exercises.md`. Every demo runs offline; with an API key in the repo `.env` the same commands use a real model.

**One week before:** run `demos/run_all.sh` on the laptop you will use. Collect 20 client documents into `demos/sample_docs/` (Markdown or plain text; headings matter). Print `exercises.md` per table and the five handout cards. Create tool logins for the room. Check model names/prices and write the date on slide 8.

**Room:** tables of 3–4, mixed roles. Projector + your terminal visible. Flipchart. Wi-Fi tested with 20 devices.

---

## DAY 1

| Time | Slide | Segment | What you do and say |
|---|---|---|---|
| 09:00 | 1–2 | Welcome & the promise | Read the promise on slide 1 out loud. Then slide 2 — the new colleague. "Hold this picture. Everything today maps to it." |
| 09:10 | 3 | **Hour-one win** | Everyone uploads 2–3 documents into the instant tool (NotebookLM / Claude Project / your Dify). Five questions each. Then: "Ask it something about your company it *cannot* know." Walk the room. Flipchart every failure verbatim. |
| 09:45 | 4 | Prediction machine | Phone autocomplete on the projector. Then **run `python demos/02_hallucination.py`**: closed-book first — pause on the invented answer, let it land. Then the grounded half. "Same model. Only the desk changed." |
| 10:05 | 5–6 | Tokens & cost | **Run `python demos/01_tokens_and_cost.py --daily 300`**. Walk the per-question table line by line on the whiteboard *before* showing the script output. Ask the room to guess the monthly cost, then reveal. Point at the two explosions. |
| 10:30 | | Break | |
| 10:45 | 7 | Why not paste everything | The $20,000 vs $300 slide. Four reasons: money, speed, accuracy, permissions. |
| 10:55 | 8 | Model generations | Frontier / mid / cheap / open-weight. "The best model is a per-task decision." Show the date you verified names. Do not read a vendor list; show the decision card handout. |
| 11:15 | | **Lab 1** — cost a real feature | Exercise sheet Lab 1, 20 min. Each table: one feature, best/expected/worst. Two tables read out their numbers. |
| 11:40 | 9–10 | RAG in five steps · the ladder | Draw the five steps on the whiteboard, slowly. Then the ladder. Land the warning: "An agent does not fix bad retrieval. It repeats it." |
| 12:00 | | Lunch | |
| 13:00 | 11 | Cutting the cards | Read the too-small card out loud. Then the prefix trick. **Run `python demos/03_rag_basic_vs_advanced.py`** but stop after the score table — say nothing yet. |
| 13:15 | 12 | Two searches | Explain meaning vs keyword with the ERR code and "money back". Scroll to the demo's blind-spot section. RRF by rank on the whiteboard with three cards. Then reranking = hiring: 500 → 50 → 5. |
| 13:40 | 13 | **Lab 2** — one change at a time | 45 min. Tables build on the client's documents in the no-code tool (code track: `demos/common.py` is the reference). Score 10 questions → hybrid → rerank → chunk size. **Enforce one change at a time.** Everyone reads five of their own chunks out loud. Collect before/after scores on the flipchart. |
| 14:30 | | Break | |
| 14:45 | 14–15 | The grounding sentence · fault-finding | Put slide 14 up and leave it. "Not found is a number on a dashboard." Then the three questions in order. Ask: "Where did you start yesterday?" — most say 3. |
| 15:05 | 16 | Hybrid: the router | **Run `python demos/04_router.py`**. Five questions, four routes. Pause on the SQL line: "computed, not guessed." "Log every misroute — that's your roadmap." |
| 15:20 | | Day 1 close | Each table: one item from the morning flipchart they now understand. Homework: 10 real questions from their work, 3 with the correct answer written down. |

## DAY 2

| Time | Slide | Segment | What you do and say |
|---|---|---|---|
| 09:00 | 17–18 | Vending machine vs librarian | Recap Day 1 in two minutes using the ladder. Then the loop. Draw THINK → LOOK → READ → JUDGE with the limit arrow. |
| 09:15 | 19 | Tools & MCP | Function with a schema. MCP as the socket. "20 tools ≈ 5,000 tokens every call." Read-only first. |
| 09:30 | 20 | Safety rails | Read the six caps. **Run `python demos/05_agent.py`** — narrate each THINK/ACT/OBS line; when the GATE prompt appears, ask the room whether to approve. Then **`--runaway`**: watch loop detection stop it. "Every cap is a line of code." |
| 10:00 | 21 | Injection | **Run `python demos/05_agent.py --inject`**. Show the poisoned document arriving as `<document>` data; show the agent has no send-email tool. Four controls. |
| 10:15 | | Break | |
| 10:30 | 22 | **Lab 3** — an agent that can't run away | 60 min. No-code track: n8n/Dify agent with three tools, iteration cap, approval node. Code track: copy `demos/05_agent.py`, swap in their tools. Every table must show one run that hit the cap on purpose and one injection test. |
| 11:30 | 23 | Smart routing economics | **Run `python demos/06_routing_economics.py --per-day 10000`**. Three policies. "Sort your questions first." |
| 11:45 | 24 | Token optimisation | Payoff order. **Lab 4** (20 min): apply three controls to their Lab 1 sheet. Read out the delta. |
| 12:10 | | Lunch | |
| 13:10 | 25 | Strategic use | Five value patterns; regular vs strategic use. Each table does the free readiness snapshot live (`api.uniaiverse.ai` → Free). Discuss the weakest domain per table. |
| 13:50 | 26 | ROI in one line | Whiteboard the formula with one table's workflow. Show the automation tool (`/api/automation/assess` sample) producing the same numbers. Approach by shape. |
| 14:10 | 27 | **Lab 5** — 90-day plan | 40 min. One page per table. Then 3-minute presentations, 2 questions each. You note one risk per plan. |
| 15:10 | | Break | |
| 15:25 | 28 | Five things to remember | Slide 28. Ask the room to say them before you reveal. |
| 15:35 | 29 | Back to Monday's flipchart | Go through every failure from Day 1. Name the fix. This is the moment the course pays off — don't rush it. |
| 15:50 | | Close | Handouts: cost card, RAG ladder, safety rails, optimisation checklist, plan template. Certificate criteria: working agent demo + costed plan presented. Next step offer: readiness audit or a pilot from their plan. |

---

## If you're short on time (one-day cut, 8h)
Keep: hour-one win (30) · prediction machine + Demo 2 (20) · tokens + Demo 1 (25) · ladder (15) · cutting + searches + Demo 3 (30) · Lab 2 (45) · grounding + fault-finding (15) · router + Demo 4 (15) · agent + Demo 5 incl. runaway and inject (30) · Lab 3 (45) · routing economics + Demo 6 (15) · Lab 5 (40) · close + flipchart (20). Drop model generations and strategic use into handouts. Two real breaks.

## Live-mode notes (when an API key is set)
- Demo 2's closed-book answer will vary; sometimes the model hedges. If it does, say: "Newer models hedge more — but hedging isn't citing. Watch the open-book half."
- Demo 5 uses a strict JSON contract; if the model returns prose, the script hands to a human — that *is* the lesson. Run it again.
- Costs printed are estimates from token counts × the rates in `demos/common.py`. Update `RATES` quarterly.

## What can go wrong
- **Setup eats the first hour.** Send logins a week before. Have a shared fallback login.
- **Tables change three settings at once.** Stand next to them. Make them re-run.
- **Engineers dominate.** Split the lab, not the room: code track works alongside no-code.
- **A demo fails live.** Every demo has offline mode — unset the key and re-run. Say why. That's a lesson too.

*Tool names and prices verified 19 Sep 2026. Re-verify before every delivery.*
