"""AI Governance for Leaders · Demo 2 — Design your review process — and see its queue (12 min) · Module 3
Shows: a proportionate review process by tier simulated over a quarter: reviews needed, reviewer hours and where it jams
Lab: Set REQUESTS to your own expected pipeline. Is one board meeting a month enough? What would you delegate to make it flow?
Run: python 02_review_process_design.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Governance for Leaders · Demo 2 — Design your review process — and see its queue")
PROCESS = {"minimal": ("Self-assessment by owner", 0.5, "owner"), "limited": ("Review by AI governance lead", 3, "governance lead"), "high": ("Full review board + legal + security", 14, "review board"), "prohibited": ("Rejected at intake", 0.25, "intake")}
REQUESTS = {"minimal": 22, "limited": 9, "high": 3, "prohibited": 1}; table(["Tier", "Route", "Hours each", "Requests/quarter", "Hours"], [[t, PROCESS[t][0], PROCESS[t][1], n, PROCESS[t][1] * n] for t, n in REQUESTS.items()])
total = sum(PROCESS[t][1] * n for t, n in REQUESTS.items()); board = PROCESS["high"][1] * REQUESTS["high"]; print(f"\n  {total:.0f} reviewer hours a quarter · the board carries {board:.0f} h for {REQUESTS['high']} systems")
flat = sum(14 * n for n in REQUESTS.values()); print(f"  If EVERY request went to the full board: {flat} hours — {flat / total:.1f}× the load. That is how governance becomes the department of 'no'.")
print("\n  Minimum roles: system owner · AI governance lead · review board (risk, legal, security, business) · executive sponsor\n  Minimum artefacts: policy · inventory · classification record · review record · incident log")
say("Proportionate governance is fast for the harmless and thorough for the dangerous. One queue for everything fails both.")
