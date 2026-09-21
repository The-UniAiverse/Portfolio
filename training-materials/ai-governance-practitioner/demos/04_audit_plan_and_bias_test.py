"""AI Governance Practitioner · Demo 4 — Auditing AI: audit plan, evidence sampling and a bias & robustness test (30 min) · Module 4
Shows: a risk-based audit plan, an evidence request list, and a worked test: selection rates and recall by group with the four-fifths ratio, plus a robustness perturbation test
Lab: Write the audit plan for one high-risk system: scope, five evidence requests, two tests you will re-perform yourself. Run the bias test on real or synthetic outcomes.
Run: python 04_audit_plan_and_bias_test.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Governance Practitioner · Demo 4 — Auditing AI: audit plan, evidence sampling and a bias & robustness test")
PLAN = [("Governance", "policy, roles, review records", "inspect 3 review decisions end-to-end"), ("Data", "provenance, lawful basis, quality reports", "re-perform one quality check on a sample"), ("Model", "eval results incl. subgroups, model card", "RE-PERFORM the bias test below"), ("Operation", "monitoring, incidents, overrides", "trace 5 decisions from input to outcome"), ("Third parties", "vendor due diligence, contracts", "inspect DPA + model change notices")]
table(["Area", "Evidence to request", "Test"], [list(p) for p in PLAN]); hr(); X, y, names = ml.make_churn(n=1400, seed=4); r = rng(9); grp = ["urban" if r.random() < 0.6 else "rural" for _ in X]
for i, g in enumerate(grp):
    if g == "rural": X[i][2] += 1.5                                  # rural customers raise more tickets (patchy network), not more fraud/churn → proxy effect
a, b, c, d = ml.split(X, y); gt = ml.split(X, grp)[2] if False else None; idx = list(range(len(X))); __import__("random").Random(1).shuffle(idx); te = idx[int(len(X) * 0.7):]; gte = [grp[i] for i in te]
m = ml.LogReg(epochs=120).fit(a, b); p = m.proba(c); res = ml.group_rates(d, p, gte); table(["Group", "n", "Flag rate", "Recall", "Actual positive rate"], [[g, v["n"], pct(v["selection_rate"]), pct(v["recall"]), pct(sum(d[i] for i in range(len(d)) if gte[i] == g) / v["n"])] for g, v in res.items()])
ratio = min(v["selection_rate"] for v in res.values()) / max(v["selection_rate"] for v in res.values()); print(f"\n  Selection-rate ratio {ratio:.2f} (four-fifths screening threshold 0.80) → {'within threshold' if ratio >= 0.8 else 'DISPARITY — investigate: is support_tickets a proxy for location?'}\n  A ratio is a screen, not a verdict: compare with actual base rates and check recall parity before concluding.")
hr(); flips = sum((q >= .5) != (q2 >= .5) for q, q2 in zip(p, m.proba([[v * (1.05 if j == 1 else 1) for j, v in enumerate(row)] for row in c]))); print(f"Robustness: +5% on monthly_bill flips {flips}/{len(c)} decisions ({flips / len(c):.1%}). Above ~2% near the threshold deserves a finding.")
print("\nAudit report skeleton: scope · method · findings (condition, criterion, cause, effect, recommendation) · management response · follow-up date")
say("An auditor who only reads documents audits the documentation. Re-perform at least one test yourself.")
