# Agentic AI & LLM Economics — Working Workshop
**Trainer's plan · 2 days (or the 1-day cut in §8) · v1.0 · uniAIverse**

Promise on the wall: *"By 5 pm tomorrow you will have built a grounded assistant and a working agent on your own material, and you will know — in rupees or dollars — what it costs to run and what it returns."*

Audience: mixed. Leaders decide, analysts frame, engineers build. Every lab has a no-code path (Dify / n8n / NotebookLM) and a code path (Python notebook). Never split the room; split the lab.

Master analogy for the whole workshop: **the brilliant new colleague who has never worked here** (from the RAG course). The agent is that colleague given a phone, a budget and permission to make calls — which is exactly why you give them rules.

---

## Day 1 — Understanding and grounding

### Module 1 · The hour-one win (45 min)
- 0–15: everyone uploads 2–3 of *their own* documents into an instant tool and asks five questions.
- 15–30: everyone asks the same tool one question about their company it *can't* know. Watch the confident wrong answer.
- 30–45: flipchart of what worked / what failed. This list is the curriculum; we return to it at the close of Day 2.

### Module 2 · How it actually works (75 min)
| Min | Topic | Do |
|---|---|---|
| 15 | Prediction machine: autocomplete that read the internet. No database inside. | Phone autocomplete demo |
| 15 | Tokens: ¾ of a word; 1 page ≈ 700 tokens; input vs output; cached input | Tokenise a sentence live |
| 15 | Context window: what fits on the desk; why "give it everything" fails (cost, speed, accuracy, permissions) | The $20,000 vs $300 slide |
| 15 | Structured output and tool calling: how a model asks for a calculator | Show a JSON tool call |
| 15 | **Model generations.** What changed with reasoning models and frontier tiers (e.g. Claude Fable 5.1 class, and equivalents from other labs); why "the best model" is a per-task decision; open-weight and small models; what to expect next and how to stay current without chasing every release | Model-tier decision card |

> Trainer note: verify current model names, prices and context sizes the week before delivery. Say so in the room: "these numbers were checked on <date>; the shape of the argument doesn't change, the numbers do."

### Module 3 · Cost one question by hand (45 min)
Whiteboard the per-request formula: system + retrieved context + history + question → input; answer → output. Work the $0.014 question. Then the two explosions: untrimmed history, flagship-for-everything.

**Lab 1 (20 min):** each table costs one real feature from their business — best / expected / worst — using `cost_calculator.py`.

### Module 4 · The RAG ladder (90 min)
| Level | What it adds | When | Cost/speed |
|---|---|---|---|
| Basic | fetch, answer | clean FAQ | 1× |
| Advanced | query rewriting, hybrid search, reranking, contextual chunks | real company documents — where most systems should live | 1.1× |
| Hybrid | several stores + a router (documents / SQL / live APIs) | you have documents AND a database AND live systems | 1.3× |
| Agentic | the model decides what to look up, checks, retries | multi-step, cross-system questions | 5–10×, 10× slower |

The warning that matters most: **an agent does not fix bad retrieval, it repeats it — five times, at five times the cost.** Earn your way up.

**Lab 2 (45 min):** build a grounded assistant on the client's documents. Score 10 questions. Flip on hybrid search → re-score. Flip on reranking → re-score. One change at a time. Everyone reads five of their own chunks.

### Module 5 · Answering well (45 min)
The grounding instruction (only from the documents · cite · say "not found") and why "not found" is a number on a dashboard. Output-shape prompting. The three-question fault-finding rule: was the right page fetched → fetched but ignored → fetched, used, still wrong.

**Day 1 close (15 min):** each table states the one thing from the flipchart they now understand.

---

## Day 2 — Agents, strategy, money

