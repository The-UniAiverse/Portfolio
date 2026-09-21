"""Safe & Responsible AI Use at Work · Demo 2 — Spot the attack: injection, leakage and deepfake fraud (15 min) · Module 2
Shows: eight inputs run through real controls (hidden-text stripping, injection classifier, PII redaction) and a red-flag checklist for a voice-clone payment request
Lab: In pairs: write one message that tries to trick an assistant. Add it to the list in labkit/guard.py ATTACKS and see if it is caught. Then design the control that would catch it.
Run: python 02_spot_the_attack.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Safe & Responsible AI Use at Work · Demo 2 — Spot the attack: injection, leakage and deepfake fraud")
controls = {"strip_hidden", "classifier", "delimiters", "pii"}; rows = []
for name, payload, source in guard.ATTACKS:
    r = guard.defend(payload, source, controls)
    rows.append([name, source, "BLOCKED" if r["blocked"] else "FLAGGED + treated as data" if r["flagged"] else "cleaned" if r["log"] else "passed", "; ".join(r["log"])[:60] or "—"])
table(["Input", "Arrives via", "Outcome", "Controls that fired"], rows)
hr(); print("What the hidden-text attack looked like to a human vs. to the machine:")
raw = guard.ATTACKS[3][1]; clean, n = guard.strip_hidden(raw); print(f"  human sees : Leave policy. Annual leave is 24 days.\n  machine got: {raw!r}\n  after strip: {clean!r}  ({n} hidden characters removed)")
hr(); MSG = {"channel": "WhatsApp voice note", "from": "the CFO (voice sounds right)", "ask": "transfer INR 18 lakh to a new vendor today", "pressure": "urgent, confidential, do not call me", "new_payee": True}
FLAGS = [("New payee or changed bank details", MSG["new_payee"]), ("Urgency + secrecy", "urgent" in MSG["pressure"]), ("Asks you NOT to verify", "do not call" in MSG["pressure"]), ("Unusual channel for a payment instruction", "WhatsApp" in MSG["channel"])]
print("Deepfake payment request — red flags:"); [print(f"  [{'x' if f else ' '}] {t}") for t, f in FLAGS]
print(f"\n  {sum(f for _, f in FLAGS)}/4 flags → STOP. Call back on a number you already have. No exception for seniority.")
say("You cannot hear a deepfake. You can always hear an unusual request. Verify the request, not the voice.")
