"""AI FinOps · Demo 3 — Reporting: the dashboard, budget alerts and governance (15 min) · Module 3
Shows: a month-to-date spend view with forecast, budget burn alerts by team, anomaly detection on cost per request and the monthly governance ritual
Lab: Write your dashboard spec: six tiles, each with an owner and a threshold. Which tile would have caught your last surprise?
Run: python 03_dashboard_and_budget_alerts.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI FinOps · Demo 3 — Reporting: the dashboard, budget alerts and governance")
DAY = 21; BUD = {"support": 3200, "sales": 600, "finance": 250, "strategy": 900}; MTD = {"support": 2050, "sales": 640, "finance": 95, "strategy": 1180}; rows = []
for t in BUD:
    fc = MTD[t] / DAY * 30; burn = MTD[t] / BUD[t]; st = "OVER BUDGET" if burn > 1 else "ALERT: forecast > budget" if fc > BUD[t] else "ok"; rows.append([t, money(BUD[t]), money(MTD[t]), f"{burn:.0%}", money(fc), st])
table(["Team", "Budget", f"Spend (day {DAY})", "Burn", "Forecast", "Status"], rows); hr()
CPR = [0.0182, 0.0185, 0.0181, 0.0188, 0.0184, 0.0183, 0.0312, 0.0319]; mu = sum(CPR[:6]) / 6; sd = (sum((x - mu) ** 2 for x in CPR[:6]) / 6) ** 0.5; print("Cost per request, last 8 days (support-assistant):")
[print(f"  day {i + 14}: ${x:.4f} {bar(x, 0.035, 25)} {'← ANOMALY (z=%.0f)' % ((x - mu) / sd) if (x - mu) / sd > 3 else ''}") for i, x in enumerate(CPR)]; print("  Cause found in 10 minutes because the tile existed: a release on day 20 stopped trimming chat history.")
hr(); print("DASHBOARD SPEC — six tiles: spend vs budget by team · forecast to month end · cost per resolved task by feature · top 10 users by tokens · cache hit rate · model mix\nGOVERNANCE — monthly 30-minute review: variances >10% explained · budget changes approved BEFORE the spend · price-list check each quarter · kill or fix features with cost/task above value/task")
say("A budget alert on day 21 is a conversation. An invoice on day 35 is an incident.")
