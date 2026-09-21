"""AI Development & Deployment Lifecycle · Demo 2 — Phases 5–8: take a mock project through all gates to handover and scale (30 min) · Module 2
Shows: operationalisation → validation & governance → deployment & handover → optimise & scale; a full eight-phase scorecard, readiness percentage and the handover pack contents
Lab: Take your project through all eight phases. Which phase has the least evidence? That is where your go-live risk lives.
Run: python 02_mock_project_all_gates.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Development & Deployment Lifecycle · Demo 2 — Phases 5–8: take a mock project through all gates to handover and scale")
import yaml, pathlib; P = yaml.safe_load((pathlib.Path(__file__).with_name("data") / "project.yaml").read_text()); E = P["evidence"]
ALL = [("1 Discovery", ["problem_statement", "business_case", "named_owner"]), ("2 Solution definition", ["data_access_agreed", "eval_set_defined", "success_metric_baseline"]), ("3 Architecture", ["architecture_doc", "threat_model", "cost_model"]), ("4 Build", ["poc_results_vs_target", "test_report", "model_or_prompt_versioned"]),
       ("5 Operationalisation", ["monitoring_live", "runbook"]), ("6 Validation & governance", ["governance_review_signed", "threat_model"]), ("7 Deployment & handover", ["user_training_done", "handover_accepted"]), ("8 Optimise & scale", ["benefits_tracking", "cost_model"])]
for ph, crit in ALL: got = sum(bool(E.get(c)) for c in crit); print(f"  {ph:<28}{bar(got, len(crit), 12)} {got}/{len(crit)}   {', '.join(c for c in crit if not E.get(c)) or 'complete'}")
tot = sum(bool(E.get(c)) for _, cr in ALL for c in cr); n = sum(len(cr) for _, cr in ALL); print(f"\n  Production readiness: {tot}/{n} = {tot / n:.0%}.  Built ≠ ready: phases 1–4 are {sum(bool(E.get(c)) for _, cr in ALL[:4] for c in cr)}/12, phases 5–8 are {sum(bool(E.get(c)) for _, cr in ALL[4:] for c in cr)}/8.")
print("\nHANDOVER PACK (what the run team signs for):\n  architecture + data flows · model/prompt versions and how to roll back · eval set + last results · runbook + alert owners\n  cost model + budget owner · risk tier, controls, review record · user guide + training record · open issues with owners")
print("\n  The uniAIverse Delivery Framework at /delivery generates this pack, the gate checklists and the estimates for a real engagement.")
say("Most AI projects are 'done' at phase 4 and abandoned at phase 5. The second half of the lifecycle is where value is kept or lost.")
