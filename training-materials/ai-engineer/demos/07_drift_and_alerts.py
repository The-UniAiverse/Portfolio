"""AI Engineer · Demo 7 — Monitoring: data drift, prediction drift, latency and cost alerts (25 min) · Module 7
Shows: PSI drift detection per feature between training and this week's traffic, prediction drift, and an SLO burn-rate alert — with what to do for each
Lab: Change `shift` until an alert fires. At what PSI would you retrain? Who gets the alert at 2 a.m. and what is the first thing they check?
Run: python 07_drift_and_alerts.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 7 — Monitoring: data drift, prediction drift, latency and cost alerts")
Xt, yt, names = ml.make_churn(n=1200); m = ml.LogReg(epochs=80).fit(Xt, yt); SHIFT = arg("--shift", 0.8)
Xw, yw, _ = ml.make_churn(n=600, seed=21, shift=SHIFT); rows = []
for j, nm in enumerate(names[:4]): v = dataq.psi([r[j] for r in Xt], [r[j] for r in Xw]); rows.append([nm, f"{v:.3f}", dataq.psi_label(v)])
pv = dataq.psi(m.proba(Xt), m.proba(Xw)); rows.append(["→ model score", f"{pv:.3f}", dataq.psi_label(pv)]); table(["Signal", "PSI", "Status"], rows)
print(f"\n  Labels arrive 60 days late, so drift is your early warning. Flag rate: {sum(p >= .5 for p in m.proba(Xt)) / len(Xt):.0%} in training → {sum(p >= .5 for p in m.proba(Xw)) / len(Xw):.0%} this week.")
print(f"  AUC on the delayed labels: {ml.auc(yt, m.proba(Xt)):.3f} → {ml.auc(yw, m.proba(Xw)):.3f}")
hr(); s = ops.slo_burn(good=9880, total=10000, target=0.995); print(f"Service SLO 99.5% · last hour availability {s['availability']:.2%} · burn rate {s['burn_rate']:.1f}× → {s['action']}")
print("\nRUNBOOK\n  drift 'watch'   → open ticket, compare segments, no action on the model\n  drift 'DRIFTED' → freeze auto-decisions on the drifted segment, pull labelled sample, retrain candidate, canary\n  burn ≥ 2×       → ticket · burn ≥ 14× → page on-call, roll back last release first, investigate second")
say("Models do not break with an error message. They go quietly wrong. Drift is how you hear it.")
