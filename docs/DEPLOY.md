# Deploying to uniaiverse.ai

Architecture: the Next.js site stays on Vercel at `uniaiverse.ai`. This API runs at `api.uniaiverse.ai` on one small VPS (2 vCPU / 2 GB is enough).

1. **Server:** Ubuntu 24, Docker + Compose. `git clone git@github.com:The-UniAiverse/ai-services.git /srv/uniaiverse-ai-services`.
2. **DNS:** `A api.uniaiverse.ai → <server IP>`. Caddy issues HTTPS automatically.
3. **Env:** `cp .env.example .env` and fill: `CORS_ORIGINS=https://uniaiverse.ai,https://www.uniaiverse.ai`, `PUBLIC_URL=https://api.uniaiverse.ai`, `ADMIN_TOKEN`, Razorpay keys when the merchant account is approved, optional LLM key.
4. **Run:** `docker compose -f deploy/docker-compose.prod.yml up -d --build`. Check `https://api.uniaiverse.ai/api/health`.
5. **Website:** apply `website-patch/` (uniAI bot, links, `NEXT_PUBLIC_API_URL`). Vercel env var `NEXT_PUBLIC_API_URL=https://api.uniaiverse.ai`.
6. **Razorpay:** Dashboard → Webhooks → `https://api.uniaiverse.ai/api/payments/webhook`, events `payment.captured`, `order.paid`, `virtual_account.credited`; put the secret in `RAZORPAY_WEBHOOK_SECRET`. Enable Smart Collect for NEFT/RTGS/IMPS virtual accounts. Set the UPI limit in `UPI_LIMIT_INR` (default 2000).
7. **Backups:** `outputs/uniaiverse.db` (SQLite: users, payments, news, progress) — nightly `cp` to object storage; `outputs/readiness_audit/` reports likewise.
8. **News:** GitHub Action `quest-news-refresh` runs daily; approve in `https://api.uniaiverse.ai/admin`.

Alternatives without a VPS: Render / Railway / Fly with the root `Dockerfile` (set the same env vars; persistent disk for `outputs/`).
