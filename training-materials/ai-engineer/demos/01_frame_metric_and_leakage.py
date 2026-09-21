"""AI Engineer · Demo 1 — Problem framing: metric first, baseline, and the leakage trap (25 min) · Module 1
Shows: a churn task framed with a business-weighted metric and a naive baseline, then a too-good model exposed as feature leakage
Lab: Frame your own use case: target, unit of prediction, decision it drives, cost of each error type. Write the metric BEFORE opening a notebook.
Run: python 01_frame_metric_and_leakage.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 1 — Problem framing: metric first, baseline, and the leakage trap")
X, y, names = ml.make_churn(leak=True); a, b, c, d = ml.split(X, y); base = sum(d) / len(d)
print(f"Task: predict churn in the next 60 days · {len(X)} customers · churn rate {base:.0%}\nDecision it drives: who gets a retention call (capacity 25% of customers)\nCost of errors: missed churner = INR 6,000 lost · wasted call = INR 150\n")
print(f"Baseline 'nobody churns': accuracy {1 - base:.0%} — and it saves nothing. Accuracy is the wrong metric here.\n")
m = ml.LogReg().fit(a, b); met = ml.metrics(d, m.proba(c)); print(f"Model with ALL columns: AUC {met['auc']:.3f} · recall {met['recall']:.0%}   ← suspiciously good"); imp = ml.permutation_importance(m, c, d, names)
table(["Feature", "Importance (AUC drop when shuffled)"], [[n, f"{v:.3f}"] for n, v in imp[:4]])
print(f"\n  '{imp[0][0]}' dominates. When is it recorded? AFTER the customer has already said they are leaving. That is leakage.\n")
k = names.index("retention_call_made"); strip = lambda M: [r[:k] + r[k + 1:] for r in M]; m2 = ml.LogReg().fit(strip(a), b); p2 = m2.proba(strip(c)); met2 = ml.metrics(d, p2)
thr = sorted(p2, reverse=True)[len(p2) // 4]; tp, fp, fn, tn = ml.confusion(d, p2, thr); print(f"Honest model: AUC {met2['auc']:.3f}. Calling the top 25%: catches {tp}/{tp + fn} churners → value INR {tp * 6000 * 0.3 - (tp + fp) * 150:,.0f} per cycle (30% save rate)")
say("If the model looks brilliant on day one, ask what it knows that you would not know at prediction time.")
