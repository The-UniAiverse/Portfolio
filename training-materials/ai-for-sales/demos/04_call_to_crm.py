"""AI for Sales · Demo 4 — Calls to CRM: notes → fields → follow-up (12 min) · Module 4
Shows: a call transcript turned into CRM fields by schema (unknown stays empty), next steps with owners, and a follow-up email
Lab: Use the transcript of a real call (names changed). Which CRM fields stayed empty? Those are your questions for the next call.
Run: python 04_call_to_crm.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Sales · Demo 4 — Calls to CRM: notes → fields → follow-up")
T = """Rep: Thanks Anita. So the three new warehouses go live in November?
Anita: Yes, Pune first on 4 November. Budget is around 40 lakh for the first year but finance has not signed it off.
Rep: Who else is involved in the decision?
Anita: Our CFO, Mr. Desai, and IT security will want a review.
Anita: Our main worry is mis-routes during the first month. Currently we see about 6% mis-routes.
Rep: I'll send the Kaveri case study by Wednesday.
Anita: Rep, can you share a draft implementation plan by next Friday?"""
SPEC = {"Go-live date": r"(\d{1,2} \w+)", "Budget": r"[Bb]udget is around ([\d\s\w]+?) for", "Budget approved?": r"finance has (not signed|signed)", "Decision makers": r"Our (CFO, [\w.\s]+?),", "Other stakeholders": r"and (IT security)", "Main pain": r"main worry is ([^.]+)\.", "Current metric": r"about (\d+% mis-routes)", "Competitors mentioned": r"(?:competitor|also talking to) ([\w\s]+)"}
f = text.extract_fields(T, SPEC); table(["CRM field", "Value"], [[k, v if v else "— (not said; ask next call)"] for k, v in f.items()]); acts = text.extract_actions(T); print(); table(["Owner", "Next step", "Due"], [[a["owner"], a["action"], a["due"]] for a in acts])
hr(); print(f"Subject: Next steps after today's call\n\nAnita, thank you for today. You are targeting {f['Go-live date']} for Pune, and your main concern is {f['Main pain']}.\nI will send the Kaveri case study by Wednesday and a draft implementation plan by next Friday.\nOne question: who should I include from IT security?\n")
print("  Guardrail: call recordings and customer names stay in the approved company tool — never a personal account.")
say("Five minutes after the call, the CRM is right and the follow-up is sent. That is the whole win.")
