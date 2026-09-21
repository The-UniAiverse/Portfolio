"""MLOps & LLMOps · Demo 4 — Platform patterns: a model gateway with routing, caching, budgets and cost attribution (25 min) · Module 4
Shows: three teams' traffic through one gateway: difficulty routing, response caching, team budgets enforced, and a cost-attribution report finance can use
Lab: Sketch your gateway: which policies are central (keys, logging, budgets, PII) and which stay with teams (prompts, evals)? What is your chargeback unit?
Run: python 04_gateway_design.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("MLOps & LLMOps · Demo 4 — Platform patterns: a model gateway with routing, caching, budgets and cost attribution")
gw = ops.Gateway({"support": 0.05, "sales": 0.02, "finance": 0.002}); r = rng(3)
TRAFFIC = {"support": ["where is my parcel", "explain the refund rule for late delivery in simple words", "where is my parcel", "opening hours", "where is my parcel", "summarise this complaint email and draft a reply for the customer today"],
           "sales": ["draft an outreach email to a logistics head about address quality", "compare vendor A and vendor B on cost, security and rollout and plan the next steps", "draft an outreach email to a logistics head about address quality"],
           "finance": ["analyse why overtime cost rose in August and plan three actions with owners", "analyse why overtime cost rose in August and plan three actions with owners again with more detail", "extract invoice number and total"]}
for team, qs in TRAFFIC.items():
    for q in qs * 4: gw.call(team, q, out_tokens=r.choice([120, 250, 400]))
table(["Team", "Requests", "Cache hits", "Spend", "Budget", "Blocked"], gw.report()); tiers = {}
for row in gw.rows: tiers[row["tier"]] = tiers.get(row["tier"], 0) + 1
print("\n  Routing mix: " + " · ".join(f"{k} {v}" for k, v in tiers.items())); naive = sum(cost(tokens(q), 250, "flagship") for t, qs in TRAFFIC.items() for q in qs * 4); print(f"  Everything on the flagship model with no cache: ${naive:.4f} vs through the gateway: ${sum(gw.spend.values()):.4f} ({naive / max(sum(gw.spend.values()), 1e-9):.0f}× more)")
print("\n  Finance hit its budget → requests BLOCKED with a clear error, not a surprise invoice. The conversation about raising the budget happens before the spend.")
print("\nCentral in the gateway: keys · logging · PII redaction · budgets · model allow-list · fallbacks.   With the teams: prompts · evals · product decisions.")
say("One door to the models gives you one place to log, one place to cap and one place to switch provider.")
