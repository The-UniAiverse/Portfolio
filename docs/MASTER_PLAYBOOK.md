# UniAiVerse v2.6 — Master Founder Operating Playbook

*For Sarfi. Written 24 September 2026 against the v2.6.1 codebase on `features/sarfi`. This is the one document that answers "what do I do next?". Everything else in `docs/` is detail it points to. All rupee figures are estimates to verify at purchase unless marked "measured".*

**Company facts:** mailboxes `support@uniaiverse.ai` (customers, grievance officer), `admin@uniaiverse.ai` (accounts, providers, GitHub), `ai@uniaiverse.ai` (company address, not final) · GSTIN 27AADCU8825H1Z0 · GST ARN AA270926111040M · domain `uniaiverse.ai` owned until 2027 (never buy another) · repo `git@github.com:The-UniAiverse/ai-services.git` · API `https://api.uniaiverse.ai`.

---

## 1. Current state

An engine (FastAPI) with 13 services, 25 courses with 115 runnable labs, an AI Delivery Framework, a control plane, and now an LLM gateway. 84 automated tests pass; every course pre-flight passes; a clean install from the commit runs. Not yet deployed, no paying customer, no cohort delivered, Razorpay unapproved, legal pages unwritten, prices unconfirmed. The product is ahead of the business. This playbook exists to invert that.

## 2. What v2.6 contains

| Layer | Contents | Where |
|---|---|---|
| Faces | `/` audit · `/discovery` · `/delivery` · `/tools` · `/demos` · `/course-finder` · `/quest` · `/pay` · `/register` · `/platform` · `/admin` · `/docs` | `ui/*.html`, routes in `app/main.py` |
| Engines | readiness audit, strategy, governance, automation, pricing, quest, bot, demos hub, discovery, payments, delivery framework, platform (control plane + gateway) | `app/services/*` |
| Content as data | question banks, curriculum, bot knowledge, pricing, delivery content (8 files), platform content (plans, capabilities, cost model, token policy, prerequisites, tooling, procurement, 5 registries) | `*.yaml` |
| Training | 25 AI courses with demos, guides, exercises, handouts, run_all; 6 workshop editions; shared `labkit` | `training-materials/` |
| Operations | CI (6 checks), deploy with health check and rollback, worker, backups, Dockerfile | `.github/`, `deploy/` |
| Documents | this playbook, How-To (v2.5), Platform playbook (v2.6), PLATFORM, COST_ANALYSIS (generated), GO_TO_MARKET, GAPS, EDITING, WORK_SPLIT, DEPLOY, templates | `docs/` |

## 3. Final changes in v2.6.1 (this release)

1. LLM gateway with real token metering, per-learner and per-cohort caps, budgets, rate limits, platform-wide cap, audit, offline stub.
2. Cohorts as classroom tenants: admin-created, learners enrolled by email, keys that expire with the cohort. Not on the price page.
3. Registries for tools, models (classes and prices), providers, agents, tracks.
4. Operating content: token policy, student prerequisites, corporate prerequisites (+ template), team tooling, procurement.
5. Team and positioning applied: Sarfi / Sachin / Harsh; DevOps and Development are not standalone public offerings; `training-materials/tracks/` scaffold for their draft curricula.
6. Docs: GAPS reclassified into phases, EDITING, WORK_SPLIT, website-patch, CHANGELOG.

Nothing from v2.5 or v2.6 was removed. The 78 previous tests pass unchanged.

## 4. Team ownership

| Person | Owns | Does not own |
|---|---|---|
| **Sarfi** | AI content and labs, consulting delivery, commercial (pricing, sales, contracts), product decisions, control-plane content, registries, this playbook | servers, website code |
| **Sachin** | VPS, Docker, deploy, Cloudflare, backups and restore tests, monitoring, secrets vault, key rotation, DevOps track (draft) | pricing, customer contracts |
| **Harsh** | Website build and content, website analytics, development/SDE track (draft, language undecided), small engine tasks under review | anything touching production secrets or customer data |

Decision rule: Sarfi decides money and customers; Sachin decides how things run; Harsh proposes and learns. Any change to prices, plans, legal text or customer data handling needs Sarfi.

## 5. Commercial positioning

Public business = **AI**: services, consulting, readiness, assessments, workshops, solutions and demos, platform. Training & Mentorship = one page with three tracks: AI (Sarfi), DevOps (Sachin), Development / SDE (Harsh). DevOps and Development are taught inside cohorts; they are **not** separate service pages or price-list items until the business decides otherwise. Source of truth: `registries/tracks.yaml → public_positioning`; the website shows only `status: final` tracks as offerings.

## 6. Monetisation (staged activation)

| # | Stream | Activate when | First offer | Price to test |
|---|---|---|---|---|
| 1 | Professional cohorts | now | "AI at Work", 4 weekends, bring your own workflow | ₹15–30k per seat, 12–25 seats |
| 2 | Student cohorts | after cohort 1 | "AI Engineer + ship it", 6 weekends, includes DevOps and SDE modules | ₹6–12k per seat or ₹1–2L per college batch |
| 3 | Corporate workshops | now | 1–2 day editions that exist | ₹75k–2.5L per day + AI pass-through |
| 4 | Consulting | now | free discovery → Delivery Framework scoping → 90-day pilot with success fee → run service | scoping ₹2–20L by tier; pilots ₹3–10L |
| 5 | Platform subscriptions | after the first pilot needs hosting | Bronze/Silver/Gold as priced in `plans.yaml` | ₹15k/45k/1.2L + infra at cost + 15% |
| 6 | Licensing | after cohort results exist | campus edition of the kits, train-the-trainer | ₹2–5L per college per year |

Illustrative first year if the first quarter works: ₹35–55L gross. A target to falsify, not a forecast.

## 7. Procurement

Master table lives in `app/services/platform/content/procurement.yaml` (status: owned / free / one_time / monthly / usage / not_yet / on_trigger). Summary:

