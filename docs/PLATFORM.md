# The control plane (v2.6) — tenants, approval, entitlements, quotas, provisioning

uniAIverse is a controlled showcase plus a controlled-access platform, not an open SaaS. Five ideas are kept separate: **account ≠ access ≠ plan ≠ entitlement ≠ resource.**

```
visitor → /register → PENDING → admin approves → plan assigned
   free  → PROVISIONING → ACTIVE (tiny shared sandbox slice, counted against ONE pool)
   paid  → PAYMENT_PENDING → Razorpay verify / webhook / mark-paid → PROVISIONING (background job) → ACTIVE (allocated environment)
ACTIVE → SUSPENDED | QUOTA_EXCEEDED | EXPIRED | CANCELLED  (state machine in plans.yaml `transitions`; anything else is refused and audited)
```

| Piece | Where | What it does |
|---|---|---|
| Plans as resource profiles | `app/services/platform/content/plans.yaml` | free sandbox pool + per-user limits; Bronze/Silver/Gold: fees, users, queries, context, storage, vector, knowledge bases, agent tool calls, documents, GPU allocation wording, isolation, spend limit, SLA, capabilities |
| Capabilities | `…/content/capabilities.yaml` | every guarded thing, its unit weight, its approximate cost to us, and which URL paths it guards |
| Entitlement engine | `engine.check()` · `POST /api/platform/check` | one answer for "may tenant T do C now?": state, plan, monthly/daily quota, spend limit, document limit, free pool |
| Enforcement | middleware in `app/main.py`, `ENTITLEMENTS_MODE` | `off` · `log` (default: check, record, always allow, `X-Entitlement` header) · `enforce` (402 beyond plan or pool, 401 on a bad key). Anonymous callers get the public sandbox: demos and free tools only, counted against the free pool |
| Provisioning | `engine.run_jobs()` · `scripts/provision_worker.py` · `worker` container | queued jobs; idempotent steps: tenant dir, database, vector namespace, storage namespace, environment file (+ generated `docker-compose.tenant.yml` for Silver/Gold), API key (hash stored, shown once), quotas, admin user, activate |
| Admin console | `/platform` | requests, approve/reject with plan, sandbox pool, tenants, dashboard (users, queries, storage, spend, projection), change limits and capabilities with a reason and **no redeploy**, state moves, mark paid, provisioning, nightly, cost model, audit |
| Public | `/register`, `GET /api/platform/plans`, `GET /api/platform/status/{id}?email=` | request access; the website reads plans from the API, never hard-codes them |
| Payments | `platform.<plan>` and `platform.<plan>.setup` in the catalog; `tenant_id` on the order | a verified payment provisions the tenant; bank transfers use "Mark paid" |
| Cost model | `…/content/cost_model.yaml` · `GET /api/platform/cost-model` · `scripts/cost_report.py` → `docs/COST_ANALYSIS.md` | fixed cost, per-plan unit economics, break-even, P&L at a mix, sensitivity |

**What a tenant environment is today.** A directory under `outputs/tenants/<id>/` with its own SQLite file, vector and storage namespaces, an `.env.tenant`, and for Silver/Gold a generated compose file to deploy on a dedicated host. The customer-facing services (RAG on tenant documents, agents, knowledge bases) are **not yet built** — see `docs/GAPS.md`. The control plane is complete and tested so those services can be added behind `engine.check()` one at a time.

**Rollout of enforcement.** Stay in `log` while Harsh adds the `X-Tenant-Key` header after sign-in; watch `X-Entitlement` headers and the usage table; then set `ENTITLEMENTS_MODE=enforce`. Public demos keep working in `enforce` until the free pool is spent.
