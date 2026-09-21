"""Safe & Responsible AI Use at Work · Demo 3 — Is this an incident? Triage and report (12 min) · Module 3
Shows: a triage rule set that turns a description into severity, owner, first actions and a filled incident report
Lab: Each table writes one realistic 'something went wrong with AI' sentence, runs it, and fills the report. Did the severity feel right? Change a rule if not.
Run: python 03_incident_triage.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Safe & Responsible AI Use at Work · Demo 3 — Is this an incident? Triage and report")
import datetime
CASES = ["I pasted a customer list with phone numbers into a free chatbot yesterday", "The website bot told a customer they get a 100% refund, which is not our policy",
         "Our AI summary tool was slow this morning", "An agent with email access sent a draft to the wrong client", "A colleague is using an unapproved AI plug-in to read contracts"]
def triage(t):
    tl = t.lower(); s = 1; tags = []
    if dataq.find_pii(t) or any(w in tl for w in ("customer list", "phone", "personal", "patient", "salary")): s = max(s, 3); tags.append("personal data left our control")
    if any(w in tl for w in ("sent", "wrong client", "transfer", "deleted")): s = max(s, 3); tags.append("AI took an action with external effect")
    if any(w in tl for w in ("told a customer", "not our policy", "wrong answer")): s = max(s, 2); tags.append("wrong information reached a customer")
    if any(w in tl for w in ("unapproved", "plug-in", "shadow")): s = max(s, 2); tags.append("unapproved tool")
    owner = {3: "Security + Data Protection Officer (same day)", 2: "Your manager + AI governance lead (within 2 working days)", 1: "IT service desk (normal ticket)"}[s]
    first = {3: ["Stop using the tool for this data", "Do not delete anything — evidence matters", "Report now; note what, when, which tool, how many people affected"],
             2: ["Correct the customer-facing error", "Capture a screenshot / log", "Report with an example"], 1: ["Log a ticket"]}[s]
    return s, tags or ["service quality only"], owner, first
rows = [[c[:66], f"SEV {triage(c)[0]}", "; ".join(triage(c)[1])] for c in CASES]; table(["What happened", "Severity", "Why"], rows)
hr(); c = CASES[0]; s, tags, owner, first = triage(c)
print("MOCK INCIDENT REPORT\n" + "\n".join([f"  Reported   : {datetime.date(2026, 9, 21).isoformat()} 10:40", f"  What       : {c}", f"  Severity   : SEV {s} — {tags[0]}", f"  Goes to    : {owner}",
      "  First steps: " + " · ".join(first), "  Still needed: which tool · how many records · was chat history/training switched on · has it been deleted at the provider"]))
print("\n  Note: legal notification duties (for example under DPDP or GDPR) are decided by the DPO, not by the reporter. Your job is speed and facts.")
say("Reporting fast is never the mistake. Hiding it for a week is.")
