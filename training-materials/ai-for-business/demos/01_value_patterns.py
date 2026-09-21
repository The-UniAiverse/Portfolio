"""AI for Business Leaders · Demo 1 — Where value comes from: map a function to the five patterns (12 min) · Module 2
Shows: a function's weekly tasks mapped to assist / automate / augment / new product / risk reduction, with hours and rupee value
Lab: Replace TASKS with your own function's week. Which pattern holds most of your value? Which task should NOT be touched?
Run: python 01_value_patterns.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Business Leaders · Demo 1 — Where value comes from: map a function to the five patterns")
TASKS = [{"name": "Answering 'where is my shipment' emails", "hours_per_week": 60, "ai_share": 0.7, "review_share": 0.15, "pattern": "Automate"}, {"name": "Writing customer quotes", "hours_per_week": 35, "ai_share": 0.5, "review_share": 0.3, "pattern": "Assist"},
         {"name": "Checking invoices against PODs", "hours_per_week": 45, "ai_share": 0.8, "review_share": 0.2, "pattern": "Automate"}, {"name": "Route exception decisions", "hours_per_week": 20, "ai_share": 0.3, "review_share": 0.5, "pattern": "Augment"},
         {"name": "Contract risk review", "hours_per_week": 10, "ai_share": 0.4, "review_share": 0.5, "pattern": "Risk reduction"}, {"name": "Salary and appraisal decisions", "hours_per_week": 6, "ai_share": 0.0, "review_share": 1.0, "pattern": "Keep human"}]
r = biz.hours_saved(TASKS, hourly_cost=450); table(["Task", "Pattern", "Hours/wk", "Hours freed/wk"], [[t["name"], t["pattern"], t["hours_per_week"], f"{s:.1f}"] for t, (_, _, s) in zip(TASKS, r["rows"])])
by = {}
for t, (_, _, s) in zip(TASKS, r["rows"]): by[t["pattern"]] = by.get(t["pattern"], 0) + s
print(); [print(f"  {k:<15}{bar(v, max(by.values()))} {v:5.1f} h/wk") for k, v in sorted(by.items(), key=lambda x: -x[1])]
print(f"\n  Total freed: {r['hours_per_week']:.0f} h/week ≈ INR {r['value_per_year'] / 1e5:.1f} lakh a year at INR 450/hour — before the cost of building anything.")
print("  'New product' is empty. That is normal in year one — and it is where the strategic question sits.")
say("Hours freed is not money saved until you decide what those hours do next.")
