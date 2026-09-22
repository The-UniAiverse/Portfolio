# uniAIverse — How-To Playbook (edit, test, ship, go live)

*For Sarfi. No coding knowledge needed. Version 2.6 · 22 September 2026. The control plane (approval, plans, quotas, provisioning, cost) has its own guide: `docs/PLATFORM_PLAYBOOK.md`.*

---

## 1. The one idea, and what is new

You have **one engine** (the API) and **many faces** (web pages that use it). Everything the engine knows lives in plain text files you can edit. Change the file, the engine changes.

Version 2.5 adds two things.

| New | What it is | Where |
|---|---|---|
| **Working demos for all 25 courses** | 108 runnable demos, plus a facilitator guide, exercise sheet, handout and pre-flight check for every course. They run with no internet and no API key. | `training-materials/<course>/` · page `/demos` |
| **AI Delivery Framework** | Fill one form about a client project. Get the tier (Bronze, Silver, Gold), plan, effort estimate, LLM cost, project cost, governance plan, security plan, gate checklists and the document pack in PDF and Word. | page `/delivery` |

**What was tested:** 71 automated tests pass, also on a clean install from the commit on a fresh machine. Every demo in every course runs. The Delivery Framework produces 13, 21 and 26 documents for Bronze, Silver and Gold, and opens as real PDF and Word files.

**What was not tested here:** the Docker build (no Docker in the build sandbox — GitHub checks it on your first push) and a real deployment to your server.

**Two things only you can do before quoting a client:** confirm the day rates and the LLM prices (section 7, edits A and B). Until then every pack prints a "placeholder rates" warning. That is deliberate.

---

## 2. Set up your computer once

You need Python 3.12 and Git. Then, in a terminal:

```bash
unzip uniaiverse-ai-services-v2.5.zip
cd uniaiverse-ai-services
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://localhost:8000/delivery`. If you see the form, everything works.

In `.env`, set `ADMIN_TOKEN=` to a long random phrase. You need it to save engagements and to use `/admin`. Never share `.env` and never put it in Git — the push script refuses if you try.

---

## 3. The pages, and when you open each

| Page | What it is | When |
|---|---|---|
| `/` | Readiness Audit | A prospect asks "how ready are we?" |
| `/discovery` | Discovery questions, PDF and Word | The moment an enquiry arrives |
| **`/delivery`** | **AI Delivery Framework** | **After discovery: size, estimate and price the project; build the pack** |
| `/tools` | Strategy, Governance, Automation reports | Inside a consulting engagement |
| **`/demos`** | Workshop demos **and labs for every course** | Sales calls, classrooms, the website's demo section |
| `/course-finder` | Which course fits a person | A learner asks what to study |
| `/quest` | Quizzes and challenges | College sessions, practice |
| `/pay` | Checkout | Linked from service pages |
| `/admin` | Approvals, unanswered bot questions, bank transfers | Ten minutes a day |
| **`/platform`** | **Control plane: access requests, tenants, quotas, provisioning, cost model (new in 2.6)** | **Every time a request or payment arrives** |
| **`/register`** | **Public: request access, see plans, check a request (new in 2.6)** | **Link it from the website** |
| `/docs` | Every endpoint | When Harsh or Sahil ask what the engine can do |

---

## 4. Using the AI Delivery Framework, click by click

