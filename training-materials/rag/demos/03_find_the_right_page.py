"""Build Your Own AI Bot (RAG for non-technical people) · Demo 3 — Day 3 — finding the right page: one change at a time (20 min) · Module 3
Shows: retrieval recall on a test sheet as you add query rewriting, hybrid search, reranking and change top-k — one change per run
Lab: In your no-code tool make ONE change (hybrid on, then reranker on, then top-k). Record before/after on your ten questions in the scoring grid.
Run: python 03_find_the_right_page.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Build Your Own AI Bot (RAG for non-technical people) · Demo 3 — Day 3 — finding the right page: one change at a time")
import csv, pathlib; tests = [t for t in csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv")) if t["type"] != "out_of_scope"]
chunks = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]
REWRITE = {"money back": "refund", "holiday": "annual leave", "broken": "damaged", "pwd": "password"}
def rw(q):
    for k, v in REWRITE.items(): q = q.lower().replace(k, v)
    return q
def run(mode, k, rr=False, rewrite=False):
    hit = 0
    for t in tests:
        q = rw(t["question"]) if rewrite else t["question"]; r = bm25(q, chunks) if mode == "keyword" else semantic(q, chunks) if mode == "meaning" else rrf(bm25(q, chunks), semantic(q, chunks))
        top = rerank(q, [c for _, c in r[:8]], k) if rr else [c for _, c in r[:k]]; hit += any(t["expected"].split(";")[0].lower()[:13] in c["text"].lower() for c in top)
    return hit
steps = [("keyword only, top-3", run("keyword", 3)), ("+ query rewriting", run("keyword", 3, rewrite=True)), ("+ hybrid (keyword + meaning)", run("hybrid", 3, rewrite=True)), ("+ reranker", run("hybrid", 3, True, True)), ("top-k 3 → 5", run("hybrid", 5, True, True)), ("top-k 5 → 1 (too greedy)", run("hybrid", 1, True, True))]
for n, h in steps: print(f"  {h:>2}/{len(tests)}  {bar(h, len(tests), 20)}  {n}")
print(f"\n  Cost of top-5 vs top-3: about {tokens(' '.join(c['text'] for c in chunks[:5])) - tokens(' '.join(c['text'] for c in chunks[:3]))} more input tokens per question — accuracy is not free.")
say("One change, one measurement. If you change three things and it improves, you learned nothing.")
