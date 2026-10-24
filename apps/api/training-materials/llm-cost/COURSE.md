# Calculating LLM Cost & Estimation Strategies — Workshop Plan (4 hours)
**Audience:** product owners, engineers, finance partners. **Promise:** estimate any GenAI feature's cost before launch, and keep it from exploding after.

## Modules
| Module | Min | Content |
|---|---|---|
| 1. The billing unit | 30 | Tokens ≈ ¾ word; 1 page ≈ 700 tokens; output costs ~5× input; cached input ~90% off; reasoning tokens are output |
| 2. The per-request formula | 40 | (system + retrieved context + history + question) × input rate + answer × output rate. Whiteboard the $0.014 question |
| 3. Volume and growth | 30 | Requests/day × 30; the two explosions: chat history growth and flagship-for-everything |
| 4. Lab: cost a real feature | 60 | Use the cost calculator (`cost_calculator.py`): three scenarios (basic / with RAG / agentic), sensitivity to k, history trim, model tier |
| 5. Estimation strategies | 40 | Bottom-up (per request) · top-down (budget → allowed tokens) · benchmark (log 100 real requests, extrapolate). Always give a range, not a number |
| 6. Cost controls | 30 | Prompt caching (static first) · routing/cascade (60-80%) · batch API (50%) · output limits · semantic cache · rerank 50 not 500 |
| 7. Monitoring | 10 | Log per request: model, in/out/cached tokens, request type, cost. Alert on cost per request, not total spend |

## Rules of thumb (2026 mid-tier rates, verify quarterly)
- Simple Q&A bot, 100 q/day: **$30-100/month**
- RAG assistant, 1,000 q/day, 5 chunks, mid-tier: **$300-800/month**
- Agentic workflow, 1,000 tasks/day: **$3,000-10,000/month** — route so only complex tasks go there
- Non-English content: **2-5×** tokens for the same information

## Deliverable
A cost sheet for one of your own features with best / expected / worst case and the three controls you'll apply.
