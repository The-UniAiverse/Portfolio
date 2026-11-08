# uniAIverse

One repository, two independently deployable applications.

| App | Path | Stack | Local port | Deploy target |
|---|---|---|---|---|
| Website + admin | [`apps/web`](apps/web) | Next.js 16, React 19, TypeScript, Tailwind, MySQL (`mysql2`) | 3000 | Vercel (root directory `apps/web`) |
| AI services API | [`apps/api`](apps/api) | Python 3.12, FastAPI, Pydantic, ReportLab | 8000 | Any Python/container host (Dockerfile in `apps/api`) |

The website talks to the API only over HTTP. AI provider keys, business logic and report generation stay in `apps/api`.

```text
uniaiverse/
├── apps/
│   ├── web/        Next.js site, admin panel, Next route handlers (/api/admin, /api/calendly, …)
│   └── api/        FastAPI services, training materials, pricing data, tests, Dockerfile
├── docs/
│   ├── architecture.md
│   └── local-development.md
├── .github/workflows/   api-ci.yml, web-ci.yml (path-filtered per app)
├── Makefile             thin wrappers around each app's own tooling
└── README.md
```

## Quick start

```bash
make install     # creates apps/api/.venv, runs npm ci, copies .env templates if missing
make api         # terminal 1 → http://localhost:8000  (/docs for Swagger)
make web         # terminal 2 → http://localhost:3000
make test        # pytest for the API + TypeScript check for the web
```

Without `make`, see [docs/local-development.md](docs/local-development.md) for the plain commands.

## Docs
- [Architecture](docs/architecture.md): boundaries, security model, deployment, adding workers.
- [Local development](docs/local-development.md): setup, environment variables, tests, Docker.
- App-specific details: [apps/api/README.md](apps/api/README.md), [apps/web/SETUP_INSTRUCTIONS.txt](apps/web/SETUP_INSTRUCTIONS.txt).
