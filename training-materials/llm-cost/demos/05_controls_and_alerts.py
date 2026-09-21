"""Calculating LLM Cost & Estimation Strategies · Demo 5 — Controls and monitoring: what to switch on, and the per-request alert (12 min) · Module 6
Shows: the four standard controls with their typical saving on this workload, and a per-request cost alert catching a runaway request before the invoice does
Lab: Set a per-request cost ceiling for your feature (p99 of normal + 50%). What should happen when it trips: block, degrade, or alert?
Run: python 05_controls_and_alerts.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Calculating LLM Cost & Estimation Strategies · Demo 5 — Controls and monitoring: what to switch on, and the per-request alert")
import importlib.util, pathlib; _s = importlib.util.spec_from_file_location("cc", pathlib.Path(__file__).resolve().parents[1] / "cost_calculator.py"); cc = importlib.util.module_from_spec(_s); _s.loader.exec_module(cc)

base = dict(tier="mid", system_tokens=1000, context_tokens=2500, history_tokens=6000, question_tokens=100, answer_tokens=600, cache_system=False); b = cc.per_request(**base)
C_ = [("Prompt caching", {**base, "cache_system": True}), ("+ history trimmed to 1.5k", {**base, "cache_system": True, "history_tokens": 1500}), ("+ output limit 300", {**base, "cache_system": True, "history_tokens": 1500, "answer_tokens": 300}), ("+ simple questions to cheap model", {**base, "tier": "cheap", "cache_system": True, "history_tokens": 1500, "answer_tokens": 300})]
print(f"  {'No controls':<36}${b:.4f}"); [print(f"  {n:<36}${cc.per_request(**s):.4f}  (-{1 - cc.per_request(**s) / b:.0%})") for n, s in C_]; print("  Batch processing: about half price for anything that can wait hours (reports, backfills, evals).")
hr(); r = rng(5); stream = [round(r.gauss(0.018, 0.003), 4) for _ in range(12)]; stream[8] = 0.41; CEIL = 0.05; print(f"Per-request alert (ceiling ${CEIL}):")
for i, c in enumerate(stream): print(f"  req {i + 1:>2}  ${c:.4f} {bar(min(c, 0.06), 0.06, 20)}" + ("  ← ALERT: 23× normal — agent loop re-sending a 90k-token document; request stopped at the cap, user shown a fallback" if c > CEIL else ""))
print(f"\n  Without the ceiling, that one pattern at 200 requests/day = {money(0.41 * 200 * 30)} a month — discovered on the invoice.")
say("Average cost tells you the budget. Maximum cost per request tells you whether someone is awake.")
