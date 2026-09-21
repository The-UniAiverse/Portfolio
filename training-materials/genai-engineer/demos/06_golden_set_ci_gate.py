"""GenAI Engineer · Demo 6 — Evaluation: a golden set, four metrics, a calibrated judge and a CI gate (25 min) · Module 6
Shows: the full eval loop: golden set → retrieval + answer metrics → rubric judge checked against human labels → a CI gate that blocks a regression
Lab: Write 10 golden queries for your system with expected facts and type. Wire `evals.gate` into your CI so a drop of more than 3 points fails the build.
Run: python 06_golden_set_ci_gate.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("GenAI Engineer · Demo 6 — Evaluation: a golden set, four metrics, a calibrated judge and a CI gate")
import csv, pathlib; G = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv"))); docs = [d for d in load_docs() if "draft" not in d["id"].lower()]
def system(version):
    ch = [c for d in docs for c in (chunk_by_heading(d) if version == "v2" else chunk_fixed(d, 300))]
    def f(q): top = rerank(q, [c for _, c in rrf(bm25(q, ch), semantic(q, ch))[:8]], 3) if version == "v2" else [c for _, c in semantic(q, ch)[:3]]; return grounded(q, top)[0], top
    return f
def score(sysf):
    C = F = R = 0; n_ref = sum(t["type"] == "out_of_scope" for t in G); J = []
    for t in G:
        a, top = sysf(t["question"]); oos = t["type"] == "out_of_scope"; C += (evals.correctness(a, t["expected"]) >= 0.6) if not oos else 0; F += evals.faithfulness(a, [c["text"] for c in top]); R += evals.refusal_correct(a, oos); J.append(evals.judge(t["question"], a)["total"])
    n = len(G); return {"correctness": C / (n - n_ref), "faithfulness": F / n, "refusal_correct": R / n, "judge": sum(J) / n}
base, cand = score(system("v1")), score(system("v2")); table(["Metric", "v1 (released)", "v2 (candidate)"], [[k, f"{base[k]:.2f}", f"{cand[k]:.2f}"] for k in base])
hr(); sysf = system("v2"); ans = [sysf(t["question"])[0] for t in G]
human = [int(evals.refusal_correct(a, True)) if t["type"] == "out_of_scope" else int(evals.correctness(a, t["expected"]) >= 0.6) for t, a in zip(G, ans)]; human[2] = 1 - human[2]   # people also disagree a little
def report(name, labels):
    k = evals.cohen_kappa(human, labels); print(f"  {name:<44} agreement {sum(a == b for a, b in zip(human, labels)) / len(human):.0%} · kappa {k:5.2f} → {'usable as a gate' if k >= 0.6 else 'NOT trustworthy — it is measuring style, not truth'}")
print("Judge calibration against 14 human pass/fail labels:")
report("rubric v1 (grounded, specific, concise, tone)", [int(evals.judge(t["question"], a)["total"] >= 0.75) for t, a in zip(G, ans)])
report("rubric v2 (+ 'matches the reference facts')", [int(evals.judge(t["question"], a)["total"] >= 0.5 and (evals.refusal_correct(a, True) if t["type"] == "out_of_scope" else evals.correctness(a, t["expected"]) >= 0.6)) for t, a in zip(G, ans)])
hr(); FLOORS = {"correctness": 0.70, "faithfulness": 0.85, "refusal_correct": 0.90}
for name, res, bl in (("v2 vs released v1", cand, base), ("a careless change (v1 re-submitted against v2 baseline)", base, cand)):
    ok, fails = evals.gate(res, FLOORS, bl); print(f"CI gate — {name}: {'PASS ✓ merge allowed' if ok else 'FAIL ✗'}"); [print(f"    {f}") for f in fails]
say("An LLM judge is an instrument. Calibrate it against people before you let it fail a build.")
