"""AI Governance Practitioner · Demo 2 — Frameworks in depth: a gap assessment across NIST AI RMF, ISO 42001 and the EU AI Act (30 min) · Module 2
Shows: the engine's gap assessment: maturity by NIST function, control coverage per system mapped to ISO 42001 clauses and EU AI Act articles, and a prioritised remediation roadmap
Lab: Run the assessment for your organisation at /tools → Governance with honest gap answers. Pick the five controls that close the most high-risk gaps.
Run: python 02_gap_assessment.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Governance Practitioner · Demo 2 — Frameworks in depth: a gap assessment across NIST AI RMF, ISO 42001 and the EU AI Act")
c = api(); g = c.post("/api/governance/assess", json=c.get("/api/governance/sample").json()).json(); print(f"{g['organisation']} — overall maturity {g['org_gap_overall']}/100\n"); [print(f"  {k:<8}{bar(v, 100, 28)} {v}") for k, v in g["org_gap_scores"].items()]
lib = {x["id"]: x for x in g["control_library"]}; need = {}
for s in g["inventory"]:
    for mc in s["missing_controls"]: need.setdefault(mc["id"] if isinstance(mc, dict) else mc, []).append(s)
top = sorted(need.items(), key=lambda kv: -(sum(3 if s["risk_tier"] == "high" else 1 for s in kv[1])))[:6]; print("\nControls that close the most risk (weighted ×3 for high-risk systems):\n")
table(["Control", "What", "NIST", "ISO 42001", "EU AI Act", "Systems missing it"], [[k, lib[k]["title"][:46], lib[k]["nist"], lib[k]["iso42001"], lib[k]["eu_ai_act"][:22], len(v)] for k, v in top])
print("\nRoadmap from the engine:"); [print(f"  {h:<9}{len(items):>3} action(s)   e.g. {str(items[0])[:95]}") for h, items in g["roadmap"].items() if items]
print(f"\n  Full report: {g['report_pdf_url']} · policy draft: {g['policy_pdf_url']}\n  Obligations differ by ROLE (provider / deployer / importer) and dates phase in — confirm current applicability with counsel before quoting an article to a client.")
say("Three frameworks, one control library. Map once, evidence once, report three ways.")