### Module 6 · Agents that don't run away (90 min)
| Min | Topic |
|---|---|
| 15 | Vending machine vs librarian. The loop: think → look → read → judge → answer or try again |
| 15 | Tools: function schemas, MCP servers as the standard socket, the token cost of a long tool list |
| 15 | Memory tiers: conversation, working (offload to files), long-term, procedural |
| 15 | Safety rails — not optional: max iterations, max cost, max time, loop detection, a required "I give up" path, **human approval for anything that changes the world** |
| 15 | Injection through tools and documents; least-privilege; read-only first |
| 15 | When an agent is the wrong answer: simple high-volume questions, latency-sensitive paths, anything where a script already works |

**Lab 3 (60 min):** build an agent with three tools (search documents, look up a record, draft an email — *draft*, not send), a 6-step cap and an approval gate. No-code path in n8n/Dify; code path in a notebook. Every table shows one run that hit the cap on purpose.

### Module 7 · Smart routing: the money saver (30 min)
Simple → answer directly · normal → one retrieval · complex → agent loop. The 10,000-questions-a-day numbers: all-simple $4.5k (fails hard ones) · all-agentic $22k · routed $9.8k with agentic quality where it matters. Sort your questions first.

### Module 8 · Token optimisation and model tiering (45 min)
In order of payoff: prompt caching (static-first ordering, up to 90% off input) · model routing / cascade (60–80%) · batch API (50%) · output limits and history trimming · rerank 50 not 500 · quantised indexes. Model tiering rule: cheap for extraction, mid for grounded answering, frontier for analysis and planning.

**Lab 4 (20 min):** apply three controls to the Lab 1 cost sheet; record the new expected cost.

### Module 9 · Strategic use in your business (60 min)
- Five value patterns: assist, automate, augment decisions, new products, risk reduction.
- Regular use vs strategic use: personal productivity is table stakes; strategic is a workflow redesigned with an agent in it, measured.
- Prioritisation on value × feasibility × risk × effort (uniAIverse strategy tool). Quick wins vs strategic bets.
- The readiness lens: the free 25-question snapshot, live, per table.

### Module 10 · ROI and the 90-day plan (60 min)
Workflow ROI model (uniAIverse automation tool): volume × minutes × loaded cost + error cost → automation share → monthly saving → payback. Governance quick start: inventory, risk tier, review gate, policy one-pager.

**Lab 5 (40 min):** each table produces a one-page 90-day plan for one workflow: outcome, approach (RAG level / agent or not), cost range, ROI, owner, gates. Present in three minutes.

### Close (15 min)
Return to the Day 1 flipchart. Every failure now has a name and a fix. Five things to remember:
1. No database inside — it predicts. That's why it invents.
2. Fetch the right pages first. Five right beat fifty mediocre.
3. When it's wrong, look at what it fetched before blaming the model.
4. Agents amplify retrieval quality — good or bad. Earn your way up; cap everything.
5. Cost is a design decision: cache, route, trim, tier.

---

## 6. Materials checklist
Client documents (20, curated, a week before) · sample messy PDF · Dify/n8n instance tested with 20 logins · notebooks for the code path · printed cards: model-tier decision, agent safety rails, fault-finding, cost formula · the RAG cheat sheet as the take-home reference · the two uniAIverse tools open (strategy, automation ROI) · free readiness snapshot link.

## 7. Handouts
1. Cost formula card + `cost_calculator.py`
2. RAG ladder one-pager with "you need it when"
3. Agent safety rails card (the five caps + approval gate)
4. Token-optimisation checklist in payoff order
5. 90-day plan template

## 8. The one-day cut (8h)
Keep: M1 (30), M2 (60), M3 (30), M4 + Lab 2 (90), M6 + Lab 3 (90), M7 (15), M8 (30), M10 + Lab 5 (60), Close (15). Drop M5 and M9 into handouts. Warn the room that attention collapses after hour five; take a real break.

## 9. Success measures
End of Day 1: every table has a grounded assistant with a before/after score. End of Day 2: every table has an agent that hit its cap, and a costed plan. Two weeks later: at least one plan has an owner and a date.

*Tool and model names verified 19 Sep 2026. Re-verify before every delivery — the framework is stable, the names aren't.*
