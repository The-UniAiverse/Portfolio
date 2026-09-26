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
| Change a **course demo** (any course) | `training-materials/<course>/demos/NN_name.py` — plain Python; the data it uses is at the top of the file or in `demos/data/` | `python demos/run_all.py` in that course → `ALL DEMOS OK`, then `python scripts/build_course_kits.py` |
| Add a **course demo** | copy a neighbour to the next number; keep the 4-line header (`Course · Demo N — Title (min) · Module m`, `Shows:`, `Lab:`, `Run:`) and end with `say("…")` | same as above — it appears in the guide, exercises, `/demos` and the API by itself |
| Change a demo's **timing, lab text or closing line** | the header and the last `say("…")` line of that demo | `python scripts/build_course_kits.py` rewrites README, facilitator guide, exercises, handout |
| **Hand-write** a course guide instead of the generated one | delete the first line (`<!-- GENERATED … -->`) of that file | the generator never touches it again |
| Change shared demo machinery (models, metrics, agent caps, security checks) | `training-materials/labkit/*.py` | `python scripts/validate_content.py` runs every course |
| Delivery Framework — **day rates, FX, milestones, support %** | `app/services/delivery/content/rate_card.yaml` (set `status:` to `confirmed` once real) | validate; stored engagements show "numbers out of date" until re-saved |
| Delivery Framework — **LLM prices** | `…/content/llm_rates.yaml` → `models:`; update `verified:` to today | the engine warns when `verified` is over 100 days old |
| Delivery Framework — **tier questions, score bands, risk floors, contingency %** | `…/content/tiers.yaml` | bands must cover 8–24 exactly once (validated); update `tests/test_delivery.py` on purpose |
| Delivery Framework — **effort per workstream, stage weeks, role split** | `…/content/wbs.yaml` | golden tests will tell you what moved |
| Delivery Framework — **which document goes in which tier**, document wording | `…/content/deliverables.yaml` (`bronze/silver/gold: lite | full | ""`, wording under `library:`) | Bronze 13 / Silver 21 / Gold 26 is tested — change the test if you mean it |
| Delivery Framework — **gate criteria** | `…/content/gates.yaml` (`blocking: true` = cannot be waived without written conditions) | — |
| Delivery Framework — **security controls**, **solution patterns / token profiles** | `…/content/security_controls.yaml`, `…/content/patterns.yaml` | — |
| Platform **plans, quotas, fees, capabilities per plan, state machine** | `app/services/platform/content/plans.yaml` | tests in `tests/test_platform.py` check quotas by number |
| Platform **capabilities and which URLs they guard** | `…/content/capabilities.yaml` | — |
| **Cost model** (rate card, markup, fees) | `…/content/cost_model.yaml` | `python scripts/cost_report.py` regenerates `docs/COST_ANALYSIS.md` (CI checks) |
| **Registries** (approved tools, models and prices, providers, agents, tracks) | `app/services/platform/content/registries/*.yaml` | served by `GET /api/platform/registries`; bump `version`/`verified` |
| **Classroom token policy, cohort caps** | `…/content/token_policy.yaml` and `plans.yaml → classroom.cohort` | keep the two consistent (tested) |
| **Student prerequisites** · **corporate prerequisites** · **team tooling** · **procurement** | `…/content/student_prerequisites.yaml` · `corporate_prerequisites.yaml` · `team_tooling.yaml` · `procurement.yaml` | — |
| **Look and navigation** of every page | `ui/assets/uav.css`, `ui/assets/nav.js` | reload |
| **Hour ceilings and rates** per person | `app/services/platform/monitor.py` → `ceiling`, `rates` | pytest |
| Turn entitlement **enforcement** on | `.env` → `ENTITLEMENTS_MODE=enforce` | restart; website must send `X-Tenant-Key` |
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
`/` readiness audit · `/course-finder` · `/quest` · `/pay` · `/tools` (strategy, governance, automation) · `/delivery` (AI Delivery Framework) · `/demos` (workshop demos + labs for all 25 courses) · `/discovery` · `/admin` · `/docs` (Swagger for every endpoint)

## Rules of the house
- Content changes bump `version` and `last_reviewed` in the file you touched and get a line in `CHANGELOG.md`.
- The API flags any course not reviewed for 6 months (`/api/training/curriculum` → `stale_courses`).
- Never commit `.env`. Secrets live in the server `.env` and GitHub Actions secrets.
- `python scripts/validate_content.py` and `pytest -q` must both pass before a PR to `dev`.
