"""GenAI Engineer · Demo 5 — Query understanding and grounded generation: rewrite, filter, cite, refuse, verify (25 min) · Module 5
Shows: a multi-turn conversation where follow-ups are rewritten into standalone queries, metadata filters are extracted, answers carry citations, out-of-scope is refused and a verifier checks faithfulness
Lab: Run a five-turn conversation against your own bot. Log the rewritten query each turn. Where did the rewrite lose or invent something?
Run: python 05_query_and_grounded_generation.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("GenAI Engineer · Demo 5 — Query understanding and grounded generation: rewrite, filter, cite, refuse, verify")
ch = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]; TURNS = ["How much annual leave do permanent employees get?", "and contractors?", "does it carry over?", "what about refunds for late deliveries", "what is the CEO's salary?"]
def rewrite(q, hist):
    """Follow-ups are useless to a search engine. Carry the topic forward explicitly."""
    ql = q.lower(); topic = next((t for t in ("leave", "refund", "claim", "password") for h in reversed(hist) if t in h.lower()), "")
    if ql.startswith(("and ", "what about", "does it", "is it", "how about")) and topic and not any(w in ql for w in ("leave", "refund", "claim", "password", "deliver")): q = f"{q.rstrip('?')} — {topic}" + (" for contractors" if "contractor" in " ".join(hist[-2:]).lower() and "contractor" not in ql else "") + "?"
    return q
def filters(q): return {"doc": "leave" if "leave" in q.lower() else "refund" if any(w in q.lower() for w in ("refund", "claim", "deliver")) else None}
hist = []
for t in TURNS:
    q = rewrite(t, hist); f = filters(q); pool = [c for c in ch if not f["doc"] or f["doc"] in c["doc"].lower()] or ch; top = rerank(q, [c for _, c in rrf(bm25(q, pool), semantic(q, pool))[:8]], 3); a, i, o = grounded(q, top)
    fa = evals.faithfulness(a, [c["text"] for c in top]); print(f"\nUSER   {t}\n  query  {q}   filter={f['doc'] or 'none'} ({len(pool)} chunks)\n  ANSWER {a[:150]}\n  verify faithfulness {fa:.0%} · {'REFUSED correctly' if 'could not find' in a.lower() else 'cited' if 'Source:' in a else 'NO CITATION → block'}"); hist += [t, a]
say("Rewrite the question, filter before you search, cite when you answer, refuse when you cannot, and verify before you show it.")
