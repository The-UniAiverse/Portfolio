"""GenAI Engineer · Demo 7 — Agents and routing: simple / RAG / agent — and when not to go agentic (25 min) · Module 7
Shows: a three-way router with a registry of tools, budgets and termination, and the cost/latency of sending everything to the agent
Lab: Classify 20 real questions from your logs into simple / RAG / agent by hand. What share truly needs an agent? Build the router for the majority first.
Run: python 07_router_simple_rag_agent.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("GenAI Engineer · Demo 7 — Agents and routing: simple / RAG / agent — and when not to go agentic")
ch = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]; ORDERS = {"SH-1042": {"status": "delayed 26h at Pune hub", "value": 8200, "fee": 450}}
def route(q):
    ql = q.lower()
    if any(w in ql for w in ("hello", "thanks", "opening hours")): return "simple"
    if __import__("re").search(r"sh-\d+", ql) and any(w in ql for w in ("refund", "eligible", "raise", "claim")): return "agent"
    return "rag"
tools = [agent.Tool("get_shipment", "Live shipment status", {"id": {"type": "string"}}, lambda id: ORDERS.get(id, "unknown id")), agent.Tool("search_policy", "Search policy documents", {"query": {"type": "string"}}, lambda query: answer(query, rerank(query, [c for _, c in rrf(bm25(query, ch), semantic(query, ch))[:8]], 2))[0]),
         agent.Tool("create_refund_request", "WRITE: open a refund request", {"id": {"type": "string"}, "amount": {"type": "number"}}, lambda id, amount: f"refund request RR-881 opened for {id}: INR {amount}", destructive=True, scope="write")]
QS = ["Thanks, what are your opening hours?", "How late must a delivery be for a fee refund?", "Shipment SH-1042 is late — am I eligible for a refund, and can you raise it?", "What does ERR_SVC_4471 mean?"]; tot = {"routed": 0.0, "all-agent": 0.0}
for q in QS:
    r = route(q); print(f"\nQ: {q}\n  ROUTE → {r}")
    if r == "simple": c_ = cost(300, 40, "cheap"); print("  canned/cheap-model reply")
    elif r == "rag": a, i, o = answer(q, rerank(q, [c for _, c in rrf(bm25(q, ch), semantic(q, ch))[:8]], 3)); c_ = cost(i, o); print(f"  {a[:120]}")
    else:
        pol = agent.scripted([{"think": "Need the live status first.", "tool": "get_shipment", "args": {"id": "SH-1042"}}, {"think": "Check the rule for late deliveries.", "tool": "search_policy", "args": {"query": "late delivery shipping fee refund"}},
               lambda h: {"think": "26h > 24h → eligible for the shipping fee only.", "tool": "create_refund_request", "args": {"id": "SH-1042", "amount": eval(h[0]["obs"])["fee"]}}, lambda h: {"think": "Done.", "answer": f"Eligible (delayed 26h > 24h). {h[2]['obs']}."}])
        run = agent.run_agent(q, tools, pol, caps=agent.Caps(max_steps=5, max_cost=0.05)); c_ = run.cost; print(f"  ANSWER {run.answer}")
    tot["routed"] += c_; tot["all-agent"] += cost(9000, 900)
print(f"\nCost for these four: routed ${tot['routed']:.4f} vs everything-through-the-agent ${tot['all-agent']:.4f} ({tot['all-agent'] / tot['routed']:.1f}×) — and the agent path is 5–10× slower.")
say("An agent is the most expensive way to answer a question. Route first; go agentic only when the task needs actions or several hops.")
