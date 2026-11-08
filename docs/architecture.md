# Architecture

## Shape

```text
Browser ──HTTPS──► apps/web (Next.js on Vercel)
   │                 ├─ pages / admin UI
   │                 └─ route handlers /api/admin/*, /api/calendly/*, /api/contact-info  → MySQL, Calendly
   │
   └─────HTTPS──► apps/api (FastAPI, container host)
                     ├─ /api/readiness_audit, /api/training, /api/strategy,
                     │  /api/governance, /api/automation, /api/pricing
                     ├─ LLM provider (Anthropic / OpenAI), optional
                     └─ outputs/ (generated MD/PDF reports)
```

Both apps live in one Git repository but share no code and no runtime. There is no `packages/` directory
because nothing is genuinely shared today. Add one only when a contract (e.g. generated API types from the
FastAPI OpenAPI schema) actually needs to be shared.

There is no monorepo framework. Each app keeps its native tooling. The root `Makefile` only shells into
the app folders, and CI runs one workflow per app, filtered by path.

## Responsibilities

- **apps/api** owns business logic for the AI services, AI provider integration, rule-based fallbacks,
  report generation, rate limiting and input validation. Provider keys exist only in its environment.
- **apps/web** owns presentation, marketing content, the admin panel and its MySQL-backed route handlers.
  It calls apps/api from the browser over HTTP using `NEXT_PUBLIC_AI_SERVICES_API_URL` (client: `apps/web/lib/ai-services.ts`).
  Pages backed by the API: `/tools`, `/tools/readiness-audit`, `/tools/roadmap`, `/tools/governance`,
  `/tools/automation-roi`, `/pricing`, and the course catalogue section of `/services/training`.

## AI Job Finder (third-party code)

`/tools/job-finder` is backed by `apps/api/app/services/jobs`, a thin adapter over the MIT-licensed
[ai-job-search](https://github.com/ai-job-search-dev/ai-job-search) project, vendored unmodified at
`apps/api/vendor/ai-job-search` (provenance and update steps in `apps/api/vendor/README.md`).

| Endpoint | What runs |
|---|---|
| `GET /api/jobs/search`, `GET /api/jobs/job/{id}` | Upstream's freehire connector (Bun CLI subprocess) → upstream `posting_guard.py` |
| `POST /api/jobs/match` | Rules: skills overlap. AI: upstream's `04-job-evaluation.md` rubric → model → upstream `rank_state.overall_score/band` |
| `POST /api/jobs/cover-letter` | AI only: draft with upstream's writing/cover-letter guides, review with upstream's reviewer rules, PDF via ReportLab in upstream's Lato fonts |
| `POST /api/jobs/cover-letter/pdf` | Re-renders a candidate-edited letter (no AI) |

Jobs come from freehire.me. Its terms require an **API plan** for showing its data in a commercial
product and a link back to freehire on every posting (the UI links each job to its freehire page).
The upstream connector sends no API key today; using a plan key needs a small upstream change.
Candidate profiles are not stored; generated PDFs are kept in `outputs/jobs/` under random ids.
Saved profiles and saved jobs per account are a next step (accounts already exist, see Sign-in).

## Sign-in for AI tools

AI tools require a signed-in user; marketing pages, `/pricing`, the training catalogue, `/tools` and
job browsing stay public.

1. `apps/web` runs **Better Auth** (`lib/auth.ts`, route `app/api/auth/[...all]`): "Continue with Google /
   GitHub" on `/login`. The first sign-in creates the account. Users, accounts and sessions are stored
   in **MongoDB** (`MONGODB_URI`); the session is an HttpOnly cookie on the website's domain.
2. Its JWT plugin issues 15-minute Ed25519 tokens at `/api/auth/token` (claims: `sub`, `email`, `name`,
   `iss`/`aud` = `BETTER_AUTH_URL`) and publishes the public keys at `/api/auth/jwks`.
3. The browser sends the token as `Authorization: Bearer …` on AI tool calls (`lib/ai-services.ts`).
4. `apps/api` verifies signature, expiry, issuer and audience against the JWKS
   (`app/core/auth.py`, `Depends(require_user)`) on: `POST /api/readiness_audit/run`,
   `/api/strategy/roadmap`, `/api/governance/classify`, `/api/automation/roi`, `/api/jobs/match`,
   `/api/jobs/cover-letter`, `/api/jobs/cover-letter/pdf`. No valid token → 401; JWKS unreachable → 503.

The UI gate (`components/auth/SignInGate.tsx`) only improves the experience; enforcement is in the API.
`AUTH_REQUIRED=false` disables enforcement for local development only.

## Security model

- Provider secrets are never sent to the browser and never placed in `NEXT_PUBLIC_*` variables.
- The API's browser access is limited by `CORS_ORIGINS`. CORS is not authentication; it only stops other
  sites from reading responses in a browser.
- The AI services API is currently anonymous by design (public tools). It protects itself with input bounds,
  a per-IP POST rate limit (`app/core/ratelimit.py`) and unguessable 128-bit report ids.
- The rate limiter is in-process. With several workers or instances, use a shared store (e.g. Redis) or the
  host's edge rate limiting.
- **Open issue:** the web admin panel authenticates in the browser only, and the `/api/admin/*` route
  handlers do not check a session. This has to be replaced with server-side authentication (session
  cookie or auth provider, checked in middleware and in every admin route handler) before production use.

## Deployment

| App | Target | Notes |
|---|---|---|
| web | Vercel | Set the project root directory to `apps/web`. Set the DB, Calendly and `NEXT_PUBLIC_AI_SERVICES_API_URL` env vars in Vercel. |
| api | Render / Railway / Fly.io / Cloud Run / VPS | Build from `apps/api/Dockerfile` with context `apps/api`. Set `CORS_ORIGINS` to the Vercel domain(s). Set `TRUST_PROXY_HEADERS=true` only behind the platform proxy. |

Each app deploys on its own. Path-filtered CI means a web change does not rebuild the API and vice versa.
Generated reports are written to `apps/api/outputs/`. On ephemeral hosts, mount a volume or move them to
object storage.

## Adding background workers later

Put workers next to the API, not the web app, e.g. `apps/api/app/workers/` (same codebase, same image,
different start command) or a separate `apps/worker/` if they grow their own dependencies. The web app
should only enqueue work through an API endpoint and poll or receive results over HTTP. It must never
talk to the queue directly.
