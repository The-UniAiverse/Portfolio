"""Calculating LLM Cost & Estimation Strategies · Demo 3 — Cost a real feature: three designs and a sensitivity analysis (20 min) · Module 4
Shows: one feature costed as basic, RAG and agentic designs using cost_calculator.py, then a tornado-style sensitivity showing which assumption moves the bill most
Lab: Cost your own feature with cost_calculator.py. Run the sensitivity. Put your effort into measuring the top assumption, not all six.
Run: python 03_cost_a_feature_sensitivity.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Calculating LLM Cost & Estimation Strategies · Demo 3 — Cost a real feature: three designs and a sensitivity analysis")
import importlib.util, pathlib; _s = importlib.util.spec_from_file_location("cc", pathlib.Path(__file__).resolve().parents[1] / "cost_calculator.py"); cc = importlib.util.module_from_spec(_s); _s.loader.exec_module(cc)

DAILY = arg("--daily", 2000, int); D_ = {"Basic (FAQ, cheap model)": dict(tier="cheap", system_tokens=800, context_tokens=0, history_tokens=500, question_tokens=80, answer_tokens=200), "RAG (mid model, 5 passages)": dict(tier="mid", system_tokens=1000, context_tokens=2500, history_tokens=1500, question_tokens=100, answer_tokens=400),
      "Agentic (6 steps)": dict(tier="mid", system_tokens=6000, context_tokens=30000, history_tokens=6000, question_tokens=100, answer_tokens=4000)}
table(["Design", "Per request", f"Per month @ {DAILY:,}/day"], [[n, f"${cc.per_request(**s):.4f}", money(cc.monthly(cc.per_request(**s), DAILY))] for n, s in D_.items()])
hr(); base = D_["RAG (mid model, 5 passages)"]; b = cc.monthly(cc.per_request(**base), DAILY); print(f"Sensitivity of the RAG design (base {money(b)}/month) — each assumption moved ±50%:\n"); sens = []
for k in ("context_tokens", "answer_tokens", "history_tokens", "system_tokens"):
    lo = cc.monthly(cc.per_request(**{**base, k: base[k] * 0.5}), DAILY); hi = cc.monthly(cc.per_request(**{**base, k: base[k] * 1.5}), DAILY); sens.append((k, lo, hi))
sens.append(("requests_per_day", b * 0.5, b * 1.5))
for k, lo, hi in sorted(sens, key=lambda x: -(x[2] - x[1])): print(f"  {k:<18}{money(lo):>8} … {money(hi):<8} {bar(hi - lo, b, 28)}")
print("\n  Volume and context size dominate. The system prompt barely matters once it is cached. Measure volume from logs; control context with top-k.")
say("An estimate is a list of assumptions with a total at the bottom. Know which assumption you are betting on.")
