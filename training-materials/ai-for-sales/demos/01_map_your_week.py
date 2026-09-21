"""AI for Sales · Demo 1 — Where the hours go: map the selling week (8 min) · Module 1
Shows: a rep's week split into selling vs research/typing, the hours AI can return and what that is worth in pipeline
Lab: Fill WEEK with your own real week (be honest). What share is research and typing? What will you do with the hours you get back?
Run: python 01_map_your_week.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Sales · Demo 1 — Where the hours go: map the selling week")
WEEK = [{"name": "Account research before calls", "hours_per_week": 6, "ai_share": 0.7, "review_share": 0.2}, {"name": "Writing outreach emails", "hours_per_week": 7, "ai_share": 0.6, "review_share": 0.3}, {"name": "CRM updates after calls", "hours_per_week": 5, "ai_share": 0.8, "review_share": 0.15},
        {"name": "Proposal drafting", "hours_per_week": 5, "ai_share": 0.5, "review_share": 0.35}, {"name": "Live customer conversations", "hours_per_week": 14, "ai_share": 0.0}, {"name": "Internal meetings", "hours_per_week": 6, "ai_share": 0.1}]
r = biz.hours_saved(WEEK, hourly_cost=0); tot = sum(t["hours_per_week"] for t in WEEK); [print(f"  {n[:34]:<34} {bar(h, 14, 20)} {h:>4.1f} h   → frees {s:4.1f} h") for n, h, s in r["rows"]]
sell = 14; print(f"\n  Week {tot} h · live selling {sell} h ({sell / tot:.0%}) · freed {r['hours_per_week']:.1f} h → selling time could rise to {(sell + r['hours_per_week']) / tot:.0%}")
print(f"  At 1 qualified meeting per 2.5 selling hours: about {r['hours_per_week'] / 2.5:.0f} extra meetings a week.")
say("AI does not sell. It gives you back the hours you were not selling.")
