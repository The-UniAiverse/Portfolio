"""AI Use-Case Design & Product Ownership · Demo 1 — From pain point to AI task — or not AI at all (15 min) · Module 1
Shows: three pain points framed as a task type, with the non-AI alternative tested first and a verdict
Lab: Frame three real problems from your team in the PAINS format. At least one should come out as 'not an AI problem' — if none does, you are not being honest.
Run: python 01_frame_the_problem.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Use-Case Design & Product Ownership · Demo 1 — From pain point to AI task — or not AI at all")
PAINS = [{"pain": "Agents spend 11 minutes answering each 'where is my shipment' email", "volume": "900/week", "answer_lives_in": "TMS + policy documents", "rule_based_possible": False, "errors_cost": "low, reversible"},
         {"pain": "Finance re-types supplier invoices into the ERP", "volume": "2,400/month", "answer_lives_in": "the invoice itself", "rule_based_possible": False, "errors_cost": "medium, caught at reconciliation"},
         {"pain": "Managers forget to approve leave requests", "volume": "60/month", "answer_lives_in": "nowhere — it is a reminder problem", "rule_based_possible": True, "errors_cost": "low"},
         {"pain": "We want AI to decide which drivers to dismiss", "volume": "10/quarter", "answer_lives_in": "HR judgement", "rule_based_possible": False, "errors_cost": "high, affects livelihoods"}]
def frame(p):
    if p["rule_based_possible"]: return "NOT AI", "a reminder/workflow rule solves it for a fraction of the cost", "—"
    if "high" in p["errors_cost"]: return "AI ASSIST ONLY", "decision about a person: AI may summarise evidence, a human decides and signs", "summarisation + human decision"
    a = p["answer_lives_in"].lower()
    if "document" in a or "tms" in a: return "AI — grounded Q&A (RAG + live lookup)", "answer exists in systems/documents; language is the bottleneck", "retrieval + generation"
    if "itself" in a: return "AI — structured extraction", "fields are on the page; schema + validation + human check on low confidence", "extraction"
    return "DISCOVER MORE", "unclear where the answer lives", "—"
table(["Pain point", "Volume", "Verdict", "AI task type"], [[p["pain"][:52], p["volume"], frame(p)[0], frame(p)[2]] for p in PAINS]); print()
for p in PAINS: print(f"  • {p['pain'][:50]:<50} → {frame(p)[1]}")
print("\nProblem statement template:  For [who], [task] takes [time/cost] because [cause]. If solved, [metric] moves from [baseline] to [target]. The answer lives in [where].")
say("Where does the answer live? If you cannot say, you do not have a use case yet.")
