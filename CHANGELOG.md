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

## 2026-09-21 — v2.5
### Training — every course now has a working kit
- `training-materials/labkit/`: shared pure-Python toolkit (ML from scratch, data quality/PII/drift, evals and judge, agent runtime with six caps, security controls and attack library, registry/gateway/SLO, ROI/TCO/PERT, text extraction and claim checks). Offline and deterministic; uses a real model when an LLM key is set.
- 108 demos across 24 courses (the workshop already had 7). Several call the real strategy, readiness and governance engines.
- `scripts/build_course_kits.py` generates README, facilitator guide, exercises, handout and `run_all.py` per course from demo headers + `curriculum.yaml`; hand-written files are never overwritten. `scripts/new_course.py` follows the same convention.
- Demo Hub: `GET /api/demos/courses`, `POST /api/demos/run-course/{course}/{demo}`; "Course labs" section on `/demos`.
### AI Delivery Framework 1.0 (`app/services/delivery/`)
- Twelve modules behind `/api/delivery/*` and the `/delivery` page; content in eight versioned YAML files; every pack stamped with engine version + content hash; overrides need a reason; prohibited uses stop with no pack; stored engagements, versions and gate records behind `X-Admin-Token`.
- Added to `pricing/tiers.yaml`, `pricing/blueprints.yaml` and the bot knowledge.
- Rate card and LLM prices are PLACEHOLDERS and every pack says so until they are confirmed.
### Engineering
- Fixed: `requirements.txt` lacked `email-validator` (via `pydantic[email]`) and `python-docx` — fresh installs, CI and Docker builds failed.
- Fixed: tests wrote to the real database and failed after a few runs per day; `tests/conftest.py` now isolates them. 28 → 71 tests.
- CI: secrets scan, full content + demo validation, kit freshness check, Docker build + health smoke test. Deploy waits for `/api/health` and rolls back if unhealthy. `.dockerignore` added; container `HEALTHCHECK` added. API version string is now 2.5.0.

## 2026-09-22 — v2.6
### Control plane (`app/services/platform/`, `/platform`, `/register`)
- Tenant model with ten states and an enforced state machine; approval before entitlement; plans as resource profiles (`plans.yaml`); capability catalogue with URL guards (`capabilities.yaml`).
- Entitlement engine (`engine.check`) and HTTP middleware with `ENTITLEMENTS_MODE=off|log|enforce` (default `log`); anonymous visitors draw from the free sandbox pool; `FREE CAPACITY EXHAUSTED` when the pool is spent.
- Provisioning as background jobs (`run_jobs`, `worker` container, `scripts/provision_worker.py`), idempotent, with audit trail; Razorpay `platform.*` products provision on verified payment; `tenant_id` on orders; bank-transfer "mark paid".
- Admin console: requests, approvals, sandbox pool, tenant dashboards, limit and capability changes with a reason and no redeploy, state moves, cost model.
- Cost model (`cost_model.yaml`, `GET /api/platform/cost-model`, `scripts/cost_report.py` → `docs/COST_ANALYSIS.md`), `docs/PLATFORM.md`, `docs/GO_TO_MARKET.md`, `docs/GAPS.md`.
- 78 tests. Everything from v2.5 unchanged and still passing.

## 2026-09-24 — v2.6.1
- **LLM gateway** `POST /api/platform/llm/complete`: tenant key → learner email → cohort plan → entitlement → per-user daily/cohort caps → cohort budget → platform-wide cap → rate limit → provider (model class from the registry) → real token metering → cost → audit. Hard stops answer 402. Offline stub meters at list price so quotas behave without a key. `GET /api/platform/llm/usage`, admin `GET /tenants/{id}/llm`, `POST /llm/global-cap`. New table `llm_calls`.
- **Cohorts as tenants**: `POST /api/platform/cohorts` (admin), `POST /cohorts/{id}/learners`; classroom plan in `plans.yaml → classroom.cohort` (not sold on the price page, not in the payment catalogue); keys expire with the cohort.
- **Registries** (`content/registries/`): tools, models (classes → provider model ids + INR prices), providers, agents, tracks. `GET /api/platform/registries`.
- **Operating content**: `token_policy.yaml` (hybrid decision, caps, alerts, override, abuse controls), `student_prerequisites.yaml`, `corporate_prerequisites.yaml` (+ `docs/templates/CORPORATE_PREREQUISITES_TEMPLATE.md`, admin endpoint), `team_tooling.yaml`, `procurement.yaml`.
- **Positioning and team**: Sarfi / Sachin (DevOps) / Harsh (intern, development); DevOps and Development are not standalone public offerings; `training-materials/tracks/` scaffold. Docs updated (WORK_SPLIT, website-patch, GAPS phases, EDITING).
- **Master Founder Operating Playbook**: `docs/MASTER_PLAYBOOK.md`.
- 84 tests. All v2.5 and v2.6 behaviour unchanged.
