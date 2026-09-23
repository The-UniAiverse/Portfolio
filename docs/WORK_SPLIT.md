> **Team and positioning (2026-09-24).** Sarfi: AI, AI architecture, consulting, content, product, commercial. Sachin: DevOps, deployment, infrastructure. Harsh: intern — development / SDE, programming, software engineering; his curriculum is a draft. Public business = AI (services, consulting, readiness, assessments, workshops, demos, platform). Training & Mentorship = AI (Sarfi) + DevOps (Sachin) + Development (Harsh); DevOps and Development are **not** standalone public service pages yet. Sachin now owns the server, deploy, backups and monitoring sections below; Harsh owns the website build.

# uniAIverse — who builds what

*20 September 2026 · working agreement between Sarfi and Harsh*

Two people, one product. The rule: **each capability has exactly one owner.** The other person reviews, never rebuilds. Where something already exists in the API, the website calls it rather than re-implementing it.

---

## Harsh owns — the website and everything a visitor touches first

**1. Services section**
- Services landing page and one page per service/product, each with relevant projects, use cases and success stories.
- A separate Success Stories page bringing together all case studies across products and services.
- Service pages pull live data (tiers, prices, engagement phases, course lists) from the API endpoints listed at the end — no hard-coded prices on the site.

**2. Demo & Playground sections**
- **Demo section:** the gallery of what we've built — layout, navigation, copy, screenshots, success metrics. The runnable demos themselves are served by the API at `/demos`; the website embeds or links them.
- **Playground section:** the visitor-facing interactive space and its freemium gate — sign-up, usage limits, upgrade prompts, the paid-access flow. The chatbot behind it is the uniAI assistant already in the API; the Playground's UI, accounts and limits are Harsh's.

**3. Backend & admin portal**
- Authentication portal (sign-up, login, password reset, roles) for visitors, Quest users and staff.
- Ticket-raising system — users raise and track issues; internal assignment and status flow.
- Telegram notifications on new tickets and important events.
- **Super Admin panel** for Harsh and Sarfi covering users, tickets, content approvals, payments view. The existing lightweight `/admin` page in the API is a stop-gap; it retires into the Super Admin panel once that exists.
- Website database (MySQL/Postgres), hosting on Vercel, environment variables, domain.

**4. AI Engineering news & newsletter**
- Daily fetch and summary of the top five AI engineering articles, published on the website.
- Newsletter: subscriber list, daily morning email, unsubscribe, deliverability.
- Voice-note version of the newsletter.
- The API's existing news feed (RSS → pending → approve → feed, used by Quest) merges into this: Harsh's pipeline becomes the single source, and Quest reads from it.

**5. Website assistant (uniAI)** — the widget and its placement on the site, greeting, styling. Its answers come from the API's knowledge base; adding answers is a content edit either of us can make.

---

## Sarfi owns — the AI services API and the delivery content

**1. Consulting engines** — AI Readiness Audit (348-question framework, 5 tiers, PDF reports), Strategy & Roadmap, Governance & Compliance, Automation & ROI. Methodology, question banks, scoring, report generation.

**2. Training & Mentorship** — curriculum (23 courses, tracks, certifications), the Agentic AI & LLM Economics workshop and its six audience editions (corporate, business, university, college, non-technical, domain), all runnable demos, facilitator guides, exercises, handouts, decks.

**3. Course Finder** — profile/CV → recommended track, free vs paid depth.

**4. uniAI Quest** — quiz engine, question bank, interview challenges, XP and tiers, mentor sessions. (Account creation and the paid gate move to Harsh's auth once it exists; until then Quest uses its own lightweight user id.)

**5. Payments** — Razorpay integration, method rules (UPI under the limit, cards, netbanking, NEFT/RTGS/IMPS), webhooks, tier grants. Harsh's Playground and ticketing call these endpoints for anything that charges money.

**6. Discovery kit** — enquiry → discovery-questions document per segment (corporate, business, university, college, domain) and service, in PDF/Word.

**7. API platform** — deployment of `api.uniaiverse.ai`, backups, monitoring, the content-validation and release process for the repo.

---

## Boundaries, in one line each

| Topic | Owner | The other person… |
|---|---|---|
| Anything a visitor sees on uniaiverse.ai | Harsh | supplies content and reviews |
| Anything that scores, recommends, generates a report or a quiz | Sarfi | consumes it via the API |
| Accounts, login, roles | Harsh | Sarfi's services accept the user id Harsh issues |
| Money | Sarfi (gateway) | Harsh (checkout UX and receipts on the site) |
| News content | Harsh (pipeline + newsletter) | Sarfi's Quest reads the approved feed |
| The chatbot's answers | Sarfi (knowledge base) | Harsh (widget, placement, Playground gate) |
| Admin | Harsh (Super Admin panel) | Sarfi's `/admin` retires into it |

## Endpoints the website calls (all live today)

`/api/pricing/tiers` · `/api/pricing/blueprint` · `/api/pricing/proposal` — prices and engagement phases for service pages
`/api/training/curriculum` · `/api/training/tracks` — course catalogue
`/api/training/course-finder` — Course Finder
`/api/readiness_audit/questionnaire?tier=free` · `/api/readiness_audit/run` — free snapshot
`/api/demos` · `/api/demos/run/{id}` · `/api/demos/rag/ask` — Demo section
`/api/demos/courses` · `/api/demos/run-course/{course}/{demo}` — a runnable lab catalogue for every course page (108 demos; the server only runs scripts it discovered itself)
`/api/delivery/config` · `/api/delivery/sample?tier=` · `/api/delivery/run` · `/api/delivery/pack` · `/api/delivery/file/{name}` — AI Delivery Framework (public, no storage). `/api/delivery/intake`, `/engagements`, `/gates/*` need `X-Admin-Token` and are for the internal page only — never call them from the public site.
`/api/quest/*` — Playground quizzes and challenges
`/api/bot/config` · `/api/bot/chat` — uniAI assistant
`/api/payments/catalog` · `/api/payments/order` · `/api/payments/verify` — checkout
`/api/discovery/generate` — internal, for enquiries
`/api/platform/plans` · `POST /api/platform/register` · `/api/platform/status/{id}?email=` — price page and access requests (public). After sign-in send `X-Tenant-Key` on every call; read `/api/platform/me` for what the user may do and how much is left. Never call `/api/platform/requests|approve|tenants|...` from the website (admin token).

Full reference: `https://api.uniaiverse.ai/docs`

## Working rhythm
- Branches: `features/harsh` and `features/sarfi` → `dev` → `main`. PR into `dev` reviewed by the other person. `main` deploys.
- Weekly 30-minute sync: what shipped, what's blocked, any new overlap — and the overlap goes to whoever already owns the nearest capability.
- New capability nobody owns yet → decided in that sync, written into this document.
