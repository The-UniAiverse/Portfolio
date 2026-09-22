# uniAiVerse v2.6 — Platform Playbook (control plane, cost, go-to-market)

*For Sarfi. Plain language. 22 September 2026. Companion to `HOW_TO_PLAYBOOK.md` (edit, test, ship) which still applies in full.*

## 1. What this version is

v2.5 gave you an engine with many faces. v2.6 puts a **gate** in front of the expensive parts. A feature existing is no longer the same as a visitor being allowed to use it. Five things are now separate: an account, access, a plan, an entitlement, a resource.

What changed: a control plane service (`/platform` admin console, `/register` public page), plans written as resource profiles, an entitlement engine and quotas, a capped free sandbox, background provisioning with a worker, a cost model that writes its own document, and three documents: `PLATFORM.md`, `COST_ANALYSIS.md`, `GO_TO_MARKET.md`, `GAPS.md`.

What was tested: 78 automated tests (71 from v2.5 unchanged, 7 new covering the full lifecycle, quotas, the state machine, the pool, enforcement and the cost model). Everything from v2.5 still runs. What was not tested: the two new pages in a real browser; a real dedicated host for a Silver/Gold tenant; email.

## 2. The customer lifecycle, click by click

1. A visitor fills `/register` (organisation, name, email, plan, purpose). They get an id `TEN-…` and state **PENDING**. Nothing is provisioned.
2. You open `/platform`, paste the admin token, click **Load**. The request appears with the purpose text. Choose a plan or keep the requested one. **Approve** or **Reject**.
3. Free plan: the environment is created in the background and the tenant becomes **ACTIVE** within seconds. The API key appears in the provisioning job output once; give it to the customer.
4. Paid plan: state **PAYMENT_PENDING** and a pay link is shown. Send it. When Razorpay confirms, provisioning starts by itself. Bank transfer: open the tenant, click **Mark paid**.
5. **ACTIVE**: the dashboard shows users, queries, storage, spend to date and projected spend against the budget.
6. Change any limit or add/remove a capability with a reason. It applies on the next request. No redeploy.
7. Suspend for non-payment, reactivate, cancel: buttons on the tenant; every move is audited and impossible moves are refused.
8. The nightly job expires tenants past their date and resets quota-exceeded ones on the 1st. The worker container runs it; **Run nightly** in the console runs it by hand.

## 3. Plans are resource profiles

Everything about a plan is in `app/services/platform/content/plans.yaml`: fee, setup fee, infrastructure estimate, users, concurrency, queries per month, context size, storage, vector storage, knowledge bases, agent tool calls, documents per month, GPU wording, isolation, spend limit, SLA, capabilities. Change a number there and every tenant on that plan changes; change it on one tenant in the console to make an exception. The free sandbox is one shared pool: 2,000 queries or ₹2,000 a month, at most 200 approved users. When it is spent the API says `FREE CAPACITY EXHAUSTED` and approvals stop. **Pause free approvals** in the console does the same by hand.

## 4. Enforcement, in three steps

`.env` → `ENTITLEMENTS_MODE`. `log` (today): every guarded call is checked and recorded, always allowed, and answers carry an `X-Entitlement` header you can read. `enforce`: calls beyond the plan or the pool get a 402 with the reason and the upgrade link; anonymous visitors may only run demos and free tools. Switch to `enforce` only after Harsh sends `X-Tenant-Key` after sign-in (GAPS #1). `off` disables everything.

## 5. Cost, in one paragraph

Fixed cost is about ₹4,900 a month including the ₹2,000 free-sandbox cap. Gross margin per tenant at full quota: Bronze about ₹15,900, Silver about ₹44,200, Gold about ₹94,500, because infrastructure is billed at cost + 15% and LLM spend is capped per tenant. One Bronze tenant covers the fixed cost. At 4 Bronze + 2 Silver the operating result is about ₹1.47 lakh a month before your own time. Every figure is a placeholder until you confirm hosting and prices; the full tables, break-even and sensitivity are in `docs/COST_ANALYSIS.md`, generated from the same file the API uses.

## 6. Go to market: see `docs/GO_TO_MARKET.md`

Door-openers are free (snapshot, sandbox, discovery pack). First paid step is small (a Bronze Delivery Framework engagement or a Bronze platform). Two workshops a month, one lab post a week, 20 warm accounts, two partners. 90-day target: 4 Bronze and 1 Silver tenants.

## 7. Deploy and go live

Same as v2.5 plus one container: `deploy/docker-compose.prod.yml` now runs `worker` next to `api`. `docker compose -f deploy/docker-compose.prod.yml up -d --build` starts both. Check `/api/health` lists 13 services including `platform`. Then: register a test tenant at `/register`, approve it at `/platform`, watch it become ACTIVE, delete it (cancel). Options A–D and their cost are in `COST_ANALYSIS.md` section 7.

## 8. Ship it

`./scripts/push_to_github.sh "platform: …"` → pull request → merge. CI now also checks that `COST_ANALYSIS.md` matches the cost model.

## 9. What is missing

`docs/GAPS.md`: sign-in with tenant key (Harsh), tenant RAG on uploaded documents, email, real dedicated hosts, Postgres, measured costs, IP rate limits, agent service, invoicing, legal documents, alerts, browser click-through.

## 10. Edit table and troubleshooting

| Change | File |
|---|---|
| Plan fees, quotas, capabilities, states | `app/services/platform/content/plans.yaml` |
| Which URLs a capability guards, unit weights, cost per call | `…/content/capabilities.yaml` |
| Infrastructure rate card, markup, fees | `…/content/cost_model.yaml` → `python scripts/cost_report.py` |
| Enforcement mode | `.env` → `ENTITLEMENTS_MODE` |
| Where tenant environments are written | `.env` → `TENANTS_DIR` (back it up) |

| You see | Do |
|---|---|
| 422 "free sandbox is at capacity or paused" on approve | Approve a paid plan, wait for next month, or **Resume** approvals |
| 422 "cannot move X → Y" | The state machine refused; read the allowed moves in the message |
| Tenant stuck in PROVISIONING | Open the tenant → Provisioning jobs → error; fix; **Run provisioning now** |
| 402 on the website | Expected in `enforce` mode: not in plan or quota reached; the body has the reason |
| Payment paid but tenant still PAYMENT_PENDING | The order lacked `tenant_id` and the email did not match; use **Mark paid** |
