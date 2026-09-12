# GenAI Engineer — Course Plan (8 × 4h)
**Audience:** developers building LLM applications. **Reference:** the RAG cheat sheet (every layer, options, tools). **Promise:** a production-grade RAG/agent system with evals, guardrails and cost controls.

| Day | Theme | Lab |
|---|---|---|
| 1 | LLM fundamentals for builders: tokens, context, structured output, tool calling, prompt patterns that work vs folklore | Typed LLM client with retries and structured output |
| 2 | Ingestion done right: parsing (layout-aware), cleaning, dedup, metadata & ACL capture (L0-L3) | Parse a messy two-column PDF; compare extractors by eye |
| 3 | Chunking & enrichment: structure-aware, parent-child, contextual prefix (L4-L5) | Implement contextual prefix; inspect 20 chunks |
| 4 | Embedding, storage, hybrid retrieval, RRF, reranking (L6-L12) | Hybrid search + cross-encoder rerank; measure recall@20 |
| 5 | Query understanding & generation: rewriting, filter extraction, grounding, citations, refusal (L9, L13-L15) | Multi-turn bot with grounded answers and INSUFFICIENT_CONTEXT path |
| 6 | Evaluation: golden set, RAGAS/DeepEval, LLM-as-judge discipline, CI (L17) | 50-query golden set; eval in CI; one regression caught |
| 7 | Agents & routing: ReAct loop, tool registry, budgets, termination, MCP; when NOT to go agentic (L22-L27) | Router: simple / RAG / agent with hard caps |
| 8 | Production: caching, cost per request, observability, security (prompt injection, ACLs, PII), freshness (L18-L21) | Full trace + cost dashboard; capstone demo |

**Capstone Definition of Done:** hybrid + rerank · contextual chunks · grounding + citations + refusal · golden set in CI with recall@20 > 0.9 · per-request trace with cost · ACL pre-filter · injection defence.