1. Open `/delivery`. Click **Load Silver sample** so you can see a filled form.
2. **Box 1 — the engagement.** Replace client, project, problem, metric, baseline, target. Use the client's own words from the discovery answers.
3. **Box 2 — eight sizing questions.** Pick one answer each. The score (8–24) shows live: 8–12 Bronze, 13–18 Silver, 19–24 Gold.
4. **Box 3 — solution.** Leave the pattern on "Let the engine choose" and tick the hints that are true. Enter use cases, integrations, data sources. Add the readiness score if an audit was done.
5. **Box 4 — risk.** Tick honestly. These can raise the tier whatever the score says. "Manipulation or social scoring" stops the engagement: no estimate, no pack, and a decline note.
6. **Box 5 — volumes and money.** Requests per day, model class, expected annual benefit, quote currency.
7. Click **Run the framework**. Read the result from top to bottom: tier, pattern and why, phases and gates, effort by workstream, LLM cost with scenarios, project cost, milestones, controls, document list.
8. Disagree with the engine? Open **Override**, choose what, give the new value and a reason. The reason is printed in the pack. No reason, no override.
9. Click **Build the document pack**. Download the Word file, edit the narrative, and have a named person review it. The Statement of Work always needs legal review.
10. **To keep it:** enter the admin token, click **Save this intake as a version**. You get an id such as `ENG-4F2A91C0`. Save again with that id after any change: you get version 2, and version 1 is kept.
11. **Gate reviews:** with the id filled in, click **Open gate checklists**. Tick the criteria that have evidence, name who decided, click **Record**. The engine recommends go, conditional go or no-go. A "go" with blocking items open is refused unless you write the conditions.

If the list shows **"numbers out of date — YES"**, a rate or rule changed since you saved. Re-save to refresh.

---

## 5. Running the course demos

**A week before any course:**

```bash
cd training-materials/mlops/demos        # any course folder
python run_all.py                        # must end with: ALL DEMOS OK
```

**In the room:** open `facilitator-guide.md` in the course folder. It gives the time, the demo to run and the command. Every demo ends with a **"Say it:"** line — your closing sentence. `exercises.md` has the labs; `handouts/` has the card to print.

**Live mode:** put `LLM_PROVIDER=anthropic` and a key in `.env`. The same commands then use a real model where that teaches more. Nothing else changes.

**On the website:** `/demos` → "Course labs" runs any demo in the browser.

---

## 6. The edit table: what you want → which file → what to run

After **any** edit run `python scripts/validate_content.py`. It must end with `ALL CONTENT VALID`.

| I want to change… | Edit this file | Notes |
|---|---|---|
| Day rates, currency rates, payment milestones | `app/services/delivery/content/rate_card.yaml` | Set `status: confirmed` when real |
| LLM prices | `…/content/llm_rates.yaml` | Set `verified:` to today's date |
| The eight sizing questions, score bands, contingency % | `…/content/tiers.yaml` | Bands must cover 8–24 |
| Days of effort per workstream | `…/content/wbs.yaml` | |
| Which documents each tier gets, document wording | `…/content/deliverables.yaml` | `lite`, `full` or `""` per tier |
| Gate criteria | `…/content/gates.yaml` | `blocking: true` cannot be waived silently |
| Security controls · solution patterns | `…/content/security_controls.yaml` · `patterns.yaml` | |
| Delivery Framework list prices on the website | `pricing/tiers.yaml` → `delivery:` | Keep tier names the same in `blueprints.yaml` |
| A course demo's data or wording | `training-materials/<course>/demos/NN_name.py` | Then `python scripts/build_course_kits.py` |
| A demo's minutes, lab text, closing line | The 4 header lines and the last `say("…")` line of that demo | Then rebuild kits |
| Course modules, hours, outcomes | `training-materials/curriculum.yaml` | Then rebuild kits |
| A bot answer | `app/services/bot/knowledge.yaml` | Three lines: triggers, answer, link |
| Audit questions · Quest questions · service prices | see `docs/EDITING.md` | The full table for everything older |

---

## 7. Worked edits, step by step

**A. Confirm your day rates.** Open `app/services/delivery/content/rate_card.yaml`. Change the numbers after `day_rate_usd:`. Change `status:` to `"confirmed"`. Change `last_reviewed:` to today. Save. Run the validator. Reload `/delivery` and run the Silver sample: the cost changed and the placeholder warning is gone.

**B. Update LLM prices (every quarter).** Open `llm_rates.yaml`. Under `models:` change `in`, `out`, `cached_in` (US dollars per million tokens) from the provider's price page. Set `verified:` to today. Do the same in `training-materials/llm-cost/cost_calculator.py` → `RATES` so the classroom matches.