| Item | Owner | Provider | Owned? | One-time | Monthly | Usage | Now? | Trigger |
|---|---|---|---|---|---|---|---|---|
| Domain uniaiverse.ai | Sarfi | registrar | **yes, to 2027** | 0 | 0 | 0 | — | renew 2027 |
| Cloudflare DNS/HTTPS/WAF | Sachin | Cloudflare Free | no | 0 | 0 | 0 | yes | now |
| Control-plane VPS 2 vCPU/4 GB | Sachin | DO/Linode/Vultr India | no | 0 | ₹1,700 | — | yes | day of first deploy |
| Customer host 4 vCPU/8 GB | Sachin | same | no | 0 | ₹4,200 pass-through | — | no | first paying Bronze |
| VPC / private networking | Sachin | cloud | no | 0 | 0 | — | no | first Gold or regulated customer |
| Backup bucket 50 GB | Sachin | R2/B2 | no | 0 | — | ₹100 | yes | day of first deploy |
| Database | Sachin | SQLite (repo) | yes | 0 | 0 | — | yes | Postgres after ~10 tenants or 2 nodes |
| Vector DB | Sarfi | pgvector/Qdrant | no | 0 | 0 | — | no | first paid tenant-RAG pilot |
| Company email ×3 | Sarfi | Workspace/Zoho | no | 0 | ₹1,950 | — | yes | now |
| Password manager | Sachin | Bitwarden | no | 0 | 0 | — | yes | now |
| GitHub org | Sachin | GitHub Free | no | 0 | 0 | — | yes | Team plan when minutes run out |
| GitHub Copilot | Harsh | GitHub | no | 0 | ₹840 (₹0 student) | — | yes | now |
| DevOps tooling | Sachin | OSS | yes | 0 | 0 | — | yes | now |
| Monitoring/uptime | Sachin | UptimeRobot free | no | 0 | 0 | — | yes | paid after first SLA |
| LLM API keys | Sarfi | Anthropic/OpenAI | no | 0 | — | ~₹800 | yes | console cap first |
| Student token pool | Sarfi | same key | no | 0 | — | ≤₹20,000 per cohort | no | per cohort, recovered from tickets |
| Mentor AI subscriptions | each | see §11 | no | 0 | ₹13,890 mandatory | — | yes | now |
| Razorpay | Sarfi | Razorpay | no | 0 | 0 | ~2%+GST | yes | KYC now, test mode until approved |
| Transactional email | Sachin | Resend/SES | no | 0 | 0 | tiny | no | before first cohort |
| Website hosting | Harsh | Vercel Hobby | no | 0 | 0 | — | yes | Pro on team seat/bandwidth |
| CRM | Sarfi | Google Sheet → HubSpot Free | no | 0 | 0 | — | yes | now |
| Analytics | Harsh | Cloudflare/Plausible | no | 0 | 0 | — | no | before first cohort |
| Accounting/invoicing | Sarfi | CA + Zoho Books | no | 0 | ₹3,000 | — | yes | first bank-transfer invoice |
| Legal review | Sarfi | lawyer | no | ₹25,000 | 0 | — | yes | before first payment |
| Kubernetes, GPU, redundancy, enterprise monitoring | Sachin | — | — | — | — | — | **no** | see triggers in the YAML |

## 8. Monthly budget (UniAiVerse expense only, unless marked)

| Budget | Lines | ₹/month |
|---|---|---|
| **One-time launch** | legal review ₹25,000 (+ partnership agreement in the same review) | ₹25,000–40,000 once |
| **Platform fixed** (measured by `cost_model.yaml`) | VPS 1,700 · backups 100 · domain and transactional email 300 · LLM polish 800 · free-sandbox cap 2,000 | **₹4,900** |
| **Internal team tooling** (`team_tooling.yaml`) | Sarfi Claude Max 8,400 · Sachin Claude Pro 1,700 · Harsh Copilot 840 · email ×3 1,950 · vault/Docker/GitHub 0 | **₹12,890 mandatory** (+₹4,400 optional: ChatGPT Plus, Claude Pro for Harsh, GitHub Team; email counted once) |
| **Accounting** | CA filing | ₹3,000 |
| **Minimum monthly** | platform fixed + mandatory tooling + accounting | **≈ ₹20,800** |
| **Practical monthly** | minimum + optional tooling + one cohort pool in flight | **≈ ₹25,200 own + ₹20,000 pool (recovered from tickets)** |
| **Growth-stage monthly** | practical + Postgres 1,500 + Vercel Pro 1,700 + GitHub Team 1,000 + paid uptime 1,500 + email 500 | **≈ ₹31,400 own** + pass-throughs |
| **Student/cohort variable** (student-paid or recovered) | gateway ₹100–500 per learner (cap 500) · Classroom/Meet 0 · certificate 0 · BYO subscription ≈ ₹1,700 paid by learner | ≤₹500 per learner from the pool |
| **Corporate variable (customer pass-through)** | AI usage at cost + 15% · travel at cost · their licences (Copilot ≈ USD 30/user/month) | invoiced, not absorbed |
| **Production customer (pass-through + our cost)** | per plan in `docs/COST_ANALYSIS.md`: Bronze cost to us ₹5,490 vs revenue ₹21,900; Silver ₹22,200 vs ₹68,000; Gold ₹90,000 vs ₹1,89,000 | margin 50–73% |

Three buckets never mixed: **UniAiVerse expense** (above), **customer pass-through** (infra, AI, licences, travel — invoiced at cost + 15% with GST), **student-paid** (own subscription, own laptop, free-tier hosting).

Real monthly exposure before revenue: about ₹21,000. With one cohort running: about ₹41,000, of which ₹20,000 comes back in ticket price. Nothing else is committed until a trigger fires.

## 9. Student onboarding

Checklist per track in `student_prerequisites.yaml`, served at `GET /api/platform/registries`. At enrolment send it; at week 0 run a 45-minute setup session and tick it off. Minimum: laptop 8 GB RAM, Python 3.12, Git, VS Code, browser, GitHub with 2FA, Google account, a personal AI account (free tier acceptable), stable 5 Mbps. Docker only for AI Engineer and DevOps. Deployment: GitHub Actions/Pages plus one free-tier host; students apply for the GitHub Student Developer Pack. No laptop: pair up or the shared cloud VM Sachin provides for the day. Three rules on the form: no employer, customer or third-party data in any classroom tool or key; keys are per cohort and expire with it; attendance and assignments are tracked and visible to the learner.

## 10. Student token system (the v2.6.1 decision: hybrid)

