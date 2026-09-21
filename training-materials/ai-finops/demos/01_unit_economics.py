"""AI FinOps · Demo 1 — Unit economics: cost per request, per task, per user — and attribution (15 min) · Module 1
Shows: a month of usage logs turned into cost per request, per resolved task and per active user, attributed by feature and team, with the margin check
Lab: Compute the three unit costs for one of your features. Which one would your CFO recognise? Which one would your product owner act on?
Run: python 01_unit_economics.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI FinOps · Demo 1 — Unit economics: cost per request, per task, per user — and attribution")
r = rng(11); FEATS = {"support-assistant": ("support", "mid", 5100, 400, 0.62), "email-drafts": ("sales", "mid", 2200, 350, 0.80), "invoice-extraction": ("finance", "cheap", 3000, 250, 0.95), "research-agent": ("strategy", "mid", 42000, 4000, 0.55)}
VOL = {"support-assistant": 210000, "email-drafts": 38000, "invoice-extraction": 52000, "research-agent": 2100}; USERS = {"support-assistant": 140, "email-drafts": 60, "invoice-extraction": 9, "research-agent": 12}; rows = []; total = 0
for f, (team, tier, i, o, success) in FEATS.items():
    c = cost(i, o, tier); m = c * VOL[f]; total += m; rows.append([f, team, f"{VOL[f]:,}", f"${c:.4f}", f"${c / success:.4f}", f"${m / USERS[f]:.2f}", money(m)])
table(["Feature", "Team", "Requests", "Cost/request", "Cost/RESOLVED task", "Cost/user/month", "Month"], rows); print(f"\n  Total {money(total)} · the agent is {VOL['research-agent'] / sum(VOL.values()):.1%} of requests and {cost(42000, 4000) * VOL['research-agent'] / total:.0%} of spend.")
print("  Cost per RESOLVED task is the honest unit: a cheap answer that fails 45% of the time is not cheap.")
print(f"\n  Margin check — support contact handled by a person ≈ $2.50; by the assistant ${cost(5100, 400) / 0.62:.3f} per resolved contact → the case survives even a 10× price rise.")
print("  Attribution needs three tags on every call: team · feature · environment. No tags, no FinOps.")
say("The bill is per token. The business runs per task. FinOps is the translation.")
