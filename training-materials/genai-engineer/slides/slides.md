---
marp: true
theme: default
paginate: true
style: |
  section { font-family: Georgia, "Iowan Old Style", serif; color: #14213d; background: #fbfaf7; }
  h1, h2 { color: #1f2a44; } strong { color: #0f766e; } table { font-size: 0.8em; }
  section.lead h1 { font-size: 2.2em; } footer { color: #5b6170; font-size: 0.6em; }
footer: "uniAIverse Academy · GenAI Engineer · v2.0"
---

<!-- _class: lead -->
# GenAI Engineer
## Developers building LLM applications
**32 hours · cohort · certification: professional**

---

# What you'll be able to do
- Build a production-grade RAG system with evals
- guardrails and cost controls
- Apply every layer of the RAG stack deliberately
- Implement grounding
- citations
- refusal
- ACLs and injection defence

---

# Agenda
| # | Module | Hours |
|---|---|---|
| 1 | LLM fundamentals for builders | 4 |
| 2 | Ingestion (L0-L3) | 4 |
| 3 | Chunking and enrichment (L4-L5) | 4 |
| 4 | Embedding, storage, hybrid retrieval, reranking (L6-L12) | 4 |
| 5 | Query understanding and generation (L9, L13-L15) | 4 |
| 6 | Evaluation (L17) | 4 |
| 7 | Agents and routing (L22-L27) | 4 |
| 8 | Production (L18-L21) | 4 |

---

<!-- _class: lead -->
# Module 1
## LLM fundamentals for builders
*4h*

---

# LLM fundamentals for builders — key ideas
- **tokens**
- **context**
- **structured output**
- **tool calling**
- **prompt patterns vs folklore**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# Tokens
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Context
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Structured output
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Tool calling
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Prompt patterns vs folklore
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · Typed client with retries
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** Typed client with retries

---

<!-- _class: lead -->
# Module 2
## Ingestion (L0-L3)
*4h*

---

# Ingestion (L0-L3) — key ideas
- **layout-aware parsing**
- **cleaning**
- **dedup**
- **metadata and ACL capture**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# Layout-aware parsing
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Cleaning
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Dedup
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Metadata and ACL capture
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · Parse a messy two-column PDF
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** Parse a messy two-column PDF

---

<!-- _class: lead -->
# Module 3
## Chunking and enrichment (L4-L5)
*4h*

---

# Chunking and enrichment (L4-L5) — key ideas
- **structure-aware**
- **parent-child**
- **contextual prefix**
- **late chunking**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# Structure-aware
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Parent-child
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Contextual prefix
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Late chunking
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · Contextual prefix; inspect chunks
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** Contextual prefix; inspect chunks

---

<!-- _class: lead -->
# Module 4
## Embedding, storage, hybrid retrieval, reranking (L6-L12)
*4h*

---

# Embedding, storage, hybrid retrieval, reranking (L6-L12) — key ideas
- **model choice**
- **quantisation**
- **HNSW**
- **BM25**
- **RRF**
- **cross-encoders**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# Model choice
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Quantisation
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# HNSW
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# BM25
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# RRF
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Cross-encoders
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · Hybrid + rerank; recall@20
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** Hybrid + rerank; recall@20

---

<!-- _class: lead -->
# Module 5
## Query understanding and generation (L9, L13-L15)
*4h*

---

# Query understanding and generation (L9, L13-L15) — key ideas
- **rewriting**
- **filter extraction**
- **grounding**
- **citations**
- **refusal**
- **verification**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# Rewriting
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Filter extraction
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Grounding
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Citations
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Refusal
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Verification
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · Multi-turn grounded bot
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** Multi-turn grounded bot

---

<!-- _class: lead -->
# Module 6
## Evaluation (L17)
*4h*

---

# Evaluation (L17) — key ideas
- **golden sets**
- **RAGAS/DeepEval**
- **LLM-as-judge discipline**
- **CI**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# Golden sets
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# RAGAS/DeepEval
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# LLM-as-judge discipline
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# CI
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · 50-query golden set in CI
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** 50-query golden set in CI

---

<!-- _class: lead -->
# Module 7
## Agents and routing (L22-L27)
*4h*

---

# Agents and routing (L22-L27) — key ideas
- **ReAct**
- **tool registry**
- **MCP**
- **budgets**
- **termination**
- **when not to go agentic**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# ReAct
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Tool registry
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# MCP
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Budgets
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Termination
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# When not to go agentic
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · Router: simple / RAG / agent
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** Router: simple / RAG / agent

---

<!-- _class: lead -->
# Module 8
## Production (L18-L21)
*4h*

---

# Production (L18-L21) — key ideas
- **caching**
- **cost per request**
- **observability**
- **injection**
- **ACLs**
- **PII**
- **freshness**

<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->

---

# Caching
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Cost per request
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Observability
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Injection
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# ACLs
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# PII
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Freshness
- What it is
- Why it matters for **developers building llm applications**
- One example from your organisation

<!-- TODO: replace bullets with the actual teaching content / demo cue -->

---

# Lab · Trace + cost dashboard; capstone
1. Set-up (5 min)
2. Do (bulk of the time)
3. Share one result per table

**Deliverable:** Trace + cost dashboard; capstone

---

# Assessment
Capstone DoD: hybrid + rerank · contextual chunks · grounding + citations + refusal · golden set in CI recall@20 > 0.9 · per-request trace with cost · ACL pre-filter · injection defence

---

<!-- _class: lead -->
# Thank you
## Questions · next steps · uniaiverse.ai
