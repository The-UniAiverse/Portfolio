"""AI for Business Leaders · Demo 3 — Readiness: the free snapshot, live (12 min) · Module 4
Shows: the 25-question Free readiness audit scored by the real engine: overall score, maturity level, weakest domains, red flags and 30-day actions
Lab: Everyone completes the Free snapshot for their own organisation at / (the audit page). Compare your three weakest domains with the table next to you.
Run: python 03_readiness_snapshot.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Business Leaders · Demo 3 — Readiness: the free snapshot, live")
c = api(); req = c.get("/api/readiness_audit/sample?tier=free").json(); r = c.post("/api/readiness_audit/run", json=req).json()
print(f"{r['organisation']['name']} · {r['answered_count']}/{r['question_count']} answered · score {r['overall_score']}/100 · {r['maturity_level']}\n  {r['maturity_summary']}\n")
for d in sorted(r["dimensions"], key=lambda d: d["score"]): print(f"  {d['title'][:46]:<46} {bar(d['score'], 100, 25)} {d['score']:5.1f}")
print("\nRed flags:"); [print(f"  ! {(f.get('question', str(f)) if isinstance(f, dict) else str(f))[:110]}") for f in r["red_flags"][:3]]
print("\nFirst 30 days:"); [print(f"  {x['priority']}. {x['action'][:110]}") for x in r["recommendations"]]
print(f"\n  {r['upgrade_hint'][:160]}")
say("The score is not a grade. It is the order in which to fix things.")
