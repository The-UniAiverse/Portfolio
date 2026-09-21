"""AI Evaluation & Quality Engineering · Demo 5 — Evals in the lifecycle: CI gate, production sampling, feedback loop (20 min) · Module 5
Shows: a CI gate with floors and a regression rule, a production sampling plan sized for a confidence interval, and a feedback loop that turns thumbs-down into new golden queries
Lab: Write your gate: three floors and one regression rule. Decide your weekly production sample size from the interval you need.
Run: python 05_ci_gate_and_production_sampling.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Evaluation & Quality Engineering · Demo 5 — Evals in the lifecycle: CI gate, production sampling, feedback loop")
import math; BASE = {"correctness": 0.91, "faithfulness": 0.95, "refusal_correct": 0.97}; FLOORS = {"correctness": 0.85, "faithfulness": 0.90, "refusal_correct": 0.95}
PRS = {"#412 tweak system prompt wording": {"correctness": 0.92, "faithfulness": 0.95, "refusal_correct": 0.97}, "#413 switch to cheaper model": {"correctness": 0.86, "faithfulness": 0.93, "refusal_correct": 0.96}, "#414 'be more helpful' prompt": {"correctness": 0.93, "faithfulness": 0.88, "refusal_correct": 0.79}}
for pr, res in PRS.items():
    ok, fails = evals.gate(res, FLOORS, BASE, max_drop=0.03); print(f"\n  PR {pr}: {'✓ MERGE' if ok else '✗ BLOCKED'}"); [print(f"      {f}") for f in fails]
print("\n  #413 passes every floor and is still blocked: a 5-point drop in correctness is a decision for a human, with the cost saving on the table next to it.")
hr(); print("Production sampling — how many answers to review each week?")
for n in (50, 100, 200, 400): p = 0.9; ci = 1.96 * math.sqrt(p * (1 - p) / n); print(f"  n={n:<4} → 90% measured ± {ci:.1%}   ({n * 1.5 / 60:.1f} reviewer-hours at 90 s each)")
print("  Stratify the sample: all thumbs-down + all 'not found' + a random slice. Random alone under-samples the failures.")
hr(); FB = [("How do I get my money back for a broken parcel?", "thumbs_down", "answered with late-delivery rule"), ("what is ERR_AUTH_2210", "thumbs_up", ""), ("can I carry leave to next year", "not_found", "policy exists → retrieval miss")]
print("Feedback loop this week:"); [print(f"  {s:<12} '{q}' → {'ADD to golden set as paraphrase; ' + why if s != 'thumbs_up' else 'no action'}") for q, s, why in FB]
say("Evals are not a phase. They run before merge, after deploy, and every week on what real users asked.")
