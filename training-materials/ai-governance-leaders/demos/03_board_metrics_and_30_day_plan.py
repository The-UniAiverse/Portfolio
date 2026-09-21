"""AI Governance for Leaders · Demo 3 — What the board sees, and your 30-day quick start (12 min) · Module 4+5
Shows: six governance metrics computed from an inventory and incident log, and a 30-day plan generated from the gaps by the real engine
Lab: Fill in the three numbers you do NOT currently know for your organisation. That list is your first 30 days.
Run: python 03_board_metrics_and_30_day_plan.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Governance for Leaders · Demo 3 — What the board sees, and your 30-day quick start")
c = api(); g = c.post("/api/governance/assess", json=c.get("/api/governance/sample").json()).json(); inv = g["inventory"]
INCIDENTS = [("wrong refund advice by bot", "limited", 2, True), ("PII pasted into public tool", "n/a", 1, True), ("CV tool bias complaint", "high", 9, False)]
M = [("Systems in inventory", len(inv)), ("High-risk systems", sum(s["risk_tier"] == "high" for s in inv)), ("High-risk with sign-off control (C12) evidenced", sum(1 for s in inv if s["risk_tier"] == "high" and "C12" in s["controls_in_place"])),
     ("Average control coverage", f"{sum(s['control_coverage_pct'] for s in inv) / len(inv):.0f}%"), ("Incidents this quarter", len(INCIDENTS)), ("Incidents closed within 5 days", sum(1 for *_, d, closed in INCIDENTS if closed and d <= 5))]
table(["Board metric", "Value"], [[a, b] for a, b in M]); print("\n30-DAY QUICK START (from the engine's gap analysis):"); [print(f"  • {str(x)[:120]}") for x in g["roadmap"]["30 days"]]
say("If the board sees six numbers every quarter, governance exists. If it sees a policy PDF once, it does not.")
