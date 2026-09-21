"""AI Evaluation & Quality Engineering · Demo 4 — LLM-as-judge: rubric, calibration, and three biases (25 min) · Module 4
Shows: a rubric judge calibrated against human labels, then tested for length bias, position bias and self-preference — with the fixes
Lab: Write a four-line rubric for your domain. Label 20 answers yourself first, THEN run the judge. If kappa is under 0.6, fix the rubric, not the labels.
Run: python 04_calibrate_a_judge.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Evaluation & Quality Engineering · Demo 4 — LLM-as-judge: rubric, calibration, and three biases")
ANS = [("Refunds are paid within 7 working days. (Source: Refund policy › Late delivery)", 1), ("Generally speaking it depends on many factors and you should check with the relevant team about your refund.", 0), ("7 working days.", 1),
       ("As an AI I think refunds are usually quick.", 0), ("The shipping fee is refunded within 7 working days if the parcel is over 24 hours late. (Source: Refund policy)", 1), ("Refunds take 30 days. (Source: Refund policy)", 0)]
J = [int(evals.judge("How long do refunds take?", a)["total"] >= 0.75) for a, _ in ANS]; H = [h for _, h in ANS]; table(["Answer", "Human", "Judge"], [[a[:70], h, j] for (a, h), j in zip(ANS, J)])
print(f"\n  agreement {sum(a == b for a, b in zip(H, J)) / len(H):.0%} · kappa {evals.cohen_kappa(H, J):.2f}\n  Row 3: short and correct, but the judge failed it (no citation, 'not specific'). Row 6: confidently WRONG with a citation — the judge passed it.\n  → a style rubric cannot see truth. Add a reference answer to the judge's input.")
hr(); print("Three biases to test for (each is a two-line experiment):")
short, long_ = "7 working days. (Source: Refund policy)", "Thank you for your question. " * 6 + "Refunds are typically processed in 7 working days. (Source: Refund policy)"
def naive_judge(a): return min(1.0, 0.4 + len(a.split()) / 60)       # what an uncalibrated 'rate this 0-1' prompt tends to do
print(f"  1 LENGTH    same fact, 6 vs {len(long_.split())} words: naive judge {naive_judge(short):.2f} vs {naive_judge(long_):.2f} → fix: rubric with a concision criterion (ours: {evals.judge('q', short)['total']:.2f} vs {evals.judge('q', long_)['total']:.2f})")
print("  2 POSITION  'Which is better, A or B?' favours A → fix: run both orders, count only consistent verdicts\n  3 SELF      a model prefers its own family's style → fix: judge with a different model family, or anchor with references")
say("A judge is a model making a prediction about quality. Measure its error like any other model's.")
