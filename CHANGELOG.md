# Changelog

All framework, curriculum, pricing and blueprint changes are recorded here. Bump the `version` field in the relevant YAML.

## 2026-09-12 — v2.0
### AI Readiness Framework (question_bank.yaml 2.0)
- Rebuilt from 30 questions / 6 dimensions to **348 questions / 10 domains / 51 capabilities + 6 industry modules**.
- New domains: Value & Portfolio, GenAI/LLM/Agentic Readiness, Security & Privacy, Investment & Cost.
- Tier-coded questions (Free 25 · Bronze 85 · Silver 179 · Gold 263 · Platinum 316 + industry modules).
- Evidence flags (*) and critical-control flags (!) → evidence checklist and red flags in reports.
- Capability-level remediation text; benchmarks by company size.
### Curriculum (curriculum.yaml 2.0)
- 22 courses across 10 tracks with versions, owners, review dates, prerequisites, certifications, modules, labs, assessments.
- New: Agentic AI Engineer, AI Evaluation, AI Security for Builders, AI FinOps, MLOps & LLMOps, Governance Practitioner, Executive Briefing, Sales Agents, Content Governance, Safe Use, Productivity, Use-Case Design, Data Foundations.
- Emerging-topics watchlist with review dates; API flags courses not reviewed in 6 months.
### Pricing & blueprints
- Added Free (audit) and Professional (training, individual) tiers; startup and professional size multipliers.
- New blueprints.yaml: phases, activities, outputs, team days and deliverables per service and tier; `/api/pricing/proposal` endpoint.

## 2026-09-12 — v1.0
- Initial release: 30-question audit, 9-course catalogue, tiered pricing, strategy/governance/automation calculators.

## 2026-09-15 — v2.1
- Course Finder: `POST /api/training/course-finder` (free vs paid depth), sample profiles, CV text parsing, `/course-finder` page.

## 2026-09-19 — v2.2
- **uniAI Quest**: quiz engine (136 questions, 10 topics, 3 difficulty levels), interview challenges, XP/levels, daily limits per tier, curated news pipeline (RSS → pending → admin approval), question drafts from news, mentor requests. Pages `/quest`, `/admin`.
- **Payments**: Razorpay orders, signature verification, webhook, Smart Collect bank transfer, UPI-under-limit rule, test mode, tier grants. Page `/pay`.
- **uniAI bot**: knowledge-base assistant for the website (replaces Orbi); `website-patch/` with `UniAIBot.tsx`, layout change, rewrites example, package.json fix.
- **Workshop**: Agentic AI & LLM Economics (1/2 days) trainer plan + exercises; added to business, leadership and GenAI engineer tracks.
- **Repo standard**: `features/*` → `dev` → `main` with backup-before-merge, CI on all branches, PR template, deploy workflow, Caddy/Compose for api.uniaiverse.ai, daily news refresh action.

## 2026-09-19 — v2.3
- Strategy, Governance and Automation promoted from beta to **end-to-end engagements**: structured intake, engines with editable YAML config, business cases / gap assessment / wave plans, PDF + Markdown reports, `/tools` page.
- Agentic AI workshop is now a **delivery kit**: 41-slide deck built from `slides.yaml` (speaker notes), minute-by-minute facilitator guide, 7 runnable demos (offline or live), sample documents, exercise sheets, handout cards, `run_all.py` pre-flight.
- `scripts/validate_content.py` (content integrity + demos), `scripts/new_course.py` (course pack generator), `scripts/build_slides.*`, `docs/EDITING.md`.

## 2026-09-20 — v2.4
- **Demo Hub** (`/demos`): every demo runnable in the browser, live "ask the documents" basic vs advanced RAG (your own text or samples).
- **Discovery kit** (`/discovery`): enquiry → discovery-questions document (PDF/Word/MD) for corporate, business, university, college, domain × workshop/training/audit/consulting.
- **Workshop editions**: corporate, business, university, college, non-technical, domain — each with deck, facilitator guide, exercises, README, built from one source (`variants.yaml`).
- Deployment strategy with monthly cost options (`docs/DEPLOYMENT_STRATEGY.md`), backup script, Cloudflare cache rules.
- Work split (`docs/WORK_SPLIT.md`) and plain-language guide (`docs/HOW_IT_WORKS.md`).
