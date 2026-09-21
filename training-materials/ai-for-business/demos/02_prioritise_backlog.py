"""AI for Business Leaders · Demo 2 — Prioritisation lab — on the real uniAIverse strategy engine (15 min) · Module 3
Shows: five use cases scored value × feasibility × fit with risk and effort, ranked into quick wins and strategic bets, with budgets — by the engine consultants use
Lab: Open /tools → Strategy in the browser, load the sample, replace two use cases with your own and compare ranks with the table next to you.
Run: python 02_prioritise_backlog.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Business Leaders · Demo 2 — Prioritisation lab — on the real uniAIverse strategy engine")
c = api(); req = c.get("/api/strategy/sample").json(); out = c.post("/api/strategy/roadmap", json=req).json()
print(f"Client: {out['organisation']} · goal: {out['top_goal']} · readiness {out['readiness_score']:.0f}/100\n")
table(["#", "Use case", "Score", "Quadrant", "Build $", "Payback (months)"], [[b["rank"], b["name"][:42], b["score"], b["quadrant_label"], f"{b['business_case'].get('build_usd', 0):,}", b["business_case"].get("payback_months", "—")] for b in out["backlog"]])
print(); [print(f"  {p['title']:<48} months {p['months']:<6} budget ${p['budget_usd']:,}") for p in out["phases"]]
t = out["totals"]; print(f"\n  Portfolio: build ${t['build_usd']:,} · run ${t['run_monthly_usd']:,}/month · annual benefit ${t['annual_benefit_usd']:,.0f}\n  Operating model suggested: {out['operating_model']['title']} — {out['operating_model']['fits']}")
print(f"\n  Full client-ready PDF: {out['report_pdf_url']}  (same call the website makes)")
say("Low readiness pulls the quick wins forward and pushes the bets back. The score decides the order, not the loudest person.")
