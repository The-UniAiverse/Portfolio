"""AI Governance for Leaders · Demo 1 — Map your systems to risk tiers (15 min) · Module 2
Shows: six AI systems described in plain words and classified by the real governance engine, with the single attribute that drove each tier
Lab: List every AI system your function uses (include the ones IT does not know about). Classify each with /tools → Governance. Which surprised you?
Run: python 01_map_systems_to_tiers.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Governance for Leaders · Demo 1 — Map your systems to risk tiers")
c = api(); SYS = [dict(name="CV screening assistant", purpose="rank applicants", affects_individuals_rights=True, processes_personal_data=True), dict(name="Website chatbot", purpose="answer customers", interacts_with_public=True),
       dict(name="Marketing copy generator", purpose="draft posts", generates_content=True), dict(name="Internal document search", purpose="find policies"), dict(name="Driver fatigue camera", purpose="detect drowsiness", uses_biometrics_or_surveillance=True, safety_critical=True, processes_personal_data=True),
       dict(name="Customer 'trust score' to restrict service", purpose="score people", manipulative_or_social_scoring=True, processes_personal_data=True)]
rows = []
for s in SYS:
    r = c.post("/api/governance/classify", json=s).json(); why = next((k.replace("_", " ") for k, v in s.items() if v is True), "no risk attribute set"); rows.append([s["name"], r["label"], why, len(r["required_controls"])])
table(["System", "Tier", "Driven by", "Controls required"], rows)
print("\n  Same technology, four tiers. The tier follows the USE, not the model.  (Framework-aligned guidance, not legal advice.)")
say("Nobody regulates 'AI'. They regulate what you do to people with it.")
