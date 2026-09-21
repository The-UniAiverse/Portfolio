"""AI for Business Leaders · Demo 7 — From idea to production: pilot gates and the 90-day plan (12 min) · Module 6+10
Shows: a pilot charter checked against gate criteria, and a one-page 90-day plan generated from five answers
Lab: Fill PLAN for your own use case. If the gate check says 'not ready', fix the charter before you leave the room.
Run: python 07_pilot_gates_90_day.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Business Leaders · Demo 7 — From idea to production: pilot gates and the 90-day plan")
PLAN = {"outcome": "Cut 'where is my shipment' email handling time by 50%", "use_case": "Grounded assistant on tracking data + policy documents", "owner": "Head of Customer Service", "budget_usd": 35000,
        "success_metric": "median handling time", "baseline": "11 min", "target": "5.5 min", "eval_set": "120 real emails, labelled", "data_owner": "TMS product owner", "risk_tier": "limited", "stop_rule": "stop if <70% correct on the eval set at week 4", "users_in_pilot": 12}
GATE = [("Named business owner", bool(PLAN.get("owner"))), ("One measurable outcome with baseline and target", all(PLAN.get(k) for k in ("success_metric", "baseline", "target"))), ("Evaluation set exists before build", bool(PLAN.get("eval_set"))),
        ("Data owner agreed access", bool(PLAN.get("data_owner"))), ("Risk tier recorded", bool(PLAN.get("risk_tier"))), ("Written stop rule", bool(PLAN.get("stop_rule"))), ("Budget approved", PLAN.get("budget_usd", 0) > 0)]
print("GATE: ready to start the pilot?"); [print(f"  [{'x' if ok else ' '}] {n}") for n, ok in GATE]; print(f"\n  {'GO' if all(ok for _, ok in GATE) else 'NOT READY — fix the unticked lines'}")
hr(); print("90-DAY PLAN (one page)")
table(["Days", "What happens", "Gate at the end"], [["0–15", "Charter, eval set of 120 emails, data access, risk tier", "G0 go / no-go to build"], ["16–45", f"POC on real data with {PLAN['users_in_pilot']} users shadowing", f"G1 — {PLAN['stop_rule']}"],
      ["46–75", "Pilot: live with human review of every answer; measure handling time weekly", f"G2 — {PLAN['success_metric']} {PLAN['baseline']} → {PLAN['target']}?"], ["76–90", "Decision pack: results, run cost, controls, rollout plan", "Fund production or stop"]])
print(f"\n  Owner: {PLAN['owner']} · Budget: ${PLAN['budget_usd']:,} · Definition of Done: metric hit on the eval set AND in live use, costs within model, controls signed off")
say("A pilot without a stop rule is not a pilot. It is a project that has not admitted it yet.")
