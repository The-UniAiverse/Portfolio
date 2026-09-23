# What is still missing — honest list (v2.6)

Ordered by what unblocks revenue first. Effort is engineering days for one experienced developer.

| # | Gap | Why it matters | Effort | Owner |
|---|---|---|---:|---|
| 1 | **Customer sign-in on the website** that sends `X-Tenant-Key` (or a session mapped to it) | Without it enforcement stays in `log` mode and paid tenants use the same public pages as everyone | 3–5 | Harsh |
| 2 | **Tenant-scoped RAG on uploaded documents** (`file.upload`, `kb.create`, `rag.basic`) wired to the tenant's vector namespace and storage prefix | This is what Bronze customers buy; today the RAG demo runs only on preloaded documents | 8–12 | Sarfi/Sahil |
| 3 | **Email notifications** (approved, pay link, active with API key, quota at 80%, expiry in 7 days) | Today the admin console shows the pay link; the customer must be emailed by hand | 2 | Sarfi |
| 4 | **Real dedicated provisioning** for Silver/Gold: the generated `docker-compose.tenant.yml` must be deployed on a host (Ansible/SSH step in the worker) | Today the file is generated, not applied | 4–6 | Sahil |
| 5 | **Postgres + pgvector** replacing SQLite and the directory namespaces once there are more than ~10 tenants or two API nodes | SQLite is fine for launch; it does not survive two nodes | 5 | Sahil |
| 6 | **Per-request cost from real provider bills** feeding `tenant_usage.cost_inr` instead of `approx_cost_inr` | Margins in COST_ANALYSIS are modelled, not measured | 3 | Sarfi |
| 7 | **Rate limiting per IP** on public demo paths in `enforce` mode (today the free pool is the only brake) | A crowd exhausts the pool for everyone in one afternoon | 1 | Sarfi |
| 8 | **Agent execution service** with the labkit caps behind `agent.run` | Silver/Gold capability that is sold but not yet served | 6–8 | Sarfi |
| 9 | **Invoice generation** for infrastructure pass-through (cost + 15%) and GST | Platform fee is via Razorpay; infra is invoiced manually | 3 | Sarfi + accountant |
| 10 | **Terms, DPA, SLA documents** for each plan | Gold promises a contractual SLA | — | Legal |
| 11 | Monitoring beyond uptime: usage/spend alerts to Slack or email from the nightly job | The dashboard shows the risk; nobody is paged | 1 | Sarfi |
| 12 | The `/platform` and `/register` pages were syntax-checked and their APIs tested; nobody has clicked through them in a browser yet | Same as `/delivery` in v2.5 | 0.5 | Sarfi |

Not gaps, decisions still open (D1–D8 in the Delivery playbook): day rates, LLM prices, whether Bronze runs on the control-plane host or a separate customer host, GPU policy.

## Phase classification (2026-09-24)

| Phase | Items |
|---|---|
| **Now** (before first revenue) | deploy in `log` mode · Razorpay KYC started, bank transfer + GST invoice for early customers · Terms/Privacy/Refund/Student terms · price list and one-page offers · CRM sheet · partnership agreement · procurement rows marked "required now" |
| **Before first cohort** | LLM gateway (done in v2.6.1) · cohort created and learners enrolled · provider console cap set · transactional email for keys and receipts · student prerequisites sent at enrolment · Google Classroom + Meet + WhatsApp set up · certificate template · analytics |
| **Before first corporate workshop** | corporate prerequisite record filled · NDA template · workshop pass-through line for AI usage · uptime alert on |
| **Before production customer data** | customer sign-in with tenant key (#1) · tenant-scoped RAG (#2) · real dedicated host for Silver/Gold (#4) · per-IP rate limit on public demos (#7) · DPA + SLA · key rotation and access-revocation runbook · `ENTITLEMENTS_MODE=enforce` |
| **Later** | Postgres/pgvector (#5) · measured provider cost (#6) · agent execution service (#8) · infra invoicing automation (#9) · Slack/email alerts (#11) |
| **Scale later** | redundancy, managed DB, GPU, enterprise monitoring — each tied to the trigger in `procurement.yaml` |
