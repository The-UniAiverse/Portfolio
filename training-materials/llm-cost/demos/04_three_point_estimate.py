"""Calculating LLM Cost & Estimation Strategies · Demo 4 — Estimation strategies: bottom-up, top-down, from logs — and ranges, not numbers (15 min) · Module 5
Shows: three estimation methods applied to the same feature, reconciled into a three-point (PERT) range with a confidence statement you can put in a proposal
Lab: Produce a three-point estimate for your feature using at least two methods. Write the sentence you would put in the proposal.
Run: python 04_three_point_estimate.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Calculating LLM Cost & Estimation Strategies · Demo 4 — Estimation strategies: bottom-up, top-down, from logs — and ranges, not numbers")
import importlib.util, pathlib; _s = importlib.util.spec_from_file_location("cc", pathlib.Path(__file__).resolve().parents[1] / "cost_calculator.py"); cc = importlib.util.module_from_spec(_s); _s.loader.exec_module(cc)

bu = cc.monthly(cc.per_request("mid", 1000, 2500, 1500, 100, 400), 2000); td = 0.04 * 1200 * 30 * 0.6; logs = [0.0151, 0.0190, 0.0175, 0.0322, 0.0168, 0.0181, 0.0210, 0.0702, 0.0177, 0.0169]; lg = sum(logs) / len(logs) * 2000 * 30
table(["Method", "How", "Monthly"], [["Bottom-up", "tokens per request × rate × volume", money(bu)], ["Top-down", "1,200 users × 60% active × $0.04/user/day benchmark", money(td)], ["From pilot logs", f"mean of {len(logs)} real requests (${sum(logs) / len(logs):.4f}) × volume", money(lg)]])
print(f"\n  The log-based number is {lg / bu:.0%} of bottom-up: real traffic has a TAIL (two requests cost ${max(logs):.3f} and ${sorted(logs)[-2]:.3f}). Means hide it; p95 = ${sorted(logs)[-1]:.3f}.")
o, m, p = min(bu, td, lg) * 0.8, lg, max(bu, td, lg) * 1.6; e, sd = biz.pert(o, m, p); hr(); print(f"Three-point estimate: optimistic {money(o)} · most likely {money(m)} · pessimistic {money(p)}\n  PERT expected {money(e)} ± {money(sd)}  →  80% range {money(e - 1.28 * sd)} to {money(e + 1.28 * sd)} per month")
print(f"\nProposal sentence:\n  \"We estimate run cost at {money(e)} per month (80% confidence: {money(e - 1.28 * sd)}–{money(e + 1.28 * sd)}), based on pilot logs of {len(logs)} requests and 2,000 requests/day.\n   The estimate is most sensitive to volume and retrieved context size; we will re-baseline after four weeks of production data.\"")
say("A single number is a promise you cannot keep. A range with its assumptions is an estimate you can defend.")
