"""AI Agents for Sales Operations · Demo 1 — Which sales workflows suit an agent? Rank them (12 min) · Module 1
Shows: six sales-ops workflows scored on volume, rule clarity, data access, reversibility and value — and which should stay manual
Lab: Score your own six workflows. The top one becomes your prototype in the next lab; the bottom one goes on the 'do not automate' list with a reason.
Run: python 01_rank_workflows.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Agents for Sales Operations · Demo 1 — Which sales workflows suit an agent? Rank them")
WF = [("Lead enrichment from public sources", 5, 4, 4, 5, 3), ("Inbound lead qualification + routing", 5, 4, 4, 4, 5), ("Renewal risk alerts", 3, 3, 3, 5, 5), ("Auto-send discount offers", 4, 2, 4, 1, 4), ("Meeting scheduling follow-ups", 4, 5, 5, 4, 2), ("Contract redlining", 2, 2, 3, 1, 4)]
rows = []
for n, vol, rules, data, rev, val in WF:
    s = (vol * .2 + rules * .25 + data * .2 + rev * .2 + val * .15) * 20; verdict = "DO NOT AUTOMATE (irreversible)" if rev <= 1 else "Agent with approval gate" if rev <= 3 else "Agent candidate" if s >= 75 else "Assist only"
    rows.append([n, vol, rules, data, rev, val, f"{s:.0f}", verdict])
table(["Workflow", "Vol", "Rules", "Data", "Reversible", "Value", "Score", "Verdict"], sorted(rows, key=lambda r: -float(r[6])))
print("\n  Reversibility is a veto, not a weight: sending a discount or a redline cannot be unsent.")
say("Automate what is frequent, rule-like and reversible. Anything you cannot undo keeps a human on the button.")
