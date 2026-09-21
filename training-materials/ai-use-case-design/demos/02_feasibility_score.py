"""AI Use-Case Design & Product Ownership · Demo 2 — Data and feasibility: score it before you promise it (15 min) · Module 2
Shows: a seven-question data checklist per use case turned into a feasibility score with the single biggest blocker named
Lab: Score your own use case. Take the lowest line to the data owner this week — that conversation is the real lab.
Run: python 02_feasibility_score.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Use-Case Design & Product Ownership · Demo 2 — Data and feasibility: score it before you promise it")
Q = ["Data exists for the task", "We can access it (technically)", "We are allowed to use it (lawful basis, contracts)", "Quality is known and acceptable", "It has the labels / right answers we need to evaluate", "It is fresh enough", "Permissions per user can be enforced"]
UC = {"Shipment-status assistant": [5, 4, 4, 3, 2, 5, 3], "Invoice extraction": [5, 5, 4, 3, 4, 5, 5], "Churn prediction for SME customers": [3, 2, 3, 2, 1, 3, 4]}
for name, s in UC.items():
    score = sum(s) / (5 * len(s)) * 100; worst = min(range(len(s)), key=lambda i: s[i]); verdict = "GO to POC" if score >= 70 and min(s) >= 3 else "FIX FIRST" if score >= 50 else "NOT YET"
    print(f"\n{name}  —  feasibility {score:.0f}/100  →  {verdict}"); [print(f"   {q:<52} {bar(v, 5, 10)} {v}") for q, v in zip(Q, s)]; print(f"   Biggest blocker: {Q[worst]} ({s[worst]}/5)")
hr(); print("Rule used: GO needs 70+ overall AND no line under 3. One '1' on permissions or lawful basis stops a project however good the rest looks.")
say("Most AI projects do not fail at the model. They fail at question five: we never had the right answers to test against.")
