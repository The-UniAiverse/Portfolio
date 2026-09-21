"""AI Use-Case Design & Product Ownership · Demo 5 — Running the initiative: gates, stakeholders, adoption (12 min) · Module 5
Shows: a delivery plan with gates, a stakeholder map and an adoption tracker that shows the difference between 'launched' and 'used'
Lab: Draw your own stakeholder grid. Who can stop this project with one email? What will you show them at the next gate?
Run: python 05_delivery_plan.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Use-Case Design & Product Ownership · Demo 5 — Running the initiative: gates, stakeholders, adoption")
GATES = [("G0 Fund the POC", "PRD + eval set + data access + risk tier", "Sponsor"), ("G1 POC → Pilot", "≥70% on eval set; cost per request measured", "Sponsor + Product owner"), ("G2 Pilot → Production", "metric hit with real users; controls signed off", "Sponsor + Risk + Security"), ("G3 Production → Scale", "stable 8 weeks; run cost within model", "Steering group")]
table(["Gate", "Evidence needed", "Decides"], [list(g) for g in GATES]); hr()
ST = [("Head of Customer Service", 5, 5, "Sponsor — weekly 15 min"), ("Agents (users)", 2, 5, "Co-design; two champions"), ("IT security", 4, 2, "Early threat-model review"), ("Finance partner", 3, 2, "Show cost model at G1"), ("Works council / HR", 4, 3, "Explain: assists, does not monitor")]
table(["Stakeholder", "Power", "Interest", "Plan"], [list(s) for s in ST]); hr()
WEEKS = [(1, 12, 12, 40), (2, 12, 9, 110), (3, 12, 7, 95), (4, 12, 10, 180), (5, 12, 11, 260)]; print("Adoption tracker (pilot of 12 agents):")
for w, lic, active, drafts in WEEKS: print(f"  week {w}: active {active:>2}/{lic}  {bar(active, lic, 12)}  drafts used {drafts:>3}  per active user {drafts / active:4.1f}")
print("\n  Week 3 dip = the novelty ended. The fix was two champions and removing one extra click, not a better model.")
say("Launched is a date. Adopted is a number. Report the number.")
