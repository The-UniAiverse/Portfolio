"""Build Your Own AI Bot (RAG for non-technical people) · Demo 1 — Day 1 — a bot that answers from one document (and admits when it can't) (15 min) · Module 1
Shows: closed-book guess vs grounded answer with a citation vs honest refusal, on one policy document
Lab: Pick ONE document from your own work. Ask five questions it answers and two it does not. Tick: answered correctly / cited / refused correctly.
Run: python 01_bot_from_one_document.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Build Your Own AI Bot (RAG for non-technical people) · Demo 1 — Day 1 — a bot that answers from one document (and admits when it can't)")
doc = load_docs()[1]; chunks = chunk_by_heading(doc); print(f"Document: {doc['title']} · {len(doc['text'])} characters · {len(chunks)} sections\n")
for q in ["How long do I have to claim for a damaged parcel?", "What is the refund for a late delivery?", "What is the CEO's phone number?"]:
    top = [c for _, c in bm25(q, chunks)[:3]]; a, i, o = grounded(q, top); print(f"Q: {q}\nA: {a}\n   ({i} tokens in · {o} out · ${cost(i, o):.5f})\n")
print("Choosing documents for a first bot:  ✓ current  ✓ one owner  ✓ has headings  ✓ answers real questions   ✗ drafts  ✗ duplicates  ✗ scanned images without text")
say("A good bot has two skills: finding the page, and saying 'it is not in here'. Test both from day one.")
