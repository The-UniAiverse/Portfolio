"""AI Agents for Sales Operations · Demo 3 — Measuring and governing the agent (12 min) · Module 3
Shows: a weekly metrics sheet — conversion, cost per lead, override rate, data-rule breaches — with thresholds that trigger a review
Lab: Define the four numbers you would report every Monday and the threshold at which you would switch the agent back to read-only.
Run: python 03_metrics_and_governance.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Agents for Sales Operations · Demo 3 — Measuring and governing the agent")
WEEKS = [dict(week=1, leads=220, qualified=61, human_overrides=19, cost=11.2, pii_flags=0, meetings=14), dict(week=2, leads=260, qualified=70, human_overrides=12, cost=13.0, pii_flags=0, meetings=19), dict(week=3, leads=310, qualified=118, human_overrides=41, cost=29.5, pii_flags=2, meetings=17)]
rows = []
for w in WEEKS:
    ov = w["human_overrides"] / w["qualified"]; alerts = [a for a, bad in (("override rate >25%", ov > .25), ("cost/lead up >50%", w["cost"] / w["leads"] > 1.5 * WEEKS[0]["cost"] / WEEKS[0]["leads"]), ("PII flag", w["pii_flags"] > 0)) if bad]
    rows.append([w["week"], w["leads"], f"{w['qualified'] / w['leads']:.0%}", f"{ov:.0%}", f"${w['cost'] / w['leads']:.3f}", f"${w['cost'] / w['meetings']:.2f}", w["pii_flags"], "; ".join(alerts) or "ok"])
table(["Week", "Leads", "Qualified", "Overrides", "Cost/lead", "Cost/meeting", "PII flags", "Alerts"], rows)
print("\n  Week 3: qualification jumped to 38% but reps overrode a third of them and meetings FELL — the agent got generous, not better.\n  Action: back to approval-on-every-assign, review the 41 overrides, fix the scoring rule, re-test on last month's leads.")
print("\n  Data rules: only business contact data · no scraping of personal profiles · log every write · reps can always see why a lead was scored")
say("Qualified leads is the agent's number. Meetings booked is yours. Govern on yours.")
