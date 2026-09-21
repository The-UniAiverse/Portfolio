"""AI Productivity Workflows · Demo 3 — Vendor comparison brief with a sensitivity check (12 min) · Module 3
Shows: a weighted decision matrix with sourced scores, and a test of whether the winner survives a change of weights
Lab: Replace the three vendors and criteria with a real decision you face. Does the winner change when you double the weight of your biggest worry?
Run: python 03_vendor_comparison.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Productivity Workflows · Demo 3 — Vendor comparison brief with a sensitivity check")
W = {"Fit to need": 0.30, "Total 3-yr cost": 0.25, "Data & security": 0.25, "Ease of rollout": 0.20}
V = {"Vendor A": ([4, 3, 5, 3], ["demo 12 Sep", "quote v2", "ISO 27001 cert + DPA", "ref call"]), "Vendor B": ([5, 2, 3, 4], ["demo 14 Sep", "quote v1", "no India region", "ref call"]), "Vendor C": ([3, 5, 4, 4], ["trial", "price list", "SOC 2 report", "trial"])}
def total(w): return sorted(((sum(s * x for s, x in zip(sc, w.values())), n) for n, (sc, _) in V.items()), reverse=True)
table(["Vendor"] + list(W) + ["Weighted"], [[n] + [f"{s} ({src})" for s, src in zip(sc, srcs)] + [f"{sum(s * x for s, x in zip(sc, W.values())):.2f}"] for n, (sc, srcs) in V.items()])
base = total(W); print(f"\n  Recommendation: {base[0][1]} ({base[0][0]:.2f}) over {base[1][1]} ({base[1][0]:.2f})"); hr(); print("Sensitivity — does the answer survive?")
for k in W:
    w2 = {c: (v * 2 if c == k else v) for c, v in W.items()}; s = sum(w2.values()); w2 = {c: v / s for c, v in w2.items()}; t = total(w2)
    print(f"  double '{k}': winner {t[0][1]} {'(unchanged)' if t[0][1] == base[0][1] else '← CHANGES'}")
print("\nDecision memo skeleton: 1) Decision needed by · 2) Recommendation in one line · 3) The table · 4) What would change our mind · 5) Risks and exit")
say("AI can fill the table in a minute. Your job is the weights, the sources and the one question: what would change our mind?")
