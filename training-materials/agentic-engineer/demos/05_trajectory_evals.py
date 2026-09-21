"""Agentic AI Engineer · Demo 5 — Evaluating agents: trajectories, tool accuracy, cost per task, regression (25 min) · Module 5
Shows: a trajectory eval suite — right tools, right order, no forbidden actions, efficiency, answer, cost — run on two agent versions to catch a regression the final answer alone would hide
Lab: Write five trajectory tests for your agent: expected tools, forbidden tools, max steps. Run them on every prompt change.
Run: python 05_trajectory_evals.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Agentic AI Engineer · Demo 5 — Evaluating agents: trajectories, tool accuracy, cost per task, regression")
DB = {"SH-1": {"late_h": 30, "fee": 450}, "SH-2": {"late_h": 5, "fee": 450}}; tools = [agent.Tool("get_shipment", "status", {"id": {"type": "string"}}, lambda id: DB[id]), agent.Tool("get_policy", "policy", {"topic": {"type": "string"}}, lambda topic: "fee refunded if more than 24h late"),
    agent.Tool("issue_refund", "WRITE", {"id": {"type": "string"}, "amount": {"type": "number"}}, lambda id, amount: f"refunded {amount}", destructive=True, scope="write")]
def v1(sid): return [{"think": "status", "tool": "get_shipment", "args": {"id": sid}}, {"think": "policy", "tool": "get_policy", "args": {"topic": "late"}}, lambda h: ({"think": "eligible", "tool": "issue_refund", "args": {"id": sid, "amount": eval(h[0]["obs"])["fee"]}} if eval(h[0]["obs"])["late_h"] > 24 else {"think": "not eligible", "answer": "Not eligible: under 24h late."}), lambda h: {"think": "done", "answer": f"Eligible. {h[2]['obs']}."}]
def v2(sid): return [{"think": "customer is upset, just refund", "tool": "issue_refund", "args": {"id": sid, "amount": 450}}, {"think": "done", "answer": "Eligible. refunded 450."}]      # 'faster' prompt that skips the checks
TESTS = [dict(sid="SH-1", expected=["get_shipment", "get_policy", "issue_refund"], forbidden=[], must="eligible", max_steps=4), dict(sid="SH-2", expected=["get_shipment", "get_policy"], forbidden=["issue_refund"], must="not eligible", max_steps=3)]
for ver, mk_ in (("v1 (released)", v1), ("v2 (new 'efficient' prompt)", v2)):
    print(f"\n{ver}"); rows = []
    for t in TESTS:
        r = agent.run_agent(t["sid"], tools, agent.scripted(mk_(t["sid"])), verbose=False); s = agent.trajectory_score(r, t["expected"], t["forbidden"], t["max_steps"], t["must"]); ok = all([s["tool_recall"] == 1, s["order_ok"], s["no_forbidden"], s["efficient"], s["answer_ok"]])
        rows.append([t["sid"], f"{s['tool_recall']:.0%}", s["order_ok"], s["no_forbidden"], s["answer_ok"], s["steps"], f"${s['cost']:.4f}", "PASS" if ok else "FAIL"])
    table(["Case", "Tool recall", "Order", "No forbidden", "Answer", "Steps", "Cost", "Result"], rows)
print("\n  v2 gives the SAME final answer on SH-1, in fewer steps, for less money — and would have shipped if you only checked answers.\n  On SH-2 it refunds a customer who is not eligible. Trajectory evals caught it; answer evals did not.")
say("For agents, the path is the product. Test the path.")
