"""Advanced, Hybrid & Agentic RAG · Demo 3 — Agentic retrieval: grade, rewrite, retry — with caps (25 min) · Module 4
Shows: a corrective retrieval loop (CRAG-style): grade the evidence, rewrite the query if weak, retry within a step and cost budget, and refuse rather than answer from weak evidence
Lab: Set max_steps to 1, then 3, then 6 on your own hard questions. Plot accuracy against cost. Where does the curve flatten?
Run: python 03_agentic_retrieval_loop.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Advanced, Hybrid & Agentic RAG · Demo 3 — Agentic retrieval: grade, rewrite, retry — with caps")
ch = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]
def grade(q, top):
    from common import _terms as T; qt = set(T(q)); best = max((len(qt & set(T(c["text"]))) / (len(qt) or 1) for c in top), default=0); return best
def expand(q):
    ql = q.lower().replace("?", "")
    for k, v in SYNONYMS.items(): ql = ql.replace(k, v)
    return ql
REWRITES = [lambda q: q, expand, lambda q: " ".join(w for w in expand(q).split() if len(w) > 3)]     # 1 as asked · 2 vocabulary of the documents · 3 keywords only
def loop(q, max_steps=3, max_cost=0.02):
    spent = 0.0
    for i in range(max_steps):
        q2 = REWRITES[min(i, 2)](q); top = [c for _, c in bm25(q2, ch)[:3]]; g = grade(q2, top); spent += cost(tokens(" ".join(c["text"] for c in top)) + 200, 60); print(f"    step {i + 1}: search '{q2[:50]}' → evidence grade {g:.2f} {'✓ good enough' if g >= 0.5 else '✗ weak → rewrite'}")
        if g >= 0.5: a = grounded(q, top)[0]; return a, i + 1, spent
        if spent >= max_cost: print("    cost cap reached"); break
    return "I could not find this in the available documents.", max_steps, spent
for q in ["How late must a delivery be for a shipping fee refund?", "How do I get my money back if my parcel arrived broken?", "How much holiday do temps get?", "What is the CEO's salary?"]:
    print(f"\nQ: {q}"); a, n, c_ = loop(q); print(f"  → {a[:130]}\n    {n} step(s) · ${c_:.4f}")
print("\n  Single-shot keyword search fails questions 2 and 3. The loop rescues question 3 and still refuses question 4 — for about 2–3× the cost.\n  Now read question 2 again: the loop stopped at the first 'good enough' evidence — the LATE-delivery rule, not the DAMAGE rule. Grading the evidence is not grading the answer: add an answer check (does it mention damage?) before you trust the loop.")
say("An agentic loop is a retry policy with judgement. Give it a budget and a way to say no, or it will search forever.")