- **Offline by default.** Every lab runs with no key. The facilitator guide marks the LIVE minutes.
- **BYO for building.** Projects and agentic coding use the learner's own subscription (≈ ₹1,700/month) or free tier plus a local model via Ollama. Put it in the ticket text.
- **Classroom pool for shared labs**, through the gateway, one key per cohort.

| Control | Value | Where |
|---|---|---|
| Pool per cohort | ₹20,000 hard stop; alert at 70% | `plans.yaml → classroom.cohort.monthly_spend_limit_inr`, `token_policy.yaml` |
| Per learner | 40 calls/day, 400 per cohort, ₹500 per cohort | same |
| Model class | cheap by default; mid allowed; flagship denied | `registries/models.yaml`, plan `allowed_model_classes` |
| Sizes | 6,000-token prompt, 800-token output | plan |
| Rate limit | 6/min per learner, 60/min per cohort | `token_policy.yaml` |
| Platform-wide cap | ₹60,000/month, `POST /api/platform/llm/global-cap` | `platform_settings` |
| Provider cap | set by hand in the provider console **before** the key exists (₹30,000) | `registries/providers.yaml` |
| Override | Sarfi only, `PATCH /api/platform/tenants/{cohort}/limits` with a reason, audited | console |
| Expiry | key dies 45 days after creation; rotate every cohort | `create_cohort` |
| Tracking | `llm_calls` table; `GET /api/platform/llm/usage` (cohort), `GET /api/platform/tenants/{id}/llm` (admin) | — |
| Abuse | per-user caps, cohort cap, size caps, rate limits, model allow-list, enrolment-only emails, weekly top-user review | — |

Known limitation: learners share the cohort key and identify by email (honour system). Per-user caps and the cohort cap bound the damage; a personal login per learner is GAPS #1 and comes with the website sign-in.

## 11. Mentor / team tooling budget

| Tool | User | Purpose | Tier | ₹/month | ₹/year | Mandatory |
|---|---|---|---|---|---|---|
| Claude Max (Pro in month 1 if Max is not justified) | Sarfi | content, deliverables, agentic coding on the repo | Max 5x | 8,400 | 1,00,800 | yes |
| ChatGPT Plus | Sarfi | second model family for judge calibration, demos | Plus | 1,700 | 20,400 | no |
| Claude Pro | Sachin | infra scripts, runbooks, incidents | Pro | 1,700 | 20,400 | yes |
| GitHub Copilot Pro | Harsh | daily coding assistant | Pro (free if verified student) | 840 | 10,080 | yes |
| Claude Pro | Harsh | learning, code-review explanations | Pro | 1,700 | 20,400 | no |
| GitHub Team | all | Actions minutes, protection | 3 seats | 1,000 | 12,000 | no |
| Docker Desktop, Bitwarden | all | — | free tiers | 0 | 0 | yes |
| Google Workspace or Zoho | all | email, Meet | Starter ×3 | 1,950 | 23,400 | yes |

Mandatory ≈ ₹12,890/month; optional ≈ ₹4,400. Roles differ on purpose: Sarfi's tier pays for itself in one deliverable; Sachin needs a general assistant, not agentic coding; Harsh's Copilot is free as a student.

## 12. Corporate prerequisites

Reusable framework in `corporate_prerequisites.yaml` (admin endpoint `GET /api/platform/corporate-prerequisites`) and the fill-in record `docs/templates/CORPORATE_PREREQUISITES_TEMPLATE.md`. Eleven stacks: M365/Copilot, Azure OpenAI, Azure ML/Databricks, GitHub Enterprise/Copilot, AWS, GCP, OpenAI/Anthropic direct, Entra ID/SSO, VPN/private/on-prem/hybrid, ERP/MES/CRM/databases, vector store. Each row states prerequisite, customer responsibility, our responsibility, licensing, approximate cost, access, security, data, residency, network, effort, owner. Procedure: send the template with the discovery pack; fill it in the kickoff; sign-off from customer IT, data owner and Sarfi before any access is granted.

## 13. Control plane

Tenants with ten states and an enforced state machine; approval before entitlement; plans as resource profiles; provisioning as idempotent background jobs (worker container); audit on every move. Admin console `/platform`, public `/register`. Detail: `docs/PLATFORM.md`, `docs/PLATFORM_PLAYBOOK.md`.

## 14. LLM gateway

```
learner/app → X-Tenant-Key (+ X-User-Email) → tenant state → plan → llm.complete entitled? → model class allowed? → prompt size
→ tenant monthly quota → tenant spend cap → per-user daily/cohort/spend caps → platform-wide cap → rate limits
→ provider (model id from registries/models.yaml for LLM_PROVIDER) → tokens from the provider response → INR cost → llm_calls + tenant_usage → audit on denial
```

`POST /api/platform/llm/complete` (body: prompt, max_tokens, model_class, purpose). 402 = a limit said no with the reason; 403 = identity; 429 = rate; 503 = provider failed, nothing charged. With no provider configured the gateway returns an offline stub and still meters at list price, so budgets behave identically in class rehearsals.

## 15. Entitlements: log → enforce

`ENTITLEMENTS_MODE` in `.env`: `off` (never in production), `log` (launch: check, record, allow, `X-Entitlement` header), `enforce` (402/401). The gateway always enforces its own caps regardless of mode, because it spends money.

**Switch to `enforce` only when all of these are true:** (1) the website sends `X-Tenant-Key` after sign-in for every paid user; (2) 14 days of `log` data show zero unexpected denials for paid tenants (`SELECT * FROM tenant_usage WHERE allowed=0`); (3) every public demo path still passes anonymously in a staging test; (4) the free pool cap and alert have fired at least once in a drill; (5) Sachin can roll the flag back in under five minutes and has done it once. Record the switch in the audit log.

## 16. Billing

Platform fees through Razorpay (`platform.<plan>`, `platform.<plan>.setup`); infrastructure and AI pass-through invoiced monthly at cost + 15% with GST from the tenant dashboard's spend; cohorts by bank transfer or Razorpay `training.*` products (add to `pricing/`); consulting by milestone invoices from the Delivery Framework's milestone table. Until Razorpay is live: bank transfer plus a GST invoice from Zoho Books, and **Mark paid** in `/platform`. Refunds: Razorpay dashboard; policy text on the website; cohort refund rule: full before week 1, 50% before week 2, none after.

