"""AI Evaluation & Quality Engineering · Demo 1 — Why 'it feels better' fails: the silent regression (15 min) · Module 1
Shows: a 'prompt improvement' that makes the three demo questions nicer and quietly breaks refusals — visible only on a test set
Lab: Think of the last change you shipped because 'it looked better'. Which three questions did you try? Write the five you did not.
Run: python 01_feels_better_fails.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Evaluation & Quality Engineering · Demo 1 — Why 'it feels better' fails: the silent regression")
import csv, pathlib; G = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv"))); docs = [d for d in load_docs() if "draft" not in d["id"].lower()]

ch = [c for d in docs for c in chunk_by_heading(d)]
def sys_a(q): return grounded(q, rerank(q, [c for _, c in rrf(bm25(q, ch), semantic(q, ch))[:8]], 3))[0]
def sys_b(q):
    """'Improved': friendlier, always tries to help (never refuses), meaning-search only (dropped keyword search to save latency)."""
    top = [c for _, c in semantic(q, ch)[:3]]; a = grounded(q, top)[0]
    if "could not find" in a.lower(): a = "Great question! " + " ".join(top[0]["text"].split()[:25]) + "…"
    return "Happy to help! " + a
DEMO = G[:3]; print("The three questions everyone tries in the review meeting:")
for t in DEMO: print(f"  Q: {t['question'][:60]}\n     A: {sys_a(t['question'])[:80]}\n     B: {sys_b(t['question'])[:95]}")
print("\n  Verdict in the room: 'B feels friendlier. Ship it.'"); hr()
def score(f): return {ty: sum((evals.refusal_correct(f(t["question"]), True) if ty == "out_of_scope" else evals.correctness(f(t["question"]), t["expected"]) >= 0.6) for t in G if t["type"] == ty) for ty in dict.fromkeys(t["type"] for t in G)}
a, b = score(sys_a), score(sys_b); n = {ty: sum(t["type"] == ty for t in G) for ty in a}; table(["Question type", "n", "A (released)", "B ('feels better')"], [[ty, n[ty], a[ty], b[ty]] for ty in a] + [["TOTAL", len(G), sum(a.values()), sum(b.values())]])
lost = [ty for ty in a if b[ty] < a[ty]]; print(f"\n  B scores {sum(b.values())}/{len(G)} against A's {sum(a.values())}/{len(G)}. It lost: {', '.join(lost)}. B no longer refuses — ask it the CEO's salary and it now answers with confident filler.\n  Nobody in the review meeting asked an out-of-scope question. Nobody ever does.")
say("'It feels better' is a sample size of three, chosen by the person who made the change.")
