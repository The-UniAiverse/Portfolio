# How everything works — the plain-English version

*For Sarfi. No code required to read this.*

---

## The one idea to hold

You have **one engine** (the API) and **many faces** (web pages that use it).

The engine is a program that knows how to: score a readiness audit, recommend a course, run a quiz, price a service, generate a strategy or governance report, take a payment, answer website questions, and run the workshop demos. It runs on one small server at `api.uniaiverse.ai`.

The faces are web pages. Some are built in (the ones below), and the main website Harsh builds is just another face that talks to the same engine.

Everything the engine *knows* — questions, courses, prices, quiz content, bot answers — lives in plain text files you can edit. Change the file, the engine changes its behaviour. No programmer needed for content.

---

## The pages, and when you'd use each

| Page | What it is | When you'd open it |
|---|---|---|
| `/` | AI Readiness Audit. Pick a tier, answer questions, get a scored report and PDF. | A prospect asks "how ready are we?" — send them the free tier. In a Bronze+ engagement, fill it with them. |
| `/course-finder` | Six questions or a pasted CV → which track and course fits them. | A student or professional asks "what should I learn?" |
| `/quest` | uniAI Quest — quizzes, interview challenges, XP, news, tiers. | Show it in college sessions; send it to anyone who wants to practise. |
| `/tools` | Strategy, Governance, Automation engines. Load the sample, edit the numbers, get a client-ready PDF. | Inside a consulting engagement, after discovery — this produces the deliverables. |
| `/demos` | Every runnable demo, live, in the browser. Ask-the-documents shows basic vs advanced RAG side by side. | Sales calls, workshops, the website's Demo section. |
| `/discovery` | Pick who's asking (corporate / business / university / college / domain) and what they want → a discovery-questions document in PDF and Word. | The moment an enquiry email arrives. Reply with this the same day. |
| `/pay` | Checkout. Cards, netbanking, UPI under ₹2,000, bank transfer above. | Linked from Quest tiers and service pages. |
| `/admin` | Approve news, see mentor requests, see what the bot couldn't answer, mark bank transfers paid, change a user's tier. Needs the admin token. | Ten minutes a day, or when a payment arrives by bank transfer. |
| `/docs` | The technical map of every endpoint. | When Harsh or Sahil ask "what can the engine do?" |

---

## Day-to-day: the things you'll actually do

**An enquiry comes in.**
Open `/discovery`, pick the segment and service, type the client name, click Generate. Send the PDF. Sections A–E go to the client; F is for a partner if there is one. The three answers that unblock everything: platform, who provides the environment, dates.

**A workshop is booked.**
Open `training-materials/agentic-ai-workshop/variants/` and pick the edition: `corporate`, `business`, `university`, `college`, `nontech`, `domain`. Each folder has the deck, the facilitator guide (minute by minute), the exercises and a README saying what to prepare. A week before: put the client's documents into `demos/sample_docs/`, then run `python run_all.py` in the `demos` folder — it must say `ALL DEMOS OK`. That's your pre-flight check.

**Standing in the room.**
The deck tells you which demo to run and when. Each demo is one command, printed on the slide. They work with no internet and no API key. Each one ends with a "Say it:" line — that's your closing sentence for that demo.

**A consulting engagement after discovery.**
`/tools` → pick Strategy, Governance or Automation → load the sample → replace the sample numbers with the client's → Run → download the PDF. Edit the narrative if you want, but the structure, scoring and tables are the deliverable.

**Someone asks the website bot something it can't answer.**
`/admin` → "Unanswered" shows you what they asked. Open `app/services/bot/knowledge.yaml`, add the answer (three lines: triggers, answer, link). Done.

**You want to add a course.**
One command: `python scripts/new_course.py <id> "<title>" --hours 8 --track business`. It creates the folder with a course plan, facilitator guide, exercises and a slides file, and registers it in the curriculum. Then you write the content.

**You want to change a price, a question, a tier, a quiz.**
Open `docs/EDITING.md`. It's one table: what you want to change → which file → what to run. That file is the whole manual.

**Before you push anything.**
Two commands from the repo folder: `python scripts/validate_content.py` (checks every content file and runs the demos) and `pytest -q` (checks the engine). Both green → push to `features/sarfi` → pull request into `dev`.

---

## Payments, in plain terms

- Someone buys a Quest tier or a service → Razorpay's window collects the card; your server never sees card numbers.
- Under ₹2,000: UPI is offered. ₹2,000 and above: card, netbanking, or NEFT/RTGS/IMPS to a virtual account number the system gives them with a reference to quote. That's your "avoid UPI above 2k" rule, enforced automatically.
- When Razorpay confirms, the buyer's tier upgrades by itself. If money arrives by bank transfer outside the system, you mark it paid in `/admin`.
- Until the Razorpay account is approved, everything runs in test mode — you can demo the full flow, nothing is charged.

---

## Deployment, in plain terms

Three pieces, three bills:
1. **Website** (Harsh's Next.js) on Vercel. Free to start.
2. **Engine** (this API) on one small rented server (~₹500–2,000/month) behind Cloudflare (free). Cloudflare gives HTTPS, caching so pages feel instant, and protection.
3. **Backups**: the small database and the generated reports copied nightly to cheap storage (~₹0–100/month).

Total at launch: roughly ₹1,500–4,000 a month. The full options table, with what to upgrade when paying customers depend on it, is in `docs/DEPLOYMENT_STRATEGY.md`; the step-by-step is in `docs/DEPLOY.md`. Merging to `main` deploys automatically. Before every merge to `main`, a dated backup branch is created by itself, so you can always go back.

---

## What's already true, what's still to do

**True today:** every page above works and is tested; 28 automated tests; six workshop editions built and validated; the discovery kit produces PDF and Word; payments run in test mode; demos run offline.

**To do before going live:** Razorpay merchant approval (for real money) · point `api.uniaiverse.ai` at a server and set the `.env` values · Harsh applies the website patch (uniAI bot, links) · decide who provides Quest accounts once Harsh's login exists.

**Keep doing:** the quarterly review of the question bank and curriculum (next: December). The engine flags anything not reviewed for six months.
