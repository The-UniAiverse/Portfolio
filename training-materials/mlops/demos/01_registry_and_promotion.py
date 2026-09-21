"""MLOps & LLMOps · Demo 1 — Model lifecycle: registry, gated promotion, blue/green, retirement (25 min) · Module 1
Shows: three model versions through a registry with promotion gates and evidence, a blue/green switch with canary, rollback, and a retirement checklist
Lab: Define the promotion gates for one of your models (metrics, card, approver). Practise a rollback on a test endpoint and time it.
Run: python 01_registry_and_promotion.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("MLOps & LLMOps · Demo 1 — Model lifecycle: registry, gated promotion, blue/green, retirement")
X, y, _ = ml.make_churn(n=1000); a, b, c, d = ml.split(X, y); reg = ops.Registry(); M = {"1.0": ml.LogReg(epochs=40).fit(a, b), "1.1": ml.LogReg(epochs=150).fit(a, b), "2.0-exp": ml.BoostedStumps(rounds=8).fit(a, b)}
for v, m in M.items(): reg.register("churn", v, ml.metrics(d, m.proba(c)), artefact=v, card={"intended_use": "retention ranking"} if v != "2.0-exp" else {})
table(["Version", "AUC", "Recall", "Card", "Hash"], [[v, f"{reg.versions[('churn', v)]['metrics']['auc']:.3f}", f"{reg.versions[('churn', v)]['metrics']['recall']:.2f}", "yes" if reg.versions[("churn", v)]["card"] else "NO", reg.versions[("churn", v)]["hash"]] for v in M])
print(); [print(f"  promote {v:<8} → {'PRODUCTION' if ok else 'rejected: ' + '; '.join(w)}") for v in ("1.0", "2.0-exp", "1.1") for ok, w in [reg.promote("churn", v, {"auc": 0.75})]]
can = ops.canary(M["1.0"].proba(c), M["1.1"].proba(c), d, 0.2); print(f"\n  Blue/green: 1.1 (green) took 20% of traffic — error {can['new_error']:.1%} vs blue {can['old_error']:.1%} → {'switch 100%' if can['switch'] else 'stay on blue'}")
print(f"  Drill: rollback → {reg.rollback('churn')} restored (one command).  Then re-promote after the fix.")
print("\nRetirement checklist for 1.0: no traffic for 30 days · consumers notified · artefact archived with its training-data hash · card marked 'retired' · monitoring removed")
print("\nAudit trail:"); [print("   " + l) for l in reg.log]
say("If you cannot say which version answered a customer last Tuesday, you do not have MLOps yet.")
