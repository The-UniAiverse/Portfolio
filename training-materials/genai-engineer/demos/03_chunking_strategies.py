"""GenAI Engineer · Demo 3 — Chunking and enrichment: fixed vs structure-aware vs parent-child, measured (25 min) · Module 3
Shows: four chunking strategies compared on recall and tokens per answer — including parent-child retrieval (search small, read big) and the contextual prefix
Lab: Print ten of your own chunks. For each: would it make sense to a stranger? Then measure recall before and after adding the prefix.
Run: python 03_chunking_strategies.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("GenAI Engineer · Demo 3 — Chunking and enrichment: fixed vs structure-aware vs parent-child, measured")
import csv, pathlib; tests = [t for t in csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv")) if t["type"] != "out_of_scope"]; docs = [d for d in load_docs() if "draft" not in d["id"].lower()]
def parent_child(d):
    out = []
    for p in chunk_by_heading(d, contextual=False):
        for i, s in enumerate([x for x in __import__("re").split(r"(?<=[.!?])\s+", p["text"]) if len(x) > 25]): out.append({"id": f"{p['id']}.{i}", "doc": p["doc"], "heading": p["heading"], "text": s, "parent": p["text"]})
    return out
STRATS = {"fixed 200 chars": lambda d: chunk_fixed(d, 200), "fixed 400 chars": lambda d: chunk_fixed(d, 400), "by heading": lambda d: chunk_by_heading(d, contextual=False), "by heading + contextual prefix": lambda d: chunk_by_heading(d), "parent-child (search sentence, read section)": parent_child}
rows = []
for name, fn in STRATS.items():
    ch = [c for d in docs for c in fn(d)]; hit = tok = 0
    for t in tests:
        top = [c for _, c in rrf(bm25(t["question"], ch), semantic(t["question"], ch))[:3]]; read = " ".join(dict.fromkeys(c.get("parent", c["text"]) for c in top)); hit += evals.correctness(read, t["expected"]) >= 0.7; tok += tokens(read)
    rows.append([name, len(ch), f"{hit}/{len(tests)}", tok // len(tests)])
table(["Strategy", "Chunks", "Answerable from top-3", "Tokens read / question"], rows)
print("\n  Small chunks find precisely but read too little. Parent-child searches the sentence and hands the model the whole section.")
say("Chunking is not preprocessing. It is the most important modelling decision in a RAG system — so measure it.")
