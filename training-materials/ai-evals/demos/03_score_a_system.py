"""AI Evaluation & Quality Engineering · Demo 3 — Metrics: score a system end to end (25 min) · Module 3
Shows: retrieval metrics (recall@k, precision@k, MRR, nDCG) and answer metrics (correctness, faithfulness, refusal correctness) computed by hand-readable code, by question type
Lab: Score your own system on ten queries by hand first, then with code. Where do the numbers disagree with your gut? That gap is the point of the exercise.
Run: python 03_score_a_system.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Evaluation & Quality Engineering · Demo 3 — Metrics: score a system end to end")
import csv, pathlib; G = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv"))); docs = [d for d in load_docs() if "draft" not in d["id"].lower()]

ch = [c for d in docs for c in chunk_by_heading(d)]; rel = lambda t: {c["id"] for c in ch if evals.correctness(c["text"], t["expected"]) >= 0.7}; R = {"recall@3": 0, "precision@3": 0, "MRR": 0, "nDCG@5": 0}; A = {"correctness": 0, "faithfulness": 0, "refusal_correct": 0}; ans_n = 0; bytype = {}
for t in G:
    q = t["question"]; ranked = rerank(q, [c for _, c in rrf(bm25(q, ch), semantic(q, ch))[:8]], 8); ids = [c["id"] for c in ranked]; a = grounded(q, ranked[:3])[0]; oos = t["type"] == "out_of_scope"; A["refusal_correct"] += evals.refusal_correct(a, oos)
    if not oos:
        r = rel(t); ans_n += 1; R["recall@3"] += evals.recall_at_k(ids, r, 3); R["precision@3"] += evals.precision_at_k(ids, r, 3); R["MRR"] += evals.mrr(ids, r); R["nDCG@5"] += evals.ndcg(ids, {i: 1 for i in r}, 5)
        c_ = evals.correctness(a, t["expected"]); A["correctness"] += c_ >= 0.6; A["faithfulness"] += evals.faithfulness(a, [x["text"] for x in ranked[:3]]); bytype.setdefault(t["type"], []).append(c_ >= 0.6)
print("RETRIEVAL (did the right page reach the model?)"); [print(f"  {k:<13}{v / ans_n:.2f}") for k, v in R.items()]; print("\nANSWER (did the model use it properly?)"); print(f"  correctness     {A['correctness'] / ans_n:.2f}\n  faithfulness    {A['faithfulness'] / ans_n:.2f}\n  refusal correct {A['refusal_correct'] / len(G):.2f}")
print("\nBy question type:"); [print(f"  {k:<12}{sum(v)}/{len(v)}") for k, v in bytype.items()]
print("\n  Precision@3 is low BY DESIGN: usually one chunk is relevant, so the best possible is 0.33. Know the ceiling of every metric before you chase it.")
print("  Reading the pair: high recall + low correctness = generation problem · low recall = retrieval problem. Never tune the prompt to fix recall.")
say("One number hides everything. Report retrieval and answer metrics separately, by question type.")
