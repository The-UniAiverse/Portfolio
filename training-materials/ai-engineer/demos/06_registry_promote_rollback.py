"""AI Engineer · Demo 6 — MLOps: two versions, a gated promotion, a canary and a rollback (25 min) · Module 6
Shows: a model registry with evidence-based promotion, a canary comparison on live-like traffic, and a one-command rollback when the new version misbehaves
Lab: Register a third version that is better on AUC but has no model card. What happens? Decide your own three promotion gates and write them down.
Run: python 06_registry_promote_rollback.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 6 — MLOps: two versions, a gated promotion, a canary and a rollback")
X, y, n = ml.make_churn(n=1200); a, b, c, d = ml.split(X, y); reg = ops.Registry(); v1 = ml.LogReg(epochs=60).fit(a, b); v2 = ml.BoostedStumps(rounds=40).fit(a, b); v3 = ml.LogReg(epochs=5, lr=0.05).fit(a, b)
card = {"intended_use": "rank customers for retention calls"}; GATES = {"auc": 0.75, "recall": 0.40}
for ver, m, cd in (("1.0", v1, card), ("2.0", v2, card), ("3.0-rushed", v3, {})): reg.register("churn", ver, ml.metrics(d, m.proba(c)), artefact=ver, card=cd)
for ver in ("1.0", "3.0-rushed", "2.0"):
    ok, why = reg.promote("churn", ver, GATES); print(f"  promote churn:{ver:<11} → {'PRODUCTION' if ok else 'REJECTED: ' + '; '.join(why)}")
hr(); Xs, ys, _ = ml.make_churn(n=600, seed=99, shift=0.0); can = ops.canary(v1.proba(Xs), v2.proba(Xs), ys, share=0.1); print(f"Canary on 10% of live traffic: old error {can['old_error']:.1%} · new error {can['new_error']:.1%} → {'keep new' if can['switch'] else 'ROLL BACK'}")
print("\nIncident: 2.0 starts timing out under load (p95 4.2 s vs SLO 1 s)."); prev = reg.rollback("churn"); print(f"  rollback → production is now churn:{prev} · time to restore: one command, no rebuild")
print("\nAudit trail:"); [print("  " + l) for l in reg.log]
say("Promotion is a decision with evidence. Rollback is a button you tested before you needed it.")
