"""Agentic AI Engineer · Demo 1 — Agent architecture: one agent, three tools, explicit state (25 min) · Module 1
Shows: a ReAct-style loop with typed tools, explicit state and a termination rule, versus plan-and-execute on the same task — with steps and cost compared
Lab: Implement the same task in your framework of choice. Print every THINK/ACT/OBS. How many steps did it take? What is your termination condition?
Run: python 01_single_agent_three_tools.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Agentic AI Engineer · Demo 1 — Agent architecture: one agent, three tools, explicit state")
INV = {"INV-2291": {"po": "PO-771", "amount": 48250, "vendor": "Shree Packaging"}}; PO = {"PO-771": {"amount": 48000, "status": "approved", "tolerance_pct": 1.0}}; NOTES = []
tools = [agent.Tool("get_invoice", "Fetch an invoice", {"id": {"type": "string"}}, lambda id: INV.get(id, "not found")), agent.Tool("get_po", "Fetch a purchase order", {"id": {"type": "string"}}, lambda id: PO.get(id, "not found")),
         agent.Tool("add_note", "WRITE: add a note to the invoice", {"id": {"type": "string"}, "note": {"type": "string"}}, lambda id, note: NOTES.append(note) or "note saved", destructive=True, scope="write")]
react = agent.scripted([{"think": "I need the invoice first.", "tool": "get_invoice", "args": {"id": "INV-2291"}}, lambda h: {"think": "It references a PO — fetch it.", "tool": "get_po", "args": {"id": eval(h[0]["obs"])["po"]}},
    lambda h: (lambda inv, po: {"think": f"Difference {abs(inv['amount'] - po['amount']) / po['amount']:.2%} vs tolerance {po['tolerance_pct']}% → within tolerance, record it.", "tool": "add_note", "args": {"id": "INV-2291", "note": f"3-way match OK: diff {inv['amount'] - po['amount']} within {po['tolerance_pct']}%"}})(eval(h[0]["obs"]), eval(h[1]["obs"])),
    lambda h: {"think": "Goal met — stop.", "answer": "INV-2291 matches PO-771 within tolerance; note recorded; ready for payment approval by a human."}])
print("ReAct (decide one step at a time):"); r1 = agent.run_agent("Check invoice INV-2291 against its PO and record the result", tools, react)
hr(); print("Plan-and-execute (plan once, then run; cheaper, but blind to surprises):\n  PLAN  1) get_invoice 2) get_po 3) compare 4) add_note"); c2 = cost(900, 150) + 3 * cost(300, 40, "cheap"); print(f"  cost ≈ ${c2:.4f} vs ReAct ${r1.cost:.4f}.  But if the PO is 'not found', the plan has no step for that — ReAct would notice and ask.")
print("\nState kept outside the prompt: {invoice, po, diff_pct, decision}. The model proposes; your code holds the facts.")
say("Start with one agent and three tools. Every tool you add is tokens on every call and one more way to go wrong.")
