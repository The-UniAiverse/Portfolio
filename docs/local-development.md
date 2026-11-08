# Local development

Prerequisites: Node.js 22+ and npm, Python 3.12+, optionally Docker, and MySQL if you use the web admin panel.

## Ports

| Process | URL |
|---|---|
| Web (Next.js dev server) | http://localhost:3000 |
| API (uvicorn) | http://localhost:8000. Demo UI at `/`, Swagger at `/docs`, health at `/api/health` |

The API allows browser calls from the origins in `CORS_ORIGINS` (default `http://localhost:3000`).
The web app reads the API base URL from `NEXT_PUBLIC_AI_SERVICES_API_URL` (default `http://localhost:8000`).
The AI tools (`/tools/*`), `/pricing` and the course catalogue on `/services/training` call it from the browser.

## API (`apps/api`)

```bash
cd apps/api
cp .env.example .env                       # LLM_PROVIDER=none works with no keys
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest -q
```

The AI Job Finder (`/api/jobs/*`) also needs [Bun](https://bun.sh) on `PATH` (or `BUN_BIN=/path/to/bun`)
to run the vendored job connector, e.g. `brew install oven-sh/bun/bun`. Without it the rest of the API works
and job search returns a clear "not available" error. Cover letters and AI-enhanced fit need an AI provider key.

Docker (needs a running Docker daemon):

```bash
cd apps/api
docker compose up --build                  # uses .env; mounts ./outputs for generated reports
```

### API environment variables (`apps/api/.env`)

| Variable | Required | Purpose |
|---|---|---|
| `LLM_PROVIDER` | no | `none` (default), `anthropic`, `openai`, `gemini` or `deepseek` |
| `LLM_FALLBACK_PROVIDER` | no | Second provider tried when the first fails, e.g. `deepseek` |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GEMINI_API_KEY` / `DEEPSEEK_API_KEY` | only for that provider | Provider secret. Server-side only. |
| `GEMINI_MODEL`, `DEEPSEEK_MODEL` | no | Defaults `gemini-2.5-flash`, `deepseek-chat` |
| `LLM_MODEL` | no | Model id for the chosen provider |
| `APP_ENV`, `APP_PORT` | no | Environment label, port |
| `CORS_ORIGINS` | yes in production | Comma-separated web origins allowed to call the API |
| `ENABLED_SERVICES` | no | Comma-separated service ids (see `app/core/registry.py`) |
| `BUN_BIN`, `FREEHIRE_API_URL` | no | Bun path if not on `PATH`; self-hosted freehire URL |
| `RATE_LIMIT_PER_MINUTE` | no | POSTs per client IP per minute on `/api/*` (0 disables) |
| `TRUST_PROXY_HEADERS` | no | `true` only behind a trusted proxy that sets `X-Forwarded-For` |

## Web (`apps/web`)

```bash
cd apps/web
cp .env.example .env.local
npm ci
npm run dev
npx tsc --noEmit && npm run build
```

### Web environment variables (`apps/web/.env.local`)

Full list with comments is in `apps/web/.env.example`. The ones read by the code today:

| Variable | Exposure | Purpose |
|---|---|---|
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | server only | MySQL for admin/content route handlers (`lib/db`) |
| `NEXT_PUBLIC_AI_SERVICES_API_URL` | **public** | Base URL of `apps/api`. Not a secret. |
| `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_GA_ID` | **public** | Site URL, analytics id |

Anything prefixed `NEXT_PUBLIC_` is bundled into browser JavaScript. Never put provider keys, database
credentials or admin secrets there.

## Make targets (repo root)

| Target | Does |
|---|---|
| `make install` | `api-install` + `web-install` (venv, pip, `npm ci`, copy env templates if absent) |
| `make api` / `make web` | Run each dev server |
| `make test` | `pytest` + `tsc --noEmit` |
| `make web-build` | `next build` |
| `make docker-up` / `make docker-down` | API container via `apps/api/docker-compose.yml` |
