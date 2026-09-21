"""AI FinOps · Demo 2 — Controls: caching, routing, batch, output limits, agent caps — measured (25 min) · Module 2
Shows: six cost controls applied one at a time to the same workload, showing the saving, the quality risk and the effort of each
Lab: Pick the three controls with the best saving-to-risk ratio for YOUR workload. Estimate the monthly saving and name the owner for each.
Run: python 02_apply_three_controls.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI FinOps · Demo 2 — Controls: caching, routing, batch, output limits, agent caps — measured")
import importlib.util, pathlib; spec = importlib.util.spec_from_file_location("cc", pathlib.Path(__file__).resolve().parents[2] / "llm-cost" / "cost_calculator.py"); cc = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
DAILY = 7000; base = dict(tier="mid", system_tokens=1800, context_tokens=2500, history_tokens=6000, question_tokens=100, answer_tokens=600, cache_system=False); b = cc.monthly(cc.per_request(**base), DAILY); steps = [("Baseline (no controls)", b, "—", "—")]
c1 = cc.monthly(cc.per_request(**{**base, "cache_system": True}), DAILY); steps.append(("1 Prompt caching (system prompt)", c1, "none", "hours"))
c2 = cc.monthly(cc.per_request(**{**base, "cache_system": True, "history_tokens": 1500}), DAILY); steps.append(("2 Trim/summarise history to 1.5k", c2, "low — test multi-turn", "days"))
c3 = cc.monthly(cc.per_request(**{**base, "cache_system": True, "history_tokens": 1500, "answer_tokens": 300}), DAILY); steps.append(("3 Output limit 600 → 300 tokens", c3, "low — check truncation", "hours"))
mix = 0.55 * cc.per_request(**{**base, "tier": "cheap", "cache_system": True, "history_tokens": 1500, "answer_tokens": 300, "context_tokens": 800}) + 0.45 * cc.per_request(**{**base, "cache_system": True, "history_tokens": 1500, "answer_tokens": 300}); c4 = cc.monthly(mix, DAILY); steps.append(("4 Route 55% simple → cheap model", c4, "medium — needs evals per route", "weeks"))
c5 = c4 * (1 - 0.2 * 0.5); steps.append(("5 Batch API for the 20% offline jobs (-50%)", c5, "none — latency only", "days")); c6 = c5 * 0.93; steps.append(("6 Response cache for repeat questions (7% hits)", c6, "low — invalidate on doc change", "days"))
table(["Control", "Monthly cost", "vs baseline", "Quality risk", "Effort"], [[n, money(v), f"-{1 - v / b:.0%}" if v != b else "", risk, eff] for n, v, risk, eff in steps])
print(f"\n  {money(b)} → {money(c6)} a month ({1 - c6 / b:.0%} less). The first three controls need no quality trade-off and deliver {(b - c3) / (b - c6):.0%} of the saving.")
print("  Agent caps (steps, cost per task) do not lower the average — they remove the tail: the one task that costs $40.  Quantisation applies if you self-host.")
say("Do the free controls first: cache, trim, cap the output. Routing is the big one, and the only one that needs an eval suite.")
