# Card 3 — Agent safety rails (none optional)
1. **Max iterations** — 5 to 10.
2. **Max cost per run** and **max wall-clock** — hard ceilings.
3. **Loop detection** — same tool + same arguments twice → stop.
4. **Required give-up path** — "I could not finish; here is what I tried."
5. **Human approval** for anything consequential or irreversible (send, pay, delete, change a record).
Plus: read-only tools first · least privilege · every run traced (steps, tools, tokens, cost) · weekly review of capped and failed runs · prune the tool list per route (20 tools ≈ 5,000 tokens per call).
Injection: retrieved content is data, not instructions — delimiters, strip hidden text at ingest, scan outputs, secure the sources as tightly as the index.
