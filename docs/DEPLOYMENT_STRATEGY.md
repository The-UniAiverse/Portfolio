# Deployment strategy — uniaiverse.ai

Goal: smooth for every visitor, no lag on the demo pages, survives a server failure, costs under ₹10k/month at launch, and one person can run it.

## 1. Shape

```
uniaiverse.ai  ──── Vercel (Next.js site: pages, uniAI widget, Harsh's backend)
      │
      │  NEXT_PUBLIC_API_URL
      ▼
api.uniaiverse.ai ─ Cloudflare (DNS, HTTPS, CDN cache for /static and GET endpoints, WAF, DDoS)
      │
      ▼
  App server (Docker: FastAPI + Caddy)  ──  SQLite today → Postgres when >1 server
      │                                 └─  outputs/ (reports, DB) → nightly copy to object storage
      └── LLM / Razorpay / RSS calls go out; nothing sensitive is stored on the server except .env
```

Three principles: **stateless app** (all state in the DB and object storage so a server can be replaced in minutes), **cache everything that is public** (the demo pages, the question banks, the catalogues are the same for everyone), and **run demos with limits** (timeouts, one worker pool, so a heavy demo never slows a form for someone else).

## 2. Options and monthly cost (September 2026 list prices; check before buying)

| Option | Fits | What runs where | ₹/month approx. | Notes |
|---|---|---|---|---|
| **A. Launch** (recommended now) | Up to ~5k visitors/day, a few hundred demo runs/day | Vercel Hobby/Pro for the site; **one VPS** (Hetzner CX22 / DigitalOcean 2 vCPU 4 GB) for the API; Cloudflare Free; Backblaze B2 or Cloudflare R2 for backups | Site ₹0–1,700 · VPS ₹450–2,000 · CDN ₹0 · backups ₹0–100 · domain ₹100 · **≈ ₹1,500–4,000** | SQLite with nightly backups. Redundancy = snapshots + rebuild script (10 minutes). Fine for launch. |
| **B. Managed PaaS** | Same scale, zero server admin | Railway / Render / Fly for the API container; managed Postgres | API ₹600–2,500 · Postgres ₹0–1,600 · **≈ ₹2,000–5,000** | Simplest to run; cold starts on the cheapest tiers, keep one instance always on. |
| **C. Redundant** | When paying customers depend on it | 2 API VPS behind a load balancer (Hetzner LB ₹500) or Cloudflare load balancing; managed Postgres (Neon / Supabase / DO ₹1,300–2,500); R2 for files; uptime monitoring | **≈ ₹6,000–12,000** | No single point of failure. Move here when Quest subscriptions pass ~₹50k/month. |
| **D. India-resident** | Enterprise clients that require data in India | Same as C on AWS Mumbai (t4g.small ×2, RDS Postgres, S3) or DigitalOcean Bangalore | **≈ ₹10,000–20,000** | Only when a contract demands it; A–C on Hetzner/DO already serve India well through Cloudflare's Mumbai edge. |

Variable costs on top: LLM API for narratives and bot polish ₹400–2,000/month at website volumes (everything works with none); Razorpay ~2% + GST per transaction; email (Resend / SES) ₹0–800.

## 3. Reliability design (applies to every option)

| Concern | What we do |
|---|---|
| Server dies | Docker image + `deploy/` config rebuild anywhere in ~10 min; nightly DB + outputs backup to object storage; weekly VPS snapshot. Option C removes the downtime entirely. |
| Slow pages | Cloudflare caches `/static/*`, `/api/readiness_audit/questionnaire`, `/api/training/curriculum`, `/api/quest/tiers`, `/api/pricing/*` at the edge (public, identical for everyone). Uvicorn with 2–4 workers. Demo runs capped at 90 s and run in a subprocess so they never block the API. |
| Traffic spike | Cloudflare absorbs it; rate limits per IP on `/api/demos/run/*` and `/api/quest/quiz`. |
| Bad deploy | `backup-before-merge` snapshots `main`; deploy workflow keeps the previous image; rollback = re-run with the last tag. |
| Secrets | Only in the server `.env` and GitHub Actions secrets; never in the repo. |
| Payments | Razorpay is the source of truth via webhook; the DB mirrors status; card data never touches us. |
| Monitoring | UptimeRobot / Better Stack free tier on `/api/health`; Sentry free tier for errors; Cloudflare analytics for traffic. |
| Growth | SQLite → Postgres is a config change (`db.py` keeps the same functions); files → R2 by changing `outputs_dir` to a mounted bucket. |

## 4. Launch checklist (Option A)

1. VPS with Ubuntu 24 + Docker. Clone the repo to `/srv/uniaiverse-ai-services`.
2. `.env` from `.env.example`: `PUBLIC_URL=https://api.uniaiverse.ai`, `CORS_ORIGINS=https://uniaiverse.ai,https://www.uniaiverse.ai`, `ADMIN_TOKEN`, Razorpay keys, optional LLM key.
3. `docker compose -f deploy/docker-compose.prod.yml up -d --build`. Check `/api/health`.
4. Cloudflare: DNS `api` → VPS IP (proxied), SSL Full (strict), cache rules for the paths above, rate-limit rule on `/api/demos/run/*` (30/min/IP).
5. Vercel: `NEXT_PUBLIC_API_URL=https://api.uniaiverse.ai`; apply `website-patch/`.
6. GitHub secrets: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY`, `API_URL`, `ADMIN_TOKEN`. Merge to `main` deploys.
7. Backups: cron `0 2 * * * /srv/uniaiverse-ai-services/deploy/backup.sh` (copies `outputs/` to the bucket, keeps 30 days). Test a restore once.
8. Razorpay webhook → `/api/payments/webhook`; Smart Collect enabled; UPI limit set.
9. Uptime monitor on `/api/health`, alert to email/Telegram.

## 5. When to move up
- Sustained >2k demo runs/day or p95 API latency >800 ms → Option C (second server + Postgres).
- First enterprise contract with residency clauses → Option D.
- Quest subscriptions >₹50k/month → Option C regardless of load; downtime now costs money.
