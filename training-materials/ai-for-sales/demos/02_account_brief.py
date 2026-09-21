"""AI for Sales · Demo 2 — Account research: a brief with sources, triggers and gaps (12 min) · Module 2
Shows: a one-page account brief built only from CRM facts, with a trigger, a stakeholder gap and the questions still unanswered — nothing invented
Lab: Build a brief on a live prospect using only facts you can source. Mark every line with where it came from.
Run: python 02_account_brief.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Sales · Demo 2 — Account research: a brief with sources, triggers and gaps")
import csv; rows = list(csv.DictReader(open(data_path(__file__, "crm.csv"))))
for a in rows:
    print(f"\nACCOUNT BRIEF — {a['account']}  ({a['industry']}, {a['employees']} employees, ARR ${int(a['arr_usd']):,})")
    print(f"  Trigger      : {a['trigger']}   [source: CRM note]"); print(f"  Relationship : last contact {a['last_contact_days']} days ago · {a['open_tickets']} open ticket(s)   [source: CRM]")
    print(f"  Champion     : {a['champion']}" + ("   ← GAP: no named contact — do not invent one; ask marketing for the org chart" if a["champion"] == "—" else ""))
    risk = "AT RISK: silent for 60+ days with open tickets — fix service before selling" if int(a["last_contact_days"]) > 60 and int(a["open_tickets"]) > 2 else "OPEN: trigger is fresh, lead with it"
    print(f"  Read         : {risk}"); print(f"  Ask on the call: 'What changes for your team because of \"{a['trigger'].lower()}\"?'")
print("\nRules for AI research: 1) paste the facts, do not ask it to recall them · 2) ask for a source per line · 3) 'unknown' is an acceptable answer")
say("A brief that invents a stakeholder is worse than no brief. Blank is honest.")
