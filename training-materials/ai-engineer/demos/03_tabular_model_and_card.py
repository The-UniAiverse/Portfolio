"""AI Engineer · Demo 3 — Classical ML that still wins: boosting, calibration, explanation, model card (30 min) · Module 3
Shows: logistic regression vs gradient-boosted stumps trained from scratch, a calibration table, permutation importance, a group check and a generated model card
Lab: Train both models on your own tabular data (or change the seed and sample size). Which is better calibrated? Write the 'not intended for' line of your model card.
Run: python 03_tabular_model_and_card.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 3 — Classical ML that still wins: boosting, calibration, explanation, model card")
X, y, names = ml.make_churn(n=1200); a, b, c, d = ml.split(X, y); lr = ml.LogReg().fit(a, b); gb = ml.BoostedStumps().fit(a, b); P = {"Logistic regression": lr.proba(c), "Boosted stumps (40 rounds)": gb.proba(c)}
table(["Model", "AUC", "Precision", "Recall", "F1"], [[n] + [f"{ml.metrics(d, p)[k]:.3f}" for k in ("auc", "precision", "recall", "f1")] for n, p in P.items()])
best = max(P, key=lambda n: ml.metrics(d, P[n])["auc"]); p = P[best]; print(f"\nCalibration of {best} — when it says 70%, does 70% happen?"); table(["Predicted", "Actual", "Customers"], [[pct(a_), pct(b_), n] for a_, b_, n in ml.calibration(d, p)])
print("\nWhat drives it:"); model = lr if best.startswith("Log") else gb; [print(f"  {n:<18}{bar(max(v, 0), 0.12, 24)} {v:.3f}") for n, v in ml.permutation_importance(model, c, d, names)]
groups = ["annual" if r[5] else "monthly" for r in c]; g = ml.group_rates(d, p, groups); print("\nGroup check (contract type):"); table(["Group", "n", "Flagged", "Recall"], [[k, v["n"], pct(v["selection_rate"]), pct(v["recall"])] for k, v in g.items()])
hr(); print(f"MODEL CARD\n  Name            churn-{'lr' if model is lr else 'gbm'}:1.0 · trained 2026-09-21 on {len(a)} rows, tested on {len(c)}\n  Intended use    rank customers for retention calls; a human decides the offer\n  NOT intended    pricing, credit or any decision that denies service\n  Metrics         AUC {ml.metrics(d, p)['auc']:.3f} · recall {ml.metrics(d, p)['recall']:.0%} at 0.5\n  Known limits    trained on one region; annual-contract recall is lower (few churners) — monitor\n  Retrain when    PSI > 0.25 on any top-3 feature or AUC on monthly labelled sample < 0.75")
say("On tables, a small boosted model and a calibration check beat a large language model — and cost nothing to run.")
