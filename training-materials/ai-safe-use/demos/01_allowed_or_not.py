"""Safe & Responsible AI Use at Work · Demo 1 — Allowed or not? Ten scenarios against the policy (15 min) · Module 1
Shows: an AI-use policy written as data, applied to ten real situations with the rule that decided each
Lab: Replace POLICY with your organisation's approved tools and data classes. Which verdicts change? Add two scenarios from your own week.
Run: python 01_allowed_or_not.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Safe & Responsible AI Use at Work · Demo 1 — Allowed or not? Ten scenarios against the policy")
POLICY = {"approved_tools": {"Company Copilot (enterprise)": {"public", "internal", "confidential"}, "Claude Team (company account)": {"public", "internal", "confidential"}, "Free public chatbot": {"public"}},
          "never": {"personal_sensitive", "secret"}, "disclose_when": ["customer-facing content", "decisions about people"], "human_decides": ["hiring", "credit", "discipline", "medical"]}
SCEN = [("Paste a press release into a free chatbot to shorten it", "Free public chatbot", "public", ""), ("Paste a customer complaint with name and phone into a free chatbot", "Free public chatbot", "personal_sensitive", ""),
        ("Summarise an internal strategy deck in Company Copilot", "Company Copilot (enterprise)", "confidential", ""), ("Use a browser plug-in nobody has reviewed to read your email", "Unreviewed plug-in", "confidential", ""),
        ("Draft a customer email with Claude Team and send it as written", "Claude Team (company account)", "internal", "customer-facing content"), ("Ask AI to rank 40 CVs and reject the bottom 30", "Company Copilot (enterprise)", "personal_sensitive", "hiring"),
        ("Paste production API keys to debug a script", "Claude Team (company account)", "secret", ""), ("Generate ideas for the team offsite", "Free public chatbot", "public", ""),
        ("Upload patient notes to get a summary for the doctor", "Company Copilot (enterprise)", "personal_sensitive", "medical"), ("Translate a signed NDA using the enterprise tool", "Company Copilot (enterprise)", "confidential", "")]
rows = []
for what, tool, data, flag in SCEN:
    if tool not in POLICY["approved_tools"]: v, why = "NOT ALLOWED", "tool is not on the approved list (shadow AI)"
    elif data in POLICY["never"]: v, why = "NOT ALLOWED", f"'{data}' data never goes into an AI tool without a specific approved process"
    elif data not in POLICY["approved_tools"][tool]: v, why = "NOT ALLOWED", f"{tool} is approved for {sorted(POLICY['approved_tools'][tool])} only"
    elif flag in POLICY["human_decides"]: v, why = "NOT ALLOWED", f"'{flag}' decisions are made by a person; AI may only assist"
    elif flag in POLICY["disclose_when"]: v, why = "ALLOWED WITH CARE", "review before sending; follow the disclosure rule"
    else: v, why = "ALLOWED", "approved tool, permitted data class"
    rows.append([what[:62], v, why])
table(["Scenario", "Verdict", "Rule that decided it"], rows)
print(f"\n  {sum(r[1]=='ALLOWED' for r in rows)} allowed · {sum('CARE' in r[1] for r in rows)} with care · {sum(r[1]=='NOT ALLOWED' for r in rows)} not allowed")
say("Two questions decide almost everything: is the tool approved, and what class of data is this?")
