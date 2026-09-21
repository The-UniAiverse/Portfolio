"""AI Productivity Workflows · Demo 1 — Meeting → actions → follow-up emails (15 min) · Module 1
Shows: owner/action/date extraction from a transcript, the gaps it refuses to guess, and one follow-up per owner
Lab: Paste the notes of your last real meeting (names changed) into data/meeting.txt and re-run. Which actions had no date? Fix the meeting habit, not the tool.
Run: python 01_meeting_to_followups.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Productivity Workflows · Demo 1 — Meeting → actions → follow-up emails")
T = data_path(__file__, "meeting.txt").read_text(); print(T); hr()
if LIVE: print(llm.complete("Extract action items as 'owner | action | due'. If no due date was said, write 'not stated' — never invent one.\n\n" + T, max_tokens=300)); acts = text.extract_actions(T)
else: acts = text.extract_actions(T)
table(["Owner", "Action", "Due"], [[a["owner"], a["action"], a["due"]] for a in acts])
gaps = [a for a in acts if a["due"] == "not stated"]; print(f"\n  {len(acts)} actions · {len(gaps)} without a date → ask in the follow-up, do not guess")
hr(); by = {}
for a in acts: by.setdefault(a["owner"], []).append(a)
for who, items in list(by.items())[:2]:
    print(f"To: {who}\nSubject: Actions from today's pricing review\n\nHi {who}, thanks for today. You took:\n" + "\n".join(f"  • {i['action']}" + (f" — by {i['due']}" if i['due'] != 'not stated' else " — could you confirm a date?") for i in items) + "\n")
say("The model is a good note-taker and a bad mind-reader. If nobody said a date, the right output is a question.")