**C. Move a document into Bronze.** Open `deliverables.yaml`, find the line, change `bronze: ""` to `bronze: lite`. Run `pytest -q`. One test fails and says Bronze now has 14 documents, not 13. That is the safety net working. Open `tests/test_delivery.py` and change `("bronze", 13,` to `("bronze", 14,`; do the same for the Bronze line in `scripts/validate_content.py`. Run both checks again. Green.

**D. Add a gate criterion.** Open `gates.yaml`, copy a line under the gate, give it the next id (for example `G1-07`), write the text, choose `blocking: true` or `false`. Validate.

**E. Change a course demo for a client.** Open the demo file. The data is at the top in capital letters (`TASKS`, `WEEK`, `PLAN`) or in `demos/data/`. Replace with the client's. Run `python run_all.py` in that folder.

**F. Add a demo to a course.** Copy the nearest demo to the next number, for example `05_my_demo.py`. Keep the four header lines in the same shape. End with `say("…")`. Run `python scripts/build_course_kits.py`. It now appears in the guide, the exercises, `/demos` and the API. You registered nothing.

**G. Take over a generated guide by hand.** Delete the first line of the file (`<!-- GENERATED … -->`). The generator never touches that file again.

**H. Add a course.** `python scripts/new_course.py <id> "<title>" --hours 8 --track business`, write two demos, rebuild kits.

---

## 8. Test before you ship — two commands

```bash
python scripts/validate_content.py     # about a minute · ends: ALL CONTENT VALID
python -m pytest -q                     # about 20 seconds · ends: 71 passed
```

**Reading a failure.** The validator prints `✗` and the file and reason in plain words. Fix that file. A pytest failure names the test. If the name contains `golden`, a number changed because a content file changed: either undo your edit, or, if you meant it, update the expected number in `tests/test_delivery.py` (edit C above).

---

## 9. Push to GitHub

**First time only:**

```bash
git remote add origin git@github.com:The-UniAiverse/ai-services.git
git push -u origin main dev features/sarfi
```

Then on GitHub → Settings → Branches: protect `main` and `dev` (require pull request and green CI).

**Every time after:**

```bash
./scripts/push_to_github.sh "content: confirmed day rates"
```

The script rebuilds the kits, runs both checks, commits and pushes **your** branch. It refuses to push from `main` or `dev`, and refuses if `.env` is in Git. Then on GitHub open a pull request `features/sarfi → dev`. Wait for the green tick. Merge.

---

## 10. Production-ready checklist

| # | Check | How |
|---|---|---|
| 1 | Both test commands green | Section 8 |
| 2 | GitHub CI green, including the Docker job | The tick on your pull request |
| 3 | `ADMIN_TOKEN` is long, random, only on the server | `.env` on the server |
| 4 | `CORS_ORIGINS` lists only your real sites | `https://uniaiverse.ai,https://www.uniaiverse.ai` |
| 5 | `PUBLIC_URL=https://api.uniaiverse.ai`, `APP_ENV=production` | `.env` |
| 6 | Rate card and LLM prices confirmed | Edits A and B |
| 7 | Razorpay: test mode until the merchant account is approved | Leave keys empty |
| 8 | Backups scheduled | Section 12 |
| 9 | GitHub secrets set: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_KEY` | Repo → Settings → Secrets |
| 10 | A legal reviewer named for every SOW | People, not software |

---

## 11. Deploy and go live

**Pieces:** the website (Harsh, Vercel) · the engine (one small server, about ₹500–2,000 a month) · Cloudflare in front (free) · nightly backups. Roughly ₹1,500–4,000 a month at launch. Options and upgrade triggers: `docs/DEPLOYMENT_STRATEGY.md`.

**Once, on the server** (Ubuntu 24 with Docker):

```bash
git clone git@github.com:The-UniAiverse/ai-services.git /srv/uniaiverse-ai-services
cd /srv/uniaiverse-ai-services && cp .env.example .env && nano .env
docker compose -f deploy/docker-compose.prod.yml up -d --build
```

Point DNS `api.uniaiverse.ai` at the server's IP. HTTPS arrives by itself. Open `https://api.uniaiverse.ai/api/health` — it should list twelve services including `delivery`.

