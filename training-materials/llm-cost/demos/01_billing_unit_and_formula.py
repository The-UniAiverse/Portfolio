"""Calculating LLM Cost & Estimation Strategies · Demo 1 — The billing unit and the per-request formula: whiteboard the $0.014 question (15 min) · Module 1+2
Shows: text → tokens → dollars: input vs output vs cached input, then one request built up line by line (system + context + history + question + answer)
Lab: By hand, on paper: cost one question to your own assistant. Then check with the script. Which line surprised you?
Run: python 01_billing_unit_and_formula.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Calculating LLM Cost & Estimation Strategies · Demo 1 — The billing unit and the per-request formula: whiteboard the $0.014 question")
import importlib.util, pathlib; _s = importlib.util.spec_from_file_location("cc", pathlib.Path(__file__).resolve().parents[1] / "cost_calculator.py"); cc = importlib.util.module_from_spec(_s); _s.loader.exec_module(cc)

S = "How late must a delivery be before I can claim a refund of the shipping fee?"; print(f"'{S}'\n  {len(S)} characters ≈ {tokens(S)} tokens (rule of thumb: 4 characters per token in English; Indian languages often 2–3× more)\n")
r = cc.RATES["mid"]; table(["Token type (mid-tier model)", "$ per 1M", "Relative"], [["input", r["in"], "1×"], ["output", r["out"], f"{r['out'] / r['in']:.0f}×"], ["cached input", r["cached_in"], f"{r['cached_in'] / r['in']:.1f}×"]]); print("  Reasoning/'thinking' tokens are billed as OUTPUT — the most expensive kind — even though the user never sees them.")
hr(); parts = [("system prompt", 1000, "in"), ("retrieved context (5 passages)", 2500, "in"), ("chat history", 700, "in"), ("the question", 20, "in"), ("the answer", 250, "out")]; tot = 0; print("One grounded question, line by line:")
for n, t, k in parts: c = t / 1e6 * r[k]; tot += c; print(f"  {n:<32}{t:>6} tok × ${r[k]:>5.2f}/M = ${c:.5f}")
print(f"  {'TOTAL':<32}{'':>6}                 ${tot:.4f}   ← the '$0.014 question'\n\n  The question itself is {20 / 1e6 * r['in'] / tot:.1%} of the cost. The answer is {250 / 1e6 * r['out'] / tot:.0%}. Context is {2500 / 1e6 * r['in'] / tot:.0%}.")
print("  Rates are illustrative — verify against the provider's price page and put the date on the slide.")
say("You are not paying for questions. You are paying for everything you send along with them, and five times more for every word that comes back.")
