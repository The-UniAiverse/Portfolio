"""DEMO 6 — Smart routing: why you don't put every question in the expensive vehicle (Module 7-8, ~10 min).
Run: python 06_routing_economics.py [--per-day 10000]"""
import sys; from common import *

banner("Demo 6 · Routing economics")
per_day = int(sys.argv[sys.argv.index("--per-day") + 1]) if "--per-day" in sys.argv else 10000
mix = {"simple": 0.45, "normal": 0.40, "complex": 0.15}   # typical support mix — replace with the client's logs
per_q = {"simple": cost(900, 150, "cheap"), "normal": cost(5100, 400, "mid"), "complex": cost(5100 * 6, 4000, "mid")}
print(f"{per_day:,} questions/day · mix {mix}\n")
def monthly(policy): return sum(per_day * 30 * share * per_q[policy(kind)] for kind, share in mix.items())
scen = {"Everything simple (cheap model, no retrieval)": lambda k: "simple", "Everything agentic": lambda k: "complex", "Routed by type": lambda k: k}
base = monthly(scen["Everything agentic"])
for name, pol in scen.items():
    m = monthly(pol); print(f"  {name:<48} ${m:>10,.0f}/month   ({100 * (base - m) / base:>4.0f}% cheaper than all-agentic)")
hr()
print("Then the three cheapest wins on top of routing:")
for label, factor in [("Prompt caching on the static prefix", 0.35), ("Trim history after ~10 messages", 0.15), ("Output limit: 'answer in 3 sentences'", 0.08)]:
    print(f"  {label:<44} ≈ −{factor * 100:.0f}% of input/output spend")
print("\nSay it: 'Sort your questions first. Then cache, trim, cap. The model is the last lever.'")
