"""AI for Sales · Demo 5 — Proposals and objections: skeleton from past wins + objection bank (12 min) · Module 5
Shows: a proposal skeleton assembled from a past win, and an objection bank searched by meaning so the rep gets the proven answer, not an improvised one
Lab: Add your three most common objections and your best answers to data/objections.md. Test them with the wording customers really use.
Run: python 05_proposal_and_objections.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Sales · Demo 5 — Proposals and objections: skeleton from past wins + objection bank")
docs = [{"id": "obj", "title": "Objection bank", "text": data_path(__file__, "objections.md").read_text()}]; chunks = chunk_by_heading(docs[0])
for q in ["you are more expensive than the other vendor", "we already have a system for this", "our security team will never approve it", "can you guarantee 100% accuracy?"]:
    top = rerank(q, [c for _, c in rrf(bm25(q, chunks), semantic(q, chunks))[:5]], 1); print(f"\nCustomer: \"{q}\"\n  → {top[0]['heading']}\n    {top[0]['text'].splitlines()[-1][:200]}" if top else f"\n{q}\n  → no proven answer — escalate, then ADD it to the bank")
hr(); print("PROPOSAL SKELETON (from the Kaveri win):\n  1. Your situation — in the customer's own words from the call notes\n  2. Outcome and metric — mis-routes 6% → under 3% in 90 days\n  3. Approach in three phases with a stop point after each\n  4. Proof — Kaveri: −18% mis-routes (approved case study)\n  5. Investment — PRICING IS ENTERED BY A HUMAN, never generated\n  6. Risks and what we need from you\n  7. Next step and date")
say("AI drafts the structure. Humans own the price and the promise.")
