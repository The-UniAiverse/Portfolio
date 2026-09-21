"""AI Development & Deployment Lifecycle · Demo 1 — Phases 1–4: run a gate review on real evidence (30 min) · Module 1
Shows: discovery → solution definition → architecture → build, each with exit criteria checked against a project's evidence file; the gate decision and its conditions
Lab: Fill data/project.yaml for a project you know. Run the review. Present the gate decision to the room as the sponsor would hear it: go, conditional go, or stop.
Run: python 01_gate_review_phases_1_4.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Development & Deployment Lifecycle · Demo 1 — Phases 1–4: run a gate review on real evidence")
import yaml; P = yaml.safe_load(data_path(__file__, "project.yaml").read_text()); E = P["evidence"]
PHASES = [("1 Discovery", ["problem_statement", "business_case", "named_owner"]), ("2 Solution definition", ["data_access_agreed", "eval_set_defined", "success_metric_baseline"]), ("3 Architecture", ["architecture_doc", "threat_model", "cost_model"]), ("4 Build", ["poc_results_vs_target", "test_report", "model_or_prompt_versioned"])]
print(f"{P['project']} · sponsor {P['sponsor']} · risk tier {P['risk_tier']}\n")
for ph, crit in PHASES:
    miss = [c for c in crit if not E.get(c)]; print(f"  Phase {ph:<24} {'PASS' if not miss else 'CONDITIONAL'}   " + " ".join(f"[{'x' if E.get(c) else ' '}] {c}" for c in crit))
miss = [c for _, cr in PHASES for c in cr if not E.get(c)]; hard = [m for m in miss if m in ("eval_set_defined", "named_owner", "data_access_agreed")]
print(f"\n  GATE DECISION: {'STOP — ' + ', '.join(hard) if hard else 'CONDITIONAL GO — close within 10 working days: ' + ', '.join(miss) if miss else 'GO'}")
print("  Why conditional and not stop: a missing threat model can be fixed in days; a missing eval set or owner means the project cannot know if it works.")
print("\nWorked example of cost of skipping a gate: teams that discover 'no labelled answers' in Phase 4 instead of Phase 2 typically rebuild the POC — the gate costs an hour, the rebuild costs weeks.")
say("A gate is not a meeting. It is a list of evidence, and a decision somebody signs.")
