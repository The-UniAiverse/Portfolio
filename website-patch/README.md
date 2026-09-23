# Website patch

**Positioning (2026-09-24):** the public site sells AI: readiness audit, demos, AI services, AI consulting, workshops, the AI platform. One "Training & Mentorship" page lists three tracks — AI, DevOps, Development / SDE — with DevOps and Development described as parts of cohorts, not as separate service pages. Immediate pages: readiness audit, demos, cohort one-page offer, AI services, AI consulting, workshops, training & mentorship, contact, legal (terms, privacy, refund, student terms). Tracks come from `GET /api/platform/registries` → `tracks`; show only `status: final` as offerings. — apply to `The-UniAiverse/Portfolio` (branch `features/sarfi`)

1. `components/UniAIBot.tsx` → copy into `components/`. Delete `components/OrbiBot.tsx`.
2. `app/layout.tsx`: replace `import OrbiBot from '@/components/OrbiBot'` with `import UniAIBot from '@/components/UniAIBot'` and `<OrbiBot />` with `<UniAIBot />`.
3. `.env.local` (and Vercel project env): add `NEXT_PUBLIC_API_URL=https://api.uniaiverse.ai` (local: `http://localhost:8000`).
4. `package.json`: set `repository.url` to `git+https://github.com/The-UniAiverse/Portfolio.git` and `homepage` to `https://github.com/The-UniAiverse/Portfolio#readme`.
5. Add links in the site nav / services pages:
   - Free AI Readiness snapshot → `https://api.uniaiverse.ai/`
   - Course Finder → `https://api.uniaiverse.ai/course-finder`
   - uniAI Quest → `https://api.uniaiverse.ai/quest`
   - Checkout → `https://api.uniaiverse.ai/pay?product=<id>`
   - Request access / price page → `https://api.uniaiverse.ai/register` (plans from `GET /api/platform/plans`)
   - After sign-in: send `X-Tenant-Key` on every API call; `GET /api/platform/me` returns capabilities and remaining quota; a 402 means "not in plan / quota reached" — show the upgrade link it returns.
   - AI Delivery Framework (estimate + pack) → `https://api.uniaiverse.ai/delivery`
   - Live demos and course labs → `https://api.uniaiverse.ai/demos`
   - Course pages: `GET /api/demos/courses` lists each course's labs; `POST /api/demos/run-course/{course}/{demo}` returns the output as text — render it in a `<pre>`.
   (Or proxy these under uniaiverse.ai/tools/* with a Next.js rewrite — see `next.config.rewrites.example.js`.)

## About the ChatGPT Go account
ChatGPT Go / Plus are consumer subscriptions: they have no API, and using them as a backend for a public bot is not possible technically and is outside their terms. uniAI therefore runs on the AI Services API:
- **No key needed:** answers come from `app/services/bot/knowledge.yaml` — services, pricing, booking, demos, Quest. Edit the YAML to teach it; unanswered questions are listed in `/admin`.
- **Optional polish:** set `LLM_PROVIDER=anthropic` or `openai` with an *API* key (pay-per-token, typically $5–20/month at website volumes) and answers are rephrased naturally, still only from the knowledge base.
- **Optional:** publish a public GPT named "uniAI" from a ChatGPT account that allows building GPTs, and put its link in `knowledge.yaml → bot.chatgpt_url`; the widget shows a "Continue in ChatGPT" link for long conversations.
