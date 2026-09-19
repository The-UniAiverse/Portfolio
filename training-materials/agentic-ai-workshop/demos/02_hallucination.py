"""DEMO 2 — The confident wrong answer, then the same question grounded (Module 2, ~5 min).
Run: python 02_hallucination.py"""
from common import *

banner("Demo 2 · Closed-book vs open-book")
q = "What is Acme Logistics' refund policy for late deliveries?"
print(f"Question: {q}\n")
print("1) CLOSED BOOK — no documents, just the model's 'memory':")
if LIVE:
    print("   " + (llm.complete(f"Answer briefly: {q}", max_tokens=120) or "").replace("\n", "\n   "))
else:
    print("   'Acme Logistics offers a 15% discount on late deliveries and a full refund after 48 hours…'  ← plausible, fluent, INVENTED")
print("\n   ↑ Nothing here is a lie in the model's world. It's autocomplete with nothing to go on.\n")
hr()
print("2) OPEN BOOK — same question, right page on the desk:")
docs = load_docs(); chunks = [c for d in docs for c in chunk_by_heading(d)]
hits = [c for _, c in bm25(q, chunks)[:2]]
text, ti, to = answer(q, hits)
print("   " + text.replace("\n", "\n   "))
print(f"\n   tokens in={ti} out={to}  cost≈${cost(ti, to):.4f}")
print("\nSay it: 'Same model. The only difference is what was on the desk.'")
