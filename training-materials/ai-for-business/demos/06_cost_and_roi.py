"""AI for Business Leaders · Demo 6 — Cost and ROI: the $42 bot and the business case (12 min) · Module 8
Shows: one feature costed per request and per month in three designs, then a three-year ROI with payback and a what-if
Lab: Cost one feature from your own business: requests per day, tokens in, tokens out. Then set the benefit honestly and find the payback month.
Run: python 06_cost_and_roi.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Business Leaders · Demo 6 — Cost and ROI: the $42 bot and the business case")
DAILY = arg("--daily", 500, int); designs = {"FAQ bot, cheap model, no documents": ("cheap", 1400, 200), "RAG assistant, mid model, 5 passages": ("mid", 5100, 400), "Agent, mid model, 6 steps": ("mid", 42000, 4000)}
rows = []
for n, (tier, i, o) in designs.items(): c = cost(i, o, tier); rows.append([n, f"${c:.4f}", money(c * DAILY * 30)])
table(["Design", "Per request", f"Per month @ {DAILY}/day"], rows); print("\n  Same question, same users — the design decides whether the bill is $6 or $2,500.")
hr(); run = cost(5100, 400, "mid") * DAILY * 365 + 6000; r = biz.roi(build=48000, run_per_year=run, benefit_per_year=95000)
print(f"Business case — RAG assistant: build $48,000 · run ${run:,.0f}/yr (tokens + hosting + support) · benefit $95,000/yr (ramp 50% in year 1)")
table(["Year", "Cash flow"], [[i, money(c)] for i, c in enumerate(r["cashflows"])]); print(f"\n  3-year ROI {r['roi']:.0%} · NPV {money(r['npv'])} · payback {r['payback_months']} months")
r2 = biz.roi(48000, run, 95000 * 0.6); print(f"  If adoption is only 60%: ROI {r2['roi']:.0%} · payback {r2['payback_months']} months  ← adoption is the biggest assumption in the case")
say("Tokens are rarely what kills an AI business case. Adoption is.")
