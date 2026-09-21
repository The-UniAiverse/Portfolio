"""Calculating LLM Cost & Estimation Strategies · Demo 2 — Volume and growth: history growth and flagship-for-everything (12 min) · Module 3
Shows: how an untrimmed conversation grows cost quadratically turn by turn, and what 'just use the best model for everything' does to the monthly bill
Lab: Plot your own average conversation length. At which turn does the history cost more than the context? Set a trimming rule.
Run: python 02_volume_and_growth.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Calculating LLM Cost & Estimation Strategies · Demo 2 — Volume and growth: history growth and flagship-for-everything")
import importlib.util, pathlib; _s = importlib.util.spec_from_file_location("cc", pathlib.Path(__file__).resolve().parents[1] / "cost_calculator.py"); cc = importlib.util.module_from_spec(_s); _s.loader.exec_module(cc)

print("A 20-turn conversation, history never trimmed (each turn re-sends everything before it):\n"); cum = 0
for turn in (1, 5, 10, 15, 20):
    h = (turn - 1) * 350; c = cc.per_request("mid", 1000, 2500, h, 40, 250); cum_t = sum(cc.per_request("mid", 1000, 2500, (k - 1) * 350, 40, 250) for k in range(1, turn + 1)); print(f"  turn {turn:>2}: history {h:>5} tok → ${c:.4f} this turn {bar(c, 0.04, 22)} conversation so far ${cum_t:.3f}")
trim = sum(cc.per_request("mid", 1000, 2500, min((k - 1) * 350, 1400), 40, 250) for k in range(1, 21)); full = sum(cc.per_request("mid", 1000, 2500, (k - 1) * 350, 40, 250) for k in range(1, 21)); print(f"\n  20 turns untrimmed ${full:.3f} vs trimmed to the last 4 turns ${trim:.3f} → {1 - trim / full:.0%} saved with one rule.")
hr(); DAILY = arg("--daily", 5000, int); print(f"'Just use the flagship model for everything' at {DAILY:,} requests/day:")
for t in ("cheap", "mid", "flagship"): print(f"  {t:<9}{money(cc.monthly(cc.per_request(t, 1000, 2500, 1400, 40, 250), DAILY)):>10} / month")
print("\n  Growth to plan for: users × questions per user × turns per conversation × features. Each multiplies the others.")
say("Costs do not grow with users. They grow with users times turns times context. Trim history before you negotiate price.")
