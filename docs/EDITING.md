# Editing guide — where to change what

Everything a consultant or trainer changes lives in YAML or Markdown, not code. After any edit: `python scripts/validate_content.py`, then commit on your `features/<name>` branch.

| I want to… | Edit this | Then |
|---|---|---|
| Add / remove / reword an **audit question** | `app/services/readiness_audit/question_bank.yaml` — one line per question: `S*! text` (tier letter F/B/S/G/P, `*` evidence, `!` critical) | nothing else; tiers, scoring, reports and the UI adapt |
| Change what a **capability recommends** | same file → `low_action` / `mid_action` under the capability | — |
| Add a **domain** or **industry module** | same file → copy a domain block; keep domain weights summing to 1.0 | validate |
| Change **audit tiers, prices, benchmarks** | `app/services/readiness_audit/audit_tiers.yaml` | — |
| Add a **course** | `python scripts/new_course.py <id> "<title>" --hours 8 --level 2 --track business` → fills `curriculum.yaml` and creates the folder pack (COURSE.md, facilitator-guide.md, exercises.md, slides/) | write the content; `python scripts/build_slides.py --pdf` |
| Change a course's **modules, hours, outcomes, tier availability** | `training-materials/curriculum.yaml` → the course block; bump `version`, set `last_reviewed` | `CHANGELOG.md` |
| Retire a course | set `status: retired` (keeps history) or delete the block and folder | validate |
| Edit **workshop slides** | `training-materials/agentic-ai-workshop/slides.yaml` (title, bullets, notes per slide) | `node scripts/build_slides.js training-materials/agentic-ai-workshop/slides.yaml` → rebuilds the .pptx |
| Edit a **workshop demo** | `training-materials/agentic-ai-workshop/demos/NN_*.py` — plain Python; shared helpers in `common.py` (rates in `RATES`) | `python demos/run_all.py` must print ALL DEMOS OK |
| Run demos on a **client's documents** | drop `.md` files into `demos/sample_docs/` (use `##` headings) | — |
| Add a **demo** | new `NN_name.py` in `demos/`; it runs in order automatically | — |
| Edit **facilitator run-sheet / exercises / handouts** | `facilitator-guide.md`, `exercises.md`, `handouts/*.md` | — |
| Change **Course Finder** logic (which profile → which track) | `app/services/training/course_finder.py` → `KEYWORDS` and `_choose_track` | tests |
| Add a **Quest quiz question** | `app/services/quest/question_bank.yaml` → under the topic: `q`, `options`, `answer` (index), `d` (1-3), `why`, `tags` | validate (checks duplicates and ranges) |
| Add a **Quest topic** | same file → new topic block with `id`, `title`, `emoji`, `blurb`, `questions` | free tier topics list in `quest_tiers.yaml` |
| Add an **interview challenge** | same file → `interview_challenges`: `id`, `topic`, `level`, `prompt`, `listen_for`, `model_answer` | — |
| Change **Quest tiers, prices, limits, XP** | `app/services/quest/quest_tiers.yaml` | payments catalog reads it automatically |
| Add a **news source** | `app/services/quest/news_sources.yaml` | daily action fetches; approve in `/admin` |
| Teach the **website bot** something | `app/services/bot/knowledge.yaml` → add an intent: `id`, `triggers`, `answer`, optional `link`, `quick_replies` | check `/admin` → "Unanswered" for what people actually ask |
| Rename the bot / greeting / Calendly link | same file → `bot:` block | — |
| Change **service prices / tiers** | `pricing/tiers.yaml` | blueprints must have the same tier ids (validated) |
| Change **engagement phases, deliverables, team days** | `pricing/blueprints.yaml` | `/api/pricing/proposal` uses it |
| Tune **strategy scoring, phases, KPIs, budgets** | `app/services/strategy/config.yaml` | — |
| Change **governance controls, frameworks, policy text** | `app/services/governance/{controls,frameworks,policy}.yaml` | — |
| Change **automation approach rules, step patterns, risks** | `app/services/automation/playbook.yaml` | — |
| Change **UPI limit, bank details, gateway keys** | `.env` (`UPI_LIMIT_INR`, `BANK_TRANSFER_DETAILS`, `RAZORPAY_*`) | restart |
| Turn a service **on/off** | `.env` → `ENABLED_SERVICES` | restart |
| Add a whole **new service** | folder `app/services/<id>/router.py` + one line in `app/core/registry.py`; reports via `app.core.report` | tests |

## Demo pages (all served by the API, no build step)
`/` readiness audit · `/course-finder` · `/quest` · `/pay` · `/tools` (strategy, governance, automation) · `/admin` · `/docs` (Swagger for every endpoint)

## Rules of the house
- Content changes bump `version` and `last_reviewed` in the file you touched and get a line in `CHANGELOG.md`.
- The API flags any course not reviewed for 6 months (`/api/training/curriculum` → `stale_courses`).
- Never commit `.env`. Secrets live in the server `.env` and GitHub Actions secrets.
- `python scripts/validate_content.py` and `pytest -q` must both pass before a PR to `dev`.
