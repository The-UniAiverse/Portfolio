"""AI Executive & Board Briefing · Demo 2 — What to fund first: portfolio view from the real engine (10 min) · Module 2+4
Shows: the client's use cases ranked into quick wins and bets with phase budgets, from the uniAIverse strategy engine, plus the readiness score that limits the pace
Lab: Facilitator pre-loads the client's own five use cases via /tools → Strategy. The board discusses only the top two and the one they would stop.
Run: python 02_portfolio_and_funding.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Executive & Board Briefing · Demo 2 — What to fund first: portfolio view from the real engine")
c = api(); out = c.post("/api/strategy/roadmap", json=c.get("/api/strategy/sample").json()).json()
print(f"{out['organisation']} · readiness {out['readiness_score']:.0f}/100 — low readiness caps how much can be absorbed in year one\n")
table(["Rank", "Initiative", "Type", "Score"], [[b["rank"], b["name"][:46], b["quadrant_label"], b["score"]] for b in out["backlog"]]); print()
for p in out["phases"]: print(f"  {p['title'][:46]:<46} {bar(p['budget_usd'], max(x['budget_usd'] for x in out['phases']), 20)} ${p['budget_usd']:,}")
t = out["totals"]; print(f"\n  Ask of the board: ${t['build_usd']:,} build + ${t['run_monthly_usd'] * 12:,}/yr run for ${t['annual_benefit_usd']:,.0f}/yr benefit at full adoption.")
print("  Three board questions: 1) Who owns each number?  2) What is the stop rule for the bets?  3) What are we NOT doing this year?")
say("Fund two quick wins to build the muscle and one bet to matter. Everything else waits for the readiness score to move.")