## 17. Infrastructure

Option A at launch: one VPS (api, worker, caddy), Cloudflare in front, R2 backups nightly, Bronze slices on a second host only when a Bronze pays, Silver/Gold from the generated compose file on their own VPS (applying it is GAPS #4, Sachin). Option C (two nodes, managed Postgres) when the first customer's business depends on uptime. Option D (customer cloud/on-prem) for Gold and regulated. Never Kubernetes at this size; GPU only for a Gold customer hosting open-weight models and billed to them.

## 18. Security

Secrets only in the server `.env` and Bitwarden; deploy key pair separate from personal keys; `ADMIN_TOKEN` 40+ random characters; tenant API keys stored as hashes and shown once; cohort keys expire and rotate; provider console caps before any key; CI secrets scan; Cloudflare proxy plus `ufw` 22/80/443; non-root user, password SSH off; backups nightly, restore test monthly; access revocation = cancel the tenant (key hash dead) and rotate any shared key; tenant isolation today is directory and namespace per tenant on one host (documented honestly; dedicated hosts for Silver/Gold). Rule printed on every classroom and customer document: **no customer or employer confidential data in classroom environments or classroom AI keys.**

## 19. Website (Harsh)

Immediate pages: readiness audit, demos, cohort one-page offer, AI services, AI consulting, workshops, training & mentorship (three tracks; only AI as an offering), contact, legal (terms, privacy, refund, student terms). Reads plans from `GET /api/platform/plans` and tracks from `GET /api/platform/registries`; never hard-codes prices. Later: sign-in that sends `X-Tenant-Key`. Detail: `website-patch/README.md`, `docs/WORK_SPLIT.md`.

## 20. Payments (audit of what exists)

| Item | State |
|---|---|
| Test mode | works end to end in tests (order → verify → grant/provision) |
| Live mode | key swap in `.env`; untested until Razorpay approves |
| Checkout | `/pay`, Razorpay Checkout; UPI under ₹2,000, virtual account above |
| Webhook | `/api/payments/webhook` (signature-verified) |
| Payment state | orders table; `/admin` lists; tenant state machine for platform products |
| Manual bank transfer | `/admin` mark paid (Quest); `/platform` **Mark paid** (tenants) |
| Invoice / GST | **missing** — Zoho Books by hand; automation is backlog B-12 |
| Provisioning trigger | verified payment with `tenant_id` → job; email fallback; mark-paid path |
| Refund | Razorpay dashboard only; no API path (acceptable) |
| Failed payment | order stays unpaid; tenant stays PAYMENT_PENDING; no email (backlog B-05) |

## 21. Legal

Needed before first payment: Terms of service, Privacy policy, Refund policy, Student terms and AI classroom policy (the three rules), NDA template. Before first corporate workshop: NDA signed, AI pass-through clause. Before production customer data: SOW (the Delivery Framework produces the draft), DPA, SLA per plan, IP and confidentiality clauses, data handling and residency statements from the corporate prerequisite record. Key management, secret management, backups, access revocation and tenant isolation are described in §18 and referenced from the DPA. One lawyer review (₹25,000) covers the templates; the Delivery Framework's governance output is framework-aligned guidance, not legal advice, and says so.

## 22. Cohort operations (manual first, software only where it saves founder time)

| Step | Now (manual, free) | Software when |
|---|---|---|
| Enrolment | Google Form → CRM sheet → bank transfer or Razorpay link | `training.*` products in the catalogue before cohort 2 |
| Payment | GST invoice from Zoho Books; Razorpay when live | — |
| Cohort and learners | `POST /api/platform/cohorts`, add emails; one key per cohort | done |
| Schedule and communication | Google Calendar invites, Meet, one WhatsApp or Discord group | — |
| Attendance | Meet attendance export → sheet | — |
| Assignments and submissions | Google Classroom (free) with `exercises.md`; GitHub repo per learner | — |
| Feedback | Google Form after each weekend | — |
| Learner progress | sheet: attendance, submissions, gateway usage (`/llm/usage`) | dashboard after cohort 3 |
| Certificate | PDF from the existing report engine with name, cohort, project URL | script in backlog B-09 |
| Alumni | WhatsApp group kept; LinkedIn group | — |
| Placement/career | Quest interview challenges; a "career" session in student cohorts; no placement promise | — |
| Project deployment | GitHub Actions + free-tier host; shared subpath under uniaiverse.ai for demos | — |

## 23. Consulting operations

Enquiry → discovery pack the same day (`/discovery`) → free readiness snapshot → Delivery Framework intake at `/delivery` (tier, plan, estimate, pack) → named legal review of the SOW → milestone invoices from the pack → pilot with a written stop rule and a success metric → G-gate reviews recorded in `/platform`… (delivery gates live in `/delivery`) → run service on a plan. Customer keys, customer cloud, customer data; never ours. Every engagement ends with a measured before/after that becomes a case study.

## 24. AI content management (versioned, no rebuilds)

| What | Where | Version field | Published by |
|---|---|---|---|
| Courses, modules, hours, outcomes | `training-materials/curriculum.yaml` | course `version` (add if absent) | `scripts/build_course_kits.py` + push |
| Lessons and labs | `training-materials/<course>/demos/NN_*.py` header + `say()` | git history; `demos/run_all.py` as the test | same |
| Projects | `training-materials/<course>/exercises.md` (generated) or hand-owned after removing the GENERATED line | git | same |
| Assessments | `training-materials/question_bank.yaml`, Quest bank | `version` | validator |
| Facilitator material | generated guide + handout | git | generator |
| Tools / models / providers / agents | `app/services/platform/content/registries/*.yaml` | `version`, `verified`, `status` | restart only |
| Prompts | inside demos and `labkit`; system prompts in `app/core/llm.py` | git | tests |
| Pricing/rates | `pricing/*.yaml`, `delivery/content/rate_card.yaml`, `llm_rates.yaml`, `registries/models.yaml` | `version`, `last_reviewed`, `verified` | validator + cost report |

Rule: content changes never need code changes. If they do, that is a bug for Sarfi to raise with Sachin/Harsh.

## 25. DevOps training management (Sachin)

Track status `draft` in `registries/tracks.yaml`. Material goes in `training-materials/tracks/devops/<course>/` using the same kit convention, created with `scripts/new_course.py --track devops`. It is taught inside the AI Engineer and student cohorts as the "ship it" weekends. It becomes a public offering only when Sarfi and Sachin set `status: final` and add a price to `pricing/tiers.yaml`.

## 26. Development / SDE training management (Harsh)

Same mechanics under `tracks/development/`. Language undecided (candidates in the registry). Harsh drafts module by module; Sarfi reviews; nothing is marketed until `final`. Harsh's own learning plan is part of the track: each module he writes, he first completes as a learner.

## 27. AI tool change process

Discover → evaluate (fit, cost, data policy) → security (what it can access) → privacy (where data goes) → cost (per user, per cohort) → sandbox (one mentor, one week) → test in one lab → approve (Sarfi) → version (`registries/tools.yaml`: status, owner, date) → publish (prerequisites, facilitator guide) → monitor (usage, learner feedback) → retire (`status: retired`, remove from prerequisites). File: `app/services/platform/content/registries/tools.yaml`. Reviewer: Sarfi; Sachin for anything touching servers.

## 28. Model change process

Verify (provider page, model id, dates) → pricing (INR per M in/out) → capability (which class) → benchmark (run `training-materials/ai-evals` demos 03 and 06 on the golden set) → cost (cost calculator, `llm_rates.yaml`) → provider policy (data use, residency) → gateway (`registries/models.yaml` class mapping) → budget (does the cohort pool still fit?) → approve → version (`verified` date). Then `python scripts/cost_report.py` and `pytest -q`. Retire by moving the old id to `retired`.

## 29. Agent change process

Prototype (labkit `agent.run_agent` with caps) → sandbox (offline policy) → evaluate (trajectory tests, `ai-evals` demo 05 pattern) → permissions (tools, scopes, destructive flags) → cost cap (`max_cost`, `max_steps`) → approve (Sarfi) → deploy (only inside a customer pilot with their key) → monitor (`llm_calls`, override rate) → retire. Registry: `registries/agents.yaml`; nothing runs unless `status: approved` and `where` includes the context.

## 30. Course change process

Draft (edit the demo or `curriculum.yaml`) → review (a second person reads the `say()` lines against the output) → lab test (`python demos/run_all.py`) → cost/prerequisite check (any LIVE minute added? update the pool estimate and the prerequisites) → version (bump `version` in the course entry; git) → publish (`build_course_kits.py`, push, CI green, merge) → monitor learner results (feedback form, gateway usage, assignment completion) → next iteration.

## 31. Customer proof

Target: three case studies by month 6, each with baseline, target, measured result at day 30 or 90, and the eval numbers. Cohort proof: attendance, projects deployed (URLs), hours saved reported at day 30. Publish on the website and in the discovery pack. Until then, the proof is the live product: every page is a demo.

## 32. Sales and distribution

Detail in `docs/GO_TO_MARKET.md`. Weekly: 5 outreach conversations from the CRM sheet, 1 lab-of-the-week post, 1 free 60-minute session offered. Monthly: 2 workshops (1 corporate, 1 college), 1 cohort open for enrolment. Partners: 2 implementation partners using the Delivery Framework packs. Twenty warm accounts each, Sarfi and Sachin.

## 33. Founder workload

Sarfi's hours are the scarcest input. Budget them: cohorts 8 h/weekend + 3 h prep; corporate workshop day 8 h + 6 h prep; pilot ≈ 6 h/week; sales 6 h/week; admin (`/admin`, `/platform`, invoices) 3 h/week; content 4 h/week. Two cohorts and one pilot at once is the ceiling. Anything beyond that needs a third trainer or licensing, not more hours.

## 34. Risks

| Risk | Signal | Mitigation |
|---|---|---|
| No customers, product keeps growing | weeks without a paid conversation | freeze features; the backlog gate is "a customer asked" |
| Free pool drained by a crowd | `FREE CAPACITY EXHAUSTED` | pool cap already stops spend; add per-IP limit before enforce |
| Cohort key abused | one learner far above others in `/llm/usage` | per-user caps; rotate key; enrolment rule |
| Provider price shock | `verified` date old, bills up | console caps; pass-through pricing; model class switch in the registry |
| Founder burnout | hours over §33 ceiling | say no; license; hire |
| Legal exposure | customer data in a classroom key | the rule, DPA, no customer data before enforce |
| Prices are placeholders | packs print the warning | edits A and B in the v2.5 playbook before quoting |

## 35. Launch sequence

1. Partnership agreement and legal templates (week 1). 2. Accounts: GitHub org, Cloudflare on the existing domain, email, vault (week 1). 3. Deploy in `log` mode; smoke test; backups; uptime (week 1–2, Sachin). 4. Razorpay KYC with GSTIN; bank transfer path ready (week 1). 5. Website pages (Harsh, weeks 1–3). 6. Announce cohort 1 six weeks out; 20 + 20 warm contacts (week 2). 7. Provider console cap; first cohort tenant and key rehearsal (week 3). 8. Deliver cohort 1; first workshop; first scoping engagement (weeks 6–10). 9. Publish results; open cohort 2 (week 11). 10. `enforce` when §15 criteria hold.

## 36. Recurring operating calendar

| When | Do | Owner |
|---|---|---|
| Daily 10 min | `/admin` approvals and unanswered bot questions; `/platform` requests | Sarfi |
| Weekly Monday | six numbers (seats, sessions, pilots, cash, hours, pool spend); top-user review in `/llm/usage`; CRM update | Sarfi |
| Weekly | server health, disk, backup success, restore spot-check log | Sachin |
| Per cohort | create cohort, set console cap, rotate key at end, export usage, feedback form, certificates | Sarfi (Sachin for keys) |
| Monthly | restore test on a laptop; `cost_report.py`; invoices with GST; registries `last_reviewed` | Sachin / Sarfi |
| Quarterly | LLM prices (`llm_rates.yaml`, `registries/models.yaml`), rate card, question bank and curriculum review, tool registry retire pass | Sarfi |
| Yearly | domain renewal reminder (2027), legal templates review | Sarfi |

## 37. Documentation and repository structure

`README.md` → this playbook → `docs/`: `HOW_TO_PLAYBOOK.md` (edit, test, ship), `PLATFORM_PLAYBOOK.md` (control plane, cost, GTM), `PLATFORM.md`, `COST_ANALYSIS.md` (generated), `GO_TO_MARKET.md`, `GAPS.md` (phased), `EDITING.md` (the edit table), `WORK_SPLIT.md` (Harsh/Sachin), `DEPLOY.md`, `DEPLOYMENT_STRATEGY.md`, `GIT_WORKFLOW.md`, `templates/`. Content: `app/services/platform/content/` (plans, capabilities, cost model, token policy, prerequisites, tooling, procurement, `registries/`), `app/services/delivery/content/`, `pricing/`, `training-materials/` (courses, `labkit`, `tracks/`).

## 38. Reusable templates

`docs/templates/CORPORATE_PREREQUISITES_TEMPLATE.md` · Delivery Framework packs (SOW, plan, estimate, governance, security — 26 documents) · discovery packs (5 segments) · student prerequisites checklist (`student_prerequisites.yaml`) · cohort feedback form (Google Form; questions: what did you ship, hours saved, what blocked you, NPS) · certificate (report engine) · case-study skeleton (situation, baseline, what we did, measured result, evals, what we would do differently).

## 39. Implementation backlog

| ID | Task | Owner | Dependency | Cost | Effort | Priority | Phase | Status | Completion criteria |
|---|---|---|---|---|---|---|---|---|---|
| B-01 | Sign a partnership agreement covering roles, revenue split, IP (repo stays with the company), decision rights, exit | Sarfi | lawyer | ₹ in legal review | 1 meeting | P0 | Now | open | signed PDF in the vault |
| B-02 | Legal pages: Terms, Privacy, Refund, Student terms + AI classroom policy; NDA template | Sarfi + lawyer | B-01 | ₹25,000 | 3 days | P0 | Now | open | pages live on the website; templates in `docs/templates/` |
| B-03 | Deploy v2.6.1 on a 2 vCPU VPS in `log` mode with Cloudflare, backups to R2, uptime alert; run the 5-minute smoke test | Sachin | accounts | ₹1,800/mo | 1 day | P0 | Now | open | `/api/health` shows 13 services; alert fired once in a drill |
| B-04 | Razorpay KYC with GSTIN 27AADCU8825H1Z0; test keys in `.env`; bank-transfer invoice template in Zoho Books | Sarfi | — | ₹0 | 2 h + wait | P0 | Now | open | test payment provisions a tenant; one GST invoice issued |
| B-05 | Transactional email: domain verified on Resend; emails for approved, pay link, active+key, quota 80%, expiry 7 days; failed payment | Sachin (infra) + Harsh (code) | B-03 | ₹0 | 2 days | P1 | Before first cohort | open | five emails sent from a test tenant |
| B-06 | `training.*` cohort products in `pricing/` and the payment catalogue; enrolment form → CRM sheet | Sarfi | B-04 | ₹0 | 1 day | P1 | Before first cohort | open | a seat can be bought in test mode |
| B-07 | Cohort rehearsal: create cohort, enrol 3 emails, set provider console cap, run the LIVE minutes of two labs through the gateway, hit a per-user cap on purpose, rotate the key | Sarfi | B-03 | ≤₹200 | 2 h | P1 | Before first cohort | open | usage visible in `/tenants/{id}/llm`; audit shows denial and rotation |
| B-08 | Assemble two syllabi from existing courses ("AI at Work" 4 weekends; "AI Engineer + ship it" 6 weekends incl. Sachin's DevOps weekend) with the LIVE/offline map per session | Sarfi + Sachin | — | ₹0 | 2 days | P1 | Before first cohort | open | two `syllabus.md` files under `training-materials/tracks/` |
| B-09 | Certificate script: PDF from the report engine with name, cohort, project URL, date | Harsh | — | ₹0 | 1 day | P2 | Before first cohort | open | `scripts/certificate.py` produces a PDF in tests |
| B-10 | Analytics on the website (Cloudflare Web Analytics) and the cohort funnel sheet | Harsh | website | ₹0 | 0.5 day | P2 | Before first cohort | open | weekly numbers filled from data |
| B-11 | Corporate prerequisite record filled for the first workshop customer; NDA signed; AI pass-through line on the quote | Sarfi | B-02 | ₹0 | 2 h | P1 | Before first corporate workshop | open | signed record in the vault |
| B-12 | Monthly pass-through invoice from the tenant dashboard spend (cost + 15%, GST) — script or Zoho export | Sarfi + Harsh | first tenant | ₹0 | 2 days | P2 | Before production customer data | open | one invoice generated from `/tenants/{id}` data |
| B-13 | Website sign-in that sends `X-Tenant-Key`; `/me` used for the user's quota display | Harsh | B-05 | ₹0 | 5 days | P1 | Before production customer data | open | a paid test tenant sees its plan on the site |
| B-14 | Per-IP rate limit on public demo paths | Sachin | B-03 | ₹0 | 1 day | P1 | Before production customer data | open | test: 20 rapid anonymous demo runs → 429 |
| B-15 | Tenant-scoped RAG on uploaded documents behind `file.upload`/`kb.create`/`rag.basic`, built inside the first paid pilot | Sarfi | a paying pilot | client budget | 10 days | P1 | Before production customer data | open | the client's questions answered from their documents with ACL filtering; evals ≥ launch bar |
| B-16 | Apply the generated compose file on a real dedicated host for a Silver tenant (SSH step in the worker) | Sachin | first Silver | pass-through | 5 days | P2 | Before production customer data | open | tenant answers `/api/health` on its own host |
| B-17 | DPA and SLA per plan; SOW template from the Delivery Framework reviewed once | Sarfi + lawyer | B-02 | in legal review | 2 days | P1 | Before production customer data | open | signed with the first production customer |
| B-18 | Switch `ENTITLEMENTS_MODE=enforce` per §15; record in audit | Sarfi + Sachin | B-13, B-14 | ₹0 | 1 h | P1 | Before production customer data | open | 14 days of clean logs; rollback drilled |
| B-19 | Postgres + pgvector migration | Sachin | >10 tenants or 2 nodes | ₹1,500/mo | 5 days | P3 | Later | open | tests pass on Postgres; restore tested |
| B-20 | Measured provider cost: monthly export from provider consoles reconciled with `llm_calls` | Sarfi | first cohort | ₹0 | 1 day | P3 | Later | open | variance < 10% |
| B-21 | Agent execution service behind `agent.run` with labkit caps | Sarfi | a pilot that needs it | client budget | 8 days | P3 | Later | open | trajectory tests pass; caps enforced |
| B-22 | Slack/email alerts from the nightly job (pool 70%, over-budget tenants, failed jobs) | Sachin | B-05 | ₹0 | 1 day | P3 | Later | open | one alert received in a drill |
| B-23 | Browser click-through of `/delivery`, `/platform`, `/register` with a checklist; fix what breaks | Harsh | B-03 | ₹0 | 0.5 day | P1 | Now | open | checklist ticked, bugs filed |
| B-24 | Founder-hour tracking sheet by activity (§33) | Sarfi | — | ₹0 | 1 h | P2 | Now | open | four weeks of data |
| B-25 | DevOps track: first course scaffold with two demos (Docker, deploy to VPS) | Sachin | B-08 | ₹0 | 3 days | P2 | Before first cohort | open | `run_all.py` prints ALL DEMOS OK; kit generated |
| B-26 | Development track: language decision memo and first module outline | Harsh + Sarfi | — | ₹0 | 2 days | P3 | Later | open | `tracks.yaml` updated; still `draft` until reviewed |

---

# MY NEXT 30 ACTIONS

| # | Exact action | Owner | Expected output | Dependency | Cost | Done when |
|---|---|---|---|---|---|---|
| 1 | Book one lawyer session for the partnership agreement and the legal templates (B-01, B-02) | Sarfi | appointment | — | ₹25,000 | invoice paid, date fixed |
| 2 | Create the GitHub organisation `The-UniAiverse`, private repo `ai-services`, add Sachin (owner) and Harsh (member); push `main`, `dev`, `features/sarfi` | Sarfi | repo online, CI green | — | ₹0 | six green CI checks |
| 3 | Move `uniaiverse.ai` DNS to Cloudflare (existing domain; buy nothing); set a 2027 renewal reminder | Sachin | Cloudflare active | — | ₹0 | site status "Active" |
| 4 | Create `admin@`, `support@`, and one mailbox each on Workspace or Zoho | Sarfi | 3 mailboxes | — | ₹1,950/mo | mail sent and received |
| 5 | Set up Bitwarden with a shared vault; store nothing outside it | Sachin | vault | — | ₹0 | 3 members, 5 secrets |
| 6 | Start Razorpay KYC with GSTIN 27AADCU8825H1Z0 (ARN AA270926111040M if asked); copy test keys into the vault | Sarfi | KYC submitted | 4 | ₹0 | dashboard shows "under review" |
| 7 | Ask the CA to set up Zoho Books with the GSTIN and one invoice template for training and one for consulting | Sarfi | invoice templates | — | ₹3,000/mo | a draft invoice exists |
| 8 | Buy the 2 vCPU / 4 GB VPS in an Indian region with the deploy SSH key; harden (non-root, ufw, no password SSH) | Sachin | server | 5 | ₹1,700/mo | `ssh` works with key only |
| 9 | Deploy v2.6.1 in `log` mode; A record `api` proxied; smoke test; `docker compose ps` shows api, worker, caddy | Sachin | live API | 8 | ₹0 | `/api/health` lists 13 services |
| 10 | Configure nightly encrypted backup to R2 and perform one documented restore on a laptop | Sachin | backup + restore log | 9 | ₹100/mo | restore note in `docs/` |
| 11 | Set UptimeRobot on `/api/health` with phone alert; stop the API for one minute to prove it | Sachin | alert | 9 | ₹0 | alert received |
| 12 | Set a monthly spend cap in the Anthropic (or OpenAI) console; then create the platform LLM key and put it in the vault and server `.env` | Sarfi | capped key | 5 | ₹800/mo | cap visible in console screenshot |
| 13 | Confirm day rates and LLM prices (v2.5 playbook edits A, B) and plan prices in `plans.yaml`; run `cost_report.py`; commit | Sarfi | no placeholder warnings | — | ₹0 | packs print no rate warning |
| 14 | Write the cohort one-page offer ("AI at Work", 4 weekends, price, outcome promise, refund rule) and the corporate workshop one-pager | Sarfi | two PDFs | 13 | ₹0 | sent to first 5 contacts |
| 15 | Harsh: legal pages, training & mentorship page (three tracks, AI as offering), cohort offer page, contact; `NEXT_PUBLIC_API_URL` set | Harsh | pages live | 2, 9 | ₹0 | pages load on uniaiverse.ai |
| 16 | Harsh: browser click-through checklist of `/delivery`, `/platform`, `/register`; file bugs | Harsh | checklist | 9 | ₹0 | checklist committed |
| 17 | Build the CRM sheet: 20 contacts each from Sarfi and Sachin, with segment and next action | Sarfi + Sachin | sheet | — | ₹0 | 40 rows |
| 18 | Send the first 10 messages offering a free 60-minute session on their team's real work | Sarfi | replies | 14, 17 | ₹0 | 10 sent, replies logged |
| 19 | Announce cohort 1 with a date six weeks out; Google Form enrolment; bank-transfer instructions | Sarfi | enrolment open | 14, 15 | ₹0 | first enrolment received |
| 20 | Assemble the "AI at Work" syllabus from existing courses with the LIVE/offline map (B-08) | Sarfi | `syllabus.md` | — | ₹0 | file committed |
| 21 | Sachin: DevOps weekend outline and first two demos (Docker, deploy) under `tracks/devops/` (B-25) | Sachin | kit | — | ₹0 | ALL DEMOS OK |
| 22 | Cohort rehearsal (B-07): create a test cohort, enrol 3 emails, run two LIVE labs through the gateway, hit a cap, rotate the key | Sarfi | usage report | 9, 12 | ≤₹200 | audit shows denial + rotation |
| 23 | Resend domain verification and the five transactional emails (B-05) | Sachin + Harsh | emails | 3, 9 | ₹0 | 5 test emails received |
| 24 | Google Classroom for cohort 1 with `exercises.md` as assignments; WhatsApp group; calendar invites | Sarfi | classroom | 19 | ₹0 | learners see week 1 |
| 25 | Certificate script (B-09) | Harsh | `scripts/certificate.py` | — | ₹0 | PDF generated in tests |
| 26 | Run 5 free sessions; convert to ≥1 corporate workshop booking and ≥1 Delivery Framework scoping engagement | Sarfi | bookings | 18 | ₹0 | signed quote or bank transfer |
| 27 | Fill the corporate prerequisite record and sign the NDA with the first workshop customer (B-11) | Sarfi | signed record | 26 | ₹0 | record in the vault |
| 28 | Deliver cohort 1; export gateway usage, attendance and feedback; measure hours saved at day 30 | Sarfi + Sachin | results sheet | 19–24 | ≤₹20,000 pool | numbers published |
| 29 | Write case study #1 from the cohort or the scoping engagement; put it on the website and in the discovery pack | Sarfi + Harsh | case study | 28 | ₹0 | page live |
| 30 | Review §15 criteria; if all hold, switch `ENTITLEMENTS_MODE=enforce` with a rollback drill first; otherwise stay in `log` and list what is missing | Sarfi + Sachin | decision in audit log | B-13, B-14 | ₹0 | audit entry written |

---

# HOW I KEEP UNIaiVERSE EVOLVING

Every workflow: **where / who reviews / what to test / how to version / how to publish / how to roll back.** The test and publish steps are always the same two commands (`python scripts/validate_content.py`, `python -m pytest -q`) then `./scripts/push_to_github.sh "…"` → pull request → merge; rollback is always "revert the merge on GitHub" unless stated.

| Workflow | Where | Reviewer | Test | Version | Publish | Rollback |
|---|---|---|---|---|---|---|
| Add an AI tool | `content/registries/tools.yaml` (§27 steps) | Sarfi; Sachin if it touches servers | one lab uses it; prerequisites updated | `status`, `last_reviewed` | push; prerequisites go out at next enrolment | set `status: retired` |
| Replace an AI tool | same file: old → `retired`, new → `approved`; update `student_prerequisites.yaml` and facilitator guides that name it | Sarfi | affected course `run_all.py` | same | same | flip the two statuses back |
| Add a model | `registries/models.yaml` class mapping + prices; `delivery/content/llm_rates.yaml`; `llm-cost/cost_calculator.py` RATES | Sarfi | ai-evals demos 03/06 on the golden set; `cost_report.py`; pytest | `verified` date | push | restore previous id in the class |
| Change model pricing | the three files above | Sarfi | `cost_report.py`; pytest (cost model must add up) | `verified` | push (CI checks COST_ANALYSIS matches) | revert |
| Add an agent | `registries/agents.yaml` + code under labkit or a pilot repo (§29) | Sarfi | trajectory tests; caps hit in a drill | `status`, `caps` | push; deploy only in the customer's environment | `status: retired`; remove from `where` |
| Remove an agent | `status: retired`, `where: []` | Sarfi | pytest | same | push | restore |
| Add RAG capability | `capabilities.yaml` (+ guard paths), plan `capabilities`, code in the pilot | Sarfi | golden-set evals ≥ launch bar; refusal correct | `capabilities.yaml` version | push; plan change applies on restart | remove the capability from the plan |
| Change token budgets | `plans.yaml → classroom.cohort` and `token_policy.yaml` together; one cohort: `PATCH /tenants/{id}/limits` with a reason | Sarfi | `test_gateway.py` checks the two files agree | `version` | restart (global) / immediate (one cohort) | revert file or PATCH back |
| Add a provider | `registries/providers.yaml`; `app/core/llm.py` branch; `LLM_PROVIDER` in `.env`; console cap set first | Sarfi + Sachin | `complete_with_usage` returns tokens; gateway test | `version` | `.env` change + restart | switch `LLM_PROVIDER` back |
| Change plan pricing | `plans.yaml` fees; `pricing/tiers.yaml`; website reads the API | Sarfi | pytest (golden quotas), `cost_report.py`, validator | `version`, `last_reviewed` | restart; price page updates itself | revert |
| Change quotas | `plans.yaml` limits; per tenant via console | Sarfi | `test_platform.py` numbers; update tests on purpose | same | restart / immediate | revert / PATCH |
| Add or edit course content | `curriculum.yaml`, `demos/NN_*.py`, hand-owned guides (§30) | a second reader | `run_all.py`; validator | course `version`; git | `build_course_kits.py` + push | revert commit; regenerate kits |
| Add a training project | `exercises.md` (hand-owned) or a new demo with a `Lab:` line; deployment target in the syllabus | Sarfi | run it end to end once, including deploy on a free tier | git | push | revert |
| Change DevOps curriculum | `training-materials/tracks/devops/`, `registries/tracks.yaml` modules | Sachin drafts, Sarfi reviews | `run_all.py` | `tracks.yaml` version; `status` stays `draft` until final | push; website shows offerings only when `final` | revert |
| Change Development/SDE curriculum | `tracks/development/`, `tracks.yaml` (language undecided) | Harsh drafts, Sarfi reviews | same | same | same | same |
| Update website content | Harsh's repo; prices and tracks come from the API, never typed in | Sarfi for wording that promises anything | preview deploy on Vercel | git | merge → Vercel deploy | Vercel "promote previous deployment" |
| Update legal documents | website legal pages; `docs/templates/` for SOW/DPA/SLA/NDA | lawyer for material changes; Sarfi otherwise | read-through; version date on the page | dated version line at the top | publish; customers on old terms are told | restore the previous dated version |
| Release software | `features/<name>` → PR → `dev` → weekly `main` | CI + one human review | CI's six checks; smoke test on the server | git tag `vX.Y.Z`; `app/main.py` version; CHANGELOG | merge to `main` deploys with health check | automatic rollback if unhealthy; else revert the merge or check out `backup/main-<date>` |
| Roll back software | GitHub | Sachin | `/api/health`; smoke test | the tag you return to | revert merge → deploys | n/a |

If a change needs code for something that should be data, stop and fix the data path first. That is how the system stays editable by you without a rebuild.
