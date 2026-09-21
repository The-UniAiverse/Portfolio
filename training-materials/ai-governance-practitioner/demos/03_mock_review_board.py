"""AI Governance Practitioner · Demo 3 — Review, documentation, oversight: run a mock review board (30 min) · Module 3
Shows: a review-board pack for a high-risk system checked for completeness, the board's decision with conditions, a human-oversight design test and an incident-process drill
Lab: Run the board: one person presents the system, three review (risk, legal, security). Use the pack checklist. Record the decision and conditions in writing.
Run: python 03_mock_review_board.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Governance Practitioner · Demo 3 — Review, documentation, oversight: run a mock review board")
PACK = {"system": "Claims fraud flagging", "tier": "high", "purpose_and_scope": True, "data_sheet_and_lawful_basis": True, "evaluation_results_incl_subgroups": False, "human_oversight_design": True, "security_test_report": True, "monitoring_plan": True, "incident_runbook": False, "vendor_due_diligence": True, "user_transparency_notice": True, "dpia": True}
items = [k for k in PACK if k not in ("system", "tier")]; print(f"REVIEW BOARD — {PACK['system']} ({PACK['tier']} risk)\n"); [print(f"  [{'x' if PACK[k] else ' '}] {k.replace('_', ' ')}") for k in items]; miss = [k for k in items if not PACK[k]]
blocking = [m for m in miss if m in ("evaluation_results_incl_subgroups", "human_oversight_design", "dpia")]; print(f"\n  DECISION: {'NOT APPROVED — blocking: ' + ', '.join(blocking) if blocking else 'APPROVED WITH CONDITIONS: ' + ', '.join(miss) if miss else 'APPROVED'}\n  Conditions: subgroup evaluation before go-live · incident runbook within 30 days · re-review in 6 months or on material change")
hr(); print("Human-oversight design test — is the human able to disagree?"); OV = [("Reviewer sees the evidence, not just the score", True), ("Reviewer can override without manager approval", True), ("Override rate is measured", True), ("Time allowed per case is realistic (≥ 4 min)", False), ("Reviewers are not penalised for overrides", False)]
[print(f"  [{'x' if ok else ' '}] {n}") for n, ok in OV]; print(f"  → {sum(ok for _, ok in OV)}/5. Override rate last month: 0.4% on 2,300 flags — that is not oversight, it is a rubber stamp. Fix the time and the incentive.")
hr(); print("Incident drill: 'fraud flags are 3× higher for one postcode area.'\n  T+0 log it · T+1h freeze auto-actions for the segment · T+1d root cause (proxy feature?) · T+3d notify DPO/legal to assess duties · T+10d fix, re-evaluate, board note")
say("The review board's product is a written decision with conditions and a date. Everything else is conversation.")
