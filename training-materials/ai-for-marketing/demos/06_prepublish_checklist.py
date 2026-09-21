"""AI for Marketing · Demo 6 — Guardrails: the pre-publish check and team SOP (12 min) · Module 6
Shows: an automated pre-publish check — unsupported claims, regulated words, personal data, image rights, disclosure — that gives legal a reason to review faster
Lab: Agree your own regulated-words list with legal. Run last month's three most important pieces through the check.
Run: python 06_prepublish_checklist.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Marketing · Demo 6 — Guardrails: the pre-publish check and team SOP")
FACTS = {"kaveri": "Kaveri Pharma cut mis-routes by 18% within 90 days in 2025", "reach": "ships to 2,300 pharmacies"}; REG = ["cure", "guaranteed", "risk-free", "clinically proven", "no side effects", "best in india"]
POST = {"text": "Guaranteed results! Kaveri cut mis-routes by 18% and saved 45% on overtime. Clinically proven address AI. Contact priya@acme.in.", "image": {"source": "AI-generated", "licence": None, "shows_real_person": False}, "ai_assisted": True, "disclosure_line": ""}
cl = text.check_claims(POST["text"], FACTS); reg = [w for w in REG if w in POST["text"].lower()]; pii = dataq.find_pii(POST["text"])
C = [("Every number traces to an approved fact", all(c["status"] == "supported" for c in cl if "%" in c["claim"]), "; ".join(f"{c['claim'][:40]} → {c['status']}" for c in cl)), ("No regulated / absolute words", not reg, ", ".join(reg)), ("No personal contact data", not pii, str(pii)),
     ("Image has a source and licence (or is marked AI-generated)", POST["image"]["source"] == "AI-generated" or bool(POST["image"]["licence"]), ""), ("AI-assistance disclosed where policy requires", (not POST["ai_assisted"]) or bool(POST["disclosure_line"]), "add the disclosure line from the SOP")]
print(POST["text"] + "\n"); [print(f"  [{'x' if ok else ' '}] {n}" + ("" if ok else f"\n        ← {why}")) for n, ok, why in C]; print(f"\n  {sum(ok for _, ok, _ in C)}/{len(C)} passed → {'PUBLISH' if all(ok for _, ok, _ in C) else 'BACK TO AUTHOR'}")
print("\nTEAM SOP: brief → AI draft with voice kit → author verifies facts → automated check (this script) → human approver → publish → log prompt + sources")
say("'45% on overtime' was never in the case study. The model rounded a quarter up to a headline. That is why a human signs.")
