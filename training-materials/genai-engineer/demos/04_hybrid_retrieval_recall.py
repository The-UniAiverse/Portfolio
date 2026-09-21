"""GenAI Engineer · Demo 4 — Embedding, hybrid retrieval and reranking: recall@k and nDCG (25 min) · Module 4
Shows: keyword vs meaning vs hybrid (RRF) vs hybrid+rerank scored with recall@1/3/8, MRR and nDCG on a labelled set — and the latency/cost of each stage
Lab: Build a 20-query labelled set for your corpus (query → relevant chunk ids). Report recall@20 for retrieval and nDCG@5 after reranking. Which stage is your bottleneck?
Run: python 04_hybrid_retrieval_recall.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("GenAI Engineer · Demo 4 — Embedding, hybrid retrieval and reranking: recall@k and nDCG")
import csv, pathlib; tests = [t for t in csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv")) if t["type"] != "out_of_scope"]; ch = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]
def relevant(t): return {c["id"] for c in ch if evals.correctness(c["text"], t["expected"]) >= 0.7}
def ranked(q, mode):
    if mode == "keyword (BM25)": r = bm25(q, ch)
    elif mode == "meaning (dense)": r = semantic(q, ch)
    else: r = rrf(bm25(q, ch), semantic(q, ch))
    ids = [c for _, c in r[:8]]
    if mode.endswith("rerank"): ids = rerank(q, ids, 8)
    return [c["id"] for c in ids]
rows = []
for mode in ("keyword (BM25)", "meaning (dense)", "hybrid (RRF)", "hybrid + rerank"):
    R1 = R3 = R8 = M = N = 0
    for t in tests:
        rel = relevant(t); ids = ranked(t["question"], mode); R1 += evals.recall_at_k(ids, rel, 1) > 0; R3 += evals.recall_at_k(ids, rel, 3) > 0; R8 += evals.recall_at_k(ids, rel, 8) > 0; M += evals.mrr(ids, rel); N += evals.ndcg(ids, {i: 1 for i in rel}, 5)
    n = len(tests); rows.append([mode, f"{R1 / n:.0%}", f"{R3 / n:.0%}", f"{R8 / n:.0%}", f"{M / n:.2f}", f"{N / n:.2f}"])
table(["Retriever", "hit@1", "hit@3", "hit@8", "MRR", "nDCG@5"], rows)
print("\n  Stage budget (typical):  retrieve 8 candidates ≈ 20–60 ms · rerank 8 ≈ 80–250 ms · generate ≈ 1–4 s.  Reranking is cheap next to generation.\n  Retrieval recall@k is the CEILING on answer quality. If the right chunk is not in the top-k, no prompt will save you.")
say("Measure retrieval separately from generation. Otherwise you will tune the prompt for a week to fix a search problem.")
