# Convenience wrappers. Each app keeps its own toolchain: npm for apps/web, venv + pip for apps/api.
# Run `make api` and `make web` in two terminals for local development.

API := apps/api
WEB := apps/web
PY  := .venv/bin/python

.PHONY: install api-install web-install api web test api-test web-check web-build build docker-up docker-down

install: api-install web-install

api-install:
	cd $(API) && (test -d .venv || python3 -m venv .venv)
	cd $(API) && $(PY) -m pip install -r requirements.txt
	cd $(API) && (test -f .env || cp .env.example .env)

web-install:
	cd $(WEB) && npm ci
	cd $(WEB) && (test -f .env.local || cp .env.example .env.local)

api:
	cd $(API) && $(PY) -m uvicorn app.main:app --reload --port 8000

web:
	cd $(WEB) && npm run dev

test: api-test web-check

api-test:
	cd $(API) && $(PY) -m pytest -q

web-check:
	cd $(WEB) && npx tsc --noEmit

web-build:
	cd $(WEB) && npm run build

build: web-build

docker-up:
	cd $(API) && docker compose up --build

docker-down:
	cd $(API) && docker compose down
