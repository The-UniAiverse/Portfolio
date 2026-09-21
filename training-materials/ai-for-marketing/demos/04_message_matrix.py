"""AI for Marketing · Demo 4 — Personas from real data → a message matrix (12 min) · Module 4
Shows: personas derived from survey answers (not imagination) and a persona × pain message matrix with the evidence count behind each cell
Lab: Bring 20 real customer quotes (support tickets, reviews, call notes). Tag them. Which persona did you imagine that the data does not support?
Run: python 04_message_matrix.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Marketing · Demo 4 — Personas from real data → a message matrix")
Q = [("ops head", "mis-routes", "We lose a day every time a parcel goes to the wrong hub"), ("ops head", "visibility", "I find out about delays from the customer"), ("finance", "cost", "Overtime is out of control in peak season"), ("finance", "cost", "We cannot predict logistics cost per order"),
     ("ops head", "mis-routes", "Address quality is terrible in tier-3 towns"), ("it", "integration", "Another portal to log into is a non-starter"), ("finance", "visibility", "Claims take weeks to reconcile"), ("ops head", "mis-routes", "Peak season doubles our error rate"), ("it", "security", "Where is our customer data stored?")]
pers = sorted({p for p, *_ in Q}); pains = sorted({x for _, x, _ in Q}); grid = {(p, x): [q for a, b, q in Q if a == p and b == x] for p in pers for x in pains}
table(["Persona \\ pain"] + pains, [[p] + [f"{len(grid[(p, x)])} quote(s)" if grid[(p, x)] else "—" for x in pains] for p in pers]); print("\nMESSAGE MATRIX (only where evidence ≥ 2):")
MSG = {"mis-routes": "Cut mis-routes before they reach the hub", "cost": "Know your logistics cost per order, every day", "visibility": "Hear about delays before your customer does"}
for (p, x), qs in grid.items():
    if len(qs) >= 2: print(f"  {p:<9} × {x:<11} → \"{MSG.get(x, x)}\"   evidence: \"{qs[0]}\"")
print("\n  Cells with one quote are hypotheses to test, not messages to ship. 'IT × security' needs more voices before you write for it.")
say("Ask AI to cluster what customers said. Do not ask it to imagine what they might say.")
