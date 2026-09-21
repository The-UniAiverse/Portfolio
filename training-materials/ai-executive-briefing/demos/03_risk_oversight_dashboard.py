"""AI Executive & Board Briefing · Demo 3 — Risk and oversight: the one-page board view (10 min) · Module 3
Shows: the AI inventory classified by risk tier with control coverage, from the real governance engine — the page a board should see each quarter
Lab: Facilitator pre-loads the client's AI inventory via /tools → Governance. Directors mark which system they would ask about first.
Run: python 03_risk_oversight_dashboard.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Executive & Board Briefing · Demo 3 — Risk and oversight: the one-page board view")
c = api(); g = c.post("/api/governance/assess", json=c.get("/api/governance/sample").json()).json(); print(g["narrative"][:300] + "\n")
table(["AI system", "Status", "Risk tier", "Controls in place"], [[s["name"][:34], s["status"], s["risk_tier"].upper(), f"{s['control_coverage_pct']}%"] for s in g["inventory"]])
print("\n  Organisation maturity (NIST AI RMF functions):"); [print(f"    {k:<8} {bar(v, 100, 20)} {v}") for k, v in g["org_gap_scores"].items()]
hi = [s for s in g["inventory"] if s["risk_tier"] == "high"]; print(f"\n  Board attention: {len(hi)} high-risk system(s) with average control coverage {sum(s['control_coverage_pct'] for s in hi) / max(1, len(hi)):.0f}%.")
print("  Five board questions: inventory complete? · who signs off high-risk? · incidents this quarter? · third-party model exposure? · when were we last tested?")
print("  (Framework-aligned guidance, not legal advice.)")
say("You do not need to understand the model. You need to know which systems could hurt someone, and who signed for them.")
