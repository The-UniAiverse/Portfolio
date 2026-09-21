# Deploying to uniaiverse.ai

Architecture: the Next.js site stays on Vercel at `uniaiverse.ai`. This API runs at `api.uniaiverse.ai` on one small VPS (2 vCPU / 2 GB is enough).

1. **Server:** Ubuntu 24, Docker + Compose. `git clone git@github.com:The-UniAiverse/ai-services.git /srv/uniaiverse-ai-services`.
2. **DNS:** `A api.uniaiverse.ai → <server IP>`. Caddy issues HTTPS automatically.
3. **Env:** `cp .env.example .env` and fill: `CORS_ORIGINS=https://uniaiverse.ai,https://www.uniaiverse.ai`, `PUBLIC_URL=https://api.uniaiverse.ai`, `ADMIN_TOKEN`, Razorpay keys when the merchant account is approved, optional LLM key.
4. **Run:** `docker compose -f deploy/docker-compose.prod.yml up -d --build`. Check `https://api.uniaiverse.ai/api/health`.
5. **Website:** apply `website-patch/` (uniAI bot, links, `NEXT_PUBLIC_API_URL`). Vercel env var `NEXT_PUBLIC_API_URL=https://api.uniaiverse.ai`.
6. **Razorpay:** Dashboard → Webhooks → `https://api.uniaiverse.ai/api/payments/webhook`, events `payment.captured`, `order.paid`, `virtual_account.credited`; put the secret in `RAZORPAY_WEBHOOK_SECRET`. Enable Smart Collect for NEFT/RTGS/IMPS virtual accounts. Set the UPI limit in `UPI_LIMIT_INR` (default 2000).
7. **Delivery Framework:** works with no extra setup (`delivery` is in `ENABLED_SERVICES`). Saved engagements and gate records need `ADMIN_TOKEN`. Before quoting a client, confirm `app/services/delivery/content/rate_card.yaml` and `llm_rates.yaml` — until then every pack prints a "placeholder rates" warning. Generated packs are written to `outputs/delivery/` (include in backups).
7a. **Backups:** `outputs/uniaiverse.db` (SQLite: users, payments, news, progress) — nightly `cp` to object storage; `outputs/readiness_audit/` reports likewise.
8. **News:** GitHub Action `quest-news-refresh` runs daily; approve in `https://api.uniaiverse.ai/admin`.

Alternatives without a VPS: Render / Railway / Fly with the root `Dockerfile` (set the same env vars; persistent disk for `outputs/`).

## What runs on every push and every deploy
CI (`.github/workflows/ci.yml`): secrets scan → `pytest` (71 tests incl. Delivery Framework golden tests) → `scripts/validate_content.py` (all content + every demo in all 25 courses) → generated kits up to date → Docker image builds and `/api/health` answers.
Deploy (`deploy.yml`, on merge to `main`): pull → build → wait for `/api/health`; if it never becomes healthy the server returns to the previous commit and the workflow fails loudly. `.dockerignore` keeps `.env`, `.git` and `outputs/` out of the image.
