"""AI for All · Demo 5 — Automate one weekly task — with a check step (12 min) · Module 6
Shows: a saved prompt with variables, run on this week's notes, plus the verification step that makes it safe to reuse
Lab: Write your own saved prompt for one weekly task using the four parts (role, input, format, check). Swap with a neighbour and run theirs.
Run: python 05_weekly_automation.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for All · Demo 5 — Automate one weekly task — with a check step")
SAVED_PROMPT = {"name": "Weekly status from notes", "role": "You are my chief of staff.", "input": "{notes}", "format": "Three headings: Done / Next / Risks. Bullets under 12 words. Keep every number and date exactly.",
                "check": "List any number or date in your answer that is NOT in my notes."}
NOTES = """Mon: closed 14 tickets, 3 escalated to vendor. Tue: demo to Zenith moved to 3 Oct. Wed: budget approved INR 4.5 lakh for the pilot.
Thu review call. Anil: I'll send the revised SOW by Monday. Raj: Meena, can you confirm the training room by Friday? Fri: risk — vendor API still failing 1 in 20 calls."""
print("SAVED PROMPT (reusable every week):"); [print(f"  {k:<7}{v}") for k, v in SAVED_PROMPT.items()]; hr()
if LIVE: out = llm.complete(f"{SAVED_PROMPT['role']}\n{SAVED_PROMPT['format']}\n{SAVED_PROMPT['check']}\n\nNOTES:\n{NOTES}", max_tokens=300) or ""
else:
    acts = text.extract_actions(NOTES.replace(". ", ".\n").replace("? ", "?\n"))
    out = ("DONE\n• Closed 14 tickets; 3 escalated to vendor\n• Pilot budget approved: INR 4.5 lakh\nNEXT\n• Zenith demo on 3 Oct\n" + "".join(f"• {a['owner']}: {a['action']} (by {a['due']})\n" for a in acts) + "RISKS\n• Vendor API failing 1 in 20 calls")
print(out); hr(); print("CHECK STEP — every number in the output must exist in the notes:")
import re
nums = set(re.findall(r"\d[\d.,]*", out)); src = set(re.findall(r"\d[\d.,]*", NOTES)); bad = sorted(n.strip(".,") for n in nums if n.strip(".,") not in {s.strip(".,") for s in src})
table(["Numbers in output", "All found in notes?"], [[len(nums), "YES" if not bad else f"NO — check: {bad}"]])
print("\n  Time: 25 min by hand → about 4 min with the saved prompt, including the check.")
say("An automation without a check step is just a faster way to be wrong.")
