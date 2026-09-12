# uniAIverse AI Services — backend & training materials

Working, deployable code for Sarfi's service portfolio (per *AI Services — Role & Task Ownership*), built so services can be added, removed or customised one file at a time.

| Priority | Service | API prefix | Status |
|---|---|---|---|
| 1 | **AI Readiness Audit** — Framework v2.0: 348 questions, 10 domains, 51 capabilities, 6 industry modules. Five audit tiers (Free 25 → Bronze 85 → Silver 179 → Gold 263 → Platinum 316 + industry). Evidence flags, critical-control red flags, benchmarks, capability heatmap, 30/60/90-day plan, PDF/MD report | `/api/readiness_audit` | ready |
| 2 | **Training & Mentorship** — Curriculum v2.0: 22 versioned courses, 10 tracks (incl. individual professionals), 4 certification levels, emerging-topics watchlist, staleness flags | `/api/training` | ready |
| 3 | AI Transformation, Strategy & Roadmap — use-case prioritisation + phased roadmap | `/api/strategy` | beta |
| 3 | AI Governance, Safety & Compliance — risk-tier classifier + controls + policy template | `/api/governance` | beta |
| 4 | AI Automation & Workflow Optimisation — workflow inventory + ROI/payback calculator | `/api/automation` | beta |
| — | **Pricing & engagement blueprints** — Free/Professional/Bronze/Silver/Gold/Platinum per service, size multipliers (professional → enterprise), phases/deliverables/team per tier, one-call proposal skeleton | `/api/pricing` | ready |

Everything works **without** an LLM key (rule-based, deterministic). Add a key and narratives are AI-written.

## Run it
```bash
cp .env.example .env            # optionally set LLM_PROVIDER + key
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://localhost:8000  (demo UI)  ·  /docs (Swagger)
pytest -q                       # 10 tests
# or: docker compose up
```

## Try the audit in 10 seconds
Open http://localhost:8000 → pick a tier (and an industry module for Silver+) → *fill with sample answers* → *Score my readiness* → download the PDF.
Or via API: `GET /api/readiness_audit/sample?tier=gold&industries=financial_services` → `POST /api/readiness_audit/run`.
Framework outline for the website/proposals: `GET /api/readiness_audit/framework`. Proposal skeleton: `GET /api/pricing/proposal?service=strategy&tier=gold&company_size=large`.

## Website repo note (Harsh)
`Portfolio/package.json` still points `repository.url` and `homepage` at `github.com/waghmarepb/uniaiverse-website` — update to `github.com/The-UniAiverse/Portfolio`.

## Customise without touching code
| What | Where |
|---|---|
| Audit questions, tiers per question, evidence/critical flags, remediation text | `app/services/readiness_audit/question_bank.yaml` (line format `F*! text`) |
| Audit product tiers, report features, benchmarks | `app/services/readiness_audit/audit_tiers.yaml` |
| Courses, tracks, modules, certifications, emerging topics | `training-materials/curriculum.yaml` (+ folder per course for slides/labs) |
| Prices and tiers | `pricing/tiers.yaml` |
| Engagement phases, deliverables, team per tier | `pricing/blueprints.yaml` |
| Change log | `CHANGELOG.md` — record every framework/curriculum/pricing change |
| Which services are live | `ENABLED_SERVICES` in `.env` |
| Add a service | new folder with `router.py` + one line in `app/core/registry.py` |
| LLM provider / model | `.env` (`anthropic` / `openai` / `none`) |

## Layout
```
app/core/         config · llm (provider-agnostic) · registry (service list)
app/services/     one folder per service, each self-contained
training-materials/  catalog.yaml + COURSE.md per topic (+ RAG PDFs, LLM cost calculator)
pricing/          tiers.yaml
ui/index.html     demo front-end (no build step)
tests/            pytest end-to-end
```

## Website integration (Harsh)
Deploy this API (Railway / Render / Fly / a VPS with `docker compose up`), set `CORS_ORIGINS` to the site URL, then in the Next.js site set `NEXT_PUBLIC_API_URL=https://api.uniaiverse.ai`. The service pages call:
- `GET  /api/readiness_audit/questionnaire` → render form; `POST /api/readiness_audit/run` → show result + PDF link
- `GET  /api/training/catalog` → training page; `GET /api/pricing/tiers` → pricing page
- `POST /api/automation/roi`, `/api/strategy/roadmap`, `/api/governance/classify` → calculators

## Push to GitHub (dev branch)
```bash
./scripts/push_to_github.sh git@github.com:The-UniAiverse/ai-services.git sarfi/dev
```

## Roadmap (next increments)
- P1: lead capture (email → audit report), multi-language questionnaire, benchmark against industry averages
- P2: slide decks + exercises per course (pptx), quiz engine, certificates
- P3: strategy PDF report, governance audit checklist per framework (ISO 42001 / NIST)
- P4: workflow map generator (current → future state diagrams)