**Every release after that:** merge `dev → main` on GitHub. A dated backup branch of `main` is created, the server pulls and rebuilds, and the workflow waits for `/api/health`. If the new version never becomes healthy, the server goes back to the previous version by itself and the workflow turns red.

**Website integration (Harsh).** Apply `website-patch/`. Set `NEXT_PUBLIC_API_URL=https://api.uniaiverse.ai` on Vercel. Link or proxy `/delivery` and `/demos`. For course pages: `GET /api/demos/courses` lists the labs; `POST /api/demos/run-course/{course}/{demo}` returns the output. For an estimate widget: `POST /api/delivery/run`. The website must never call `/api/delivery/intake`, `/engagements` or `/gates` — those need the admin token and stay internal. Full list: `docs/WORK_SPLIT.md`.

**Go-live smoke test, five minutes:** `/api/health` · run the Silver sample on `/delivery` and download the PDF · run one course lab on `/demos` · ask the website bot "how much will an AI project cost?" · save one engagement with the admin token.

---

## 12. After go-live

| When | Do |
|---|---|
| Daily, 10 min | `/admin`: approve news, unanswered bot questions, bank transfers |
| Weekly | `/delivery` → List engagements: any marked out of date? Any gate overdue? |
| Monthly | Restore one backup on your laptop to prove it works |
| Quarterly | LLM prices (edit B) · rate card · question bank and curriculum review (next: December) |

**Backups.** `deploy/backup.sh` copies the database and everything in `outputs/` (including Delivery packs) to cheap storage and keeps 30 days. Schedule it nightly on the server: `crontab -e` → `0 2 * * * /srv/uniaiverse-ai-services/deploy/backup.sh`.

**Rollback.** Code: on GitHub, revert the merge into `main`; it redeploys. Or use the `backup/main-<date>` branch. Content mistake: fix the file, push, merge. Data: restore last night's database file into `outputs/`.

---

## 13. When something breaks

| You see | It means | Do |
|---|---|---|
| `ModuleNotFoundError` on start | Packages not installed | `pip install -r requirements.txt` |
| `/delivery` says Not Found | Service switched off | `.env` → add `delivery` to `ENABLED_SERVICES`, restart |
| 401 "admin token required" | Token missing or wrong | Same value as `ADMIN_TOKEN` in `.env` |
| 422 when running the framework | A field is wrong; the message names it | Usually a sizing answer outside 1–3, or an override without a reason |
| "placeholder rates" on every pack | Rates not confirmed | Edit A |
| "numbers out of date" on an engagement | Content changed since it was saved | Re-save the intake |
| `FAILED … golden …` | A content edit changed an expected number | Undo, or update the test on purpose |
| A course `run_all.py` fails | The last edit to that demo broke it | The error shows the file and line; undo |
| CI red on "kits are up to date" | You edited a demo and did not rebuild | `python scripts/build_course_kits.py`, commit |
| CI red on "secrets scan" | A key went into a file | Remove it **and change the key** |
| Browser cannot reach the API from the website | CORS | Add the site to `CORS_ORIGINS`, restart |
| Deploy went red | New version unhealthy; server already rolled back | Read the log, fix, merge again |

---

## 14. Glossary

| Word | Plain meaning |
|---|---|
| Engine / API | The program on the server that does the work |
| Tier | Bronze (13 documents, gates G0–G2), Silver (21, G0–G3), Gold (26, G0–G4): how deep the engagement goes |
| Gate (G0–G4) | A checkpoint where someone decides go, conditional go or no-go on evidence |
| PERT | An estimate from three numbers: optimistic, likely, pessimistic |
| Contingency | Days added for what nobody can foresee, sized by risk |
| TCO | Total cost over three years: build plus run |
| Pack | The set of documents for a tier, in PDF, Word, Markdown and JSON |
| Content hash | A fingerprint of the rule files; if it changes, saved numbers are out of date |
| Golden test | A test that remembers the right answer for a sample, so accidents show up |
| Branch / pull request | Your own copy of the work, and the request to merge it after checks |
| CI | The checks GitHub runs on every push |
| `.env` | The private settings file. Never in Git |
