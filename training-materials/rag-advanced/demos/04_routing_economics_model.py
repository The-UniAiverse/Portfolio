"""Advanced, Hybrid & Agentic RAG · Demo 4 — Smart routing economics: simple / normal / complex tiers (15 min) · Module 5
Shows: a cost model for 10,000 questions a day under three strategies, showing where the saving comes from and how misroutes eat it
Lab: Put your own traffic mix into MIX (from a hand-labelled sample of 100 questions). What is your saving? What misroute rate would wipe it out?
Run: python 04_routing_economics_model.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Advanced, Hybrid & Agentic RAG · Demo 4 — Smart routing economics: simple / normal / complex tiers")
DAY = arg("--per-day", 10000, int); MIX = {"simple": 0.55, "normal": 0.35, "complex": 0.10}; COST = {"simple": cost(900, 120, "cheap"), "normal": cost(5100, 400, "mid"), "complex": cost(42000, 4000, "mid")}
allmid = DAY * COST["normal"] * 30; allag = DAY * COST["complex"] * 30; routed = DAY * 30 * sum(MIX[k] * COST[k] for k in MIX) + DAY * 30 * cost(250, 5, "cheap")
table(["Strategy", "Monthly cost", "vs routed"], [["Everything through the RAG pipeline", money(allmid), f"{allmid / routed:.1f}×"], ["Everything through the agent", money(allag), f"{allag / routed:.1f}×"], ["Routed (incl. router call)", money(routed), "1.0×"]])
print(f"\n  Note: routing is cheaper than 'all agent' by {1 - routed / allag:.0%} — but here it costs MORE than 'all RAG', because 10% of traffic really needs the expensive path. The router buys quality for the 10%, not savings on the 90%.")
hr(); print("What misroutes do (complex questions sent down the cheap path must be re-asked → you pay twice and the user waits):")
for m in (0.0, 0.05, 0.15, 0.30): extra = DAY * 30 * MIX["complex"] * m * COST["normal"]; print(f"  misroute rate {m:>4.0%}  → {money(routed + extra)} / month  · unhappy complex users: {DAY * MIX['complex'] * m:,.0f} a day")
say("Sort your questions before you size your bill. The mix decides the cost; the router only enforces it.")
