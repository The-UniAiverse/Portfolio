"""AI Content Governance & Brand Safety · Demo 2 — Brand risk: deepfake and impersonation response playbook (15 min) · Module 2
Shows: an impersonation incident triaged by reach and harm into a timed response plan with owners, and the monitoring signals that would have caught it earlier
Lab: Run the table-top: it is 09:10 on a Monday and this video is spreading. Who does what in the first 60 minutes? Who has the platform escalation contact?
Run: python 02_impersonation_response.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Content Governance & Brand Safety · Demo 2 — Brand risk: deepfake and impersonation response playbook")
INC = {"what": "Video of 'our CEO' announcing a refund scheme with a payment link", "channel": "WhatsApp forwards + a fake Instagram page", "reach_estimate": 40000, "asks_for_money": True, "uses_real_person": True, "customers_affected_so_far": 12}
sev = 3 if INC["asks_for_money"] and INC["reach_estimate"] > 10000 else 2 if INC["uses_real_person"] else 1; print(f"INCIDENT: {INC['what']}\n  via {INC['channel']} · reach ~{INC['reach_estimate']:,} · {INC['customers_affected_so_far']} customers already paid\n  SEVERITY {sev}/3\n")
PLAN = [("0–15 min", "Comms lead", "Confirm it is fake with the CEO's office; open the incident log; preserve copies and URLs"), ("15–30 min", "Legal + Security", "Platform takedown requests (impersonation + fraud); report the payment link to the bank/PSP"),
        ("30–60 min", "Comms lead", "Holding statement on owned channels: 'This is fake. We never ask for payment by link.' Pin it."), ("1–4 h", "Customer service", "Script for agents; contact the 12 affected customers; log losses"), ("same day", "DPO / Legal", "Assess reporting duties to authorities; police cyber-crime report"), ("week 1", "Brand", "Post-incident review; update monitoring keywords; brief employees")]
table(["When", "Owner", "Action"], [list(p) for p in PLAN]); hr()
SIG = [("New social handles containing the brand name", True), ("Spike in 'refund' + brand mentions", True), ("Customer-service contacts quoting an offer that does not exist", True), ("Payment links on look-alike domains", False)]
print("Monitoring signals — were they switched on?"); [print(f"  [{'x' if on else ' '}] {s}") for s, on in SIG]; print("\n  Prepare BEFORE the incident: platform escalation contacts · pre-approved holding statement · who may speak · where evidence is stored")
say("You cannot stop someone cloning your CEO. You can decide today who does what in the first hour.")
