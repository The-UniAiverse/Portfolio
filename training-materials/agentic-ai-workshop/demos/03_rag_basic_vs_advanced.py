"""DEMO 3 — Build the library, then climb the RAG ladder one change at a time (Module 4 / Lab 2, ~20 min).
Shows: fixed vs heading chunks · contextual prefix · keyword vs meaning vs hybrid (RRF) · reranking · scores on the test sheet.
Run: python 03_rag_basic_vs_advanced.py"""
import csv; from common import *

banner("Demo 3 · Basic → Advanced RAG, one change at a time")
docs = load_docs(); tests = list(csv.DictReader(open(Path(__file__).with_name("test_sheet.csv"))))

def retrieve(q, chunks, mode, use_rerank):
    if mode == "keyword": ranked = bm25(q, chunks)
    elif mode == "meaning": ranked = semantic(q, chunks)
    else: ranked = rrf(bm25(q, chunks), semantic(q, chunks))
    cands = [c for _, c in ranked[:8]]
    return rerank(q, cands, 3) if use_rerank else cands[:3]

def score(chunks, mode, use_rerank):
    """A question 'passes' when a chunk containing the expected wording is in the top-3 (retrieval), and the answer isn't a refusal unless it should be."""
    hits = 0; detail = []
    for t in tests:
        top = retrieve(t["question"], chunks, mode, use_rerank)
        key = t["expected"].split(";")[0].lower()[:13]
        found = any(key in c["text"].lower() for c in top)
        if t["type"] == "out_of_scope":
            ans, *_ = answer(t["question"], top); found = "could not find" in ans.lower()
        hits += found; detail.append((t["question"][:48], "✓" if found else "✗"))
    return hits, detail

configs = [("Fixed 400-char chunks · keyword search", [c for d in docs for c in chunk_fixed(d)], "keyword", False),
           ("Heading chunks (no prefix) · keyword", [c for d in docs for c in chunk_by_heading(d, contextual=False)], "keyword", False),
           ("+ contextual prefix · keyword", [c for d in docs for c in chunk_by_heading(d)], "keyword", False),
           ("+ meaning search only", [c for d in docs for c in chunk_by_heading(d)], "meaning", False),
           ("+ HYBRID (keyword + meaning, RRF)", [c for d in docs for c in chunk_by_heading(d)], "hybrid", False),
           ("+ reranking (fetch 8, keep 3)", [c for d in docs for c in chunk_by_heading(d)], "hybrid", True)]
print(f"{len(tests)} test questions. Score = questions whose right chunk reached the desk (or correctly refused).\n")
for name, chunks, mode, rr in configs:
    s, detail = score(chunks, mode, rr)
    print(f"  {s:>2}/{len(tests)}  {name}")
hr()
print("Look at one chunk with and without the prefix:\n")
c0 = chunk_by_heading(docs[0], contextual=False)[1]["text"][:110]; c1 = chunk_by_heading(docs[0])[1]["text"][:140]
print(f"  without: {c0!r}…\n  with:    {c1!r}…")
hr()
print("The exact-match blind spot (why hybrid matters):")
chunks = [c for d in docs for c in chunk_by_heading(d)]
for q in ["What does ERR_SVC_4471 mean?", "how do I get my money back for a broken parcel"]:
    print(f"\n  Q: {q}")
    for mode in ["keyword", "meaning", "hybrid"]:
        top = retrieve(q, chunks, mode, False)[0]; print(f"    {mode:<8} → {top['doc'][:28]} › {top['heading']}")
print("\nSay it: 'One change at a time. If you change three things and it improves, you learned nothing.'")
