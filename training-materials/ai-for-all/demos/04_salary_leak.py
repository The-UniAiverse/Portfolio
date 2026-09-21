"""AI for All · Demo 4 — The salary-leak case: check before you paste (10 min) · Module 5
Shows: a pre-paste check that finds personal and confidential data in text and produces a safe version
Lab: Paste a (fake) email from your own work into DRAFT. What did the checker catch? What did it miss that a human would see?
Run: python 04_salary_leak.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for All · Demo 4 — The salary-leak case: check before you paste")
DRAFT = """Hi team, please ask the AI to make this table look nicer before the board pack goes out:
Priya Nair, priya.nair@acme.in, +91 9820012345, PAN ABCPN1234K, salary INR 28,40,000, rating: below expectations
Rahul Mehta, rahul.m@acme.in, 9819912345, salary INR 19,10,000, rating: strong — promote in Q4 (CONFIDENTIAL, not announced)
Customer card for the refund: 4111 1111 1111 1111"""
print(DRAFT); hr()
hits = dataq.find_pii(DRAFT); table(["Type found", "Value"], [[k, v] for k, v in hits])
conf = [w for w in ("salary", "rating", "CONFIDENTIAL", "promote", "not announced") if w.lower() in DRAFT.lower()]
print(f"\n  Confidential markers: {', '.join(conf)}")
print("\nVERDICT: do not paste into a public AI tool.  Personal data: %d items · confidential HR content: yes" % len(hits))
hr(); safe, n = dataq.redact(DRAFT); safe = __import__("re").sub(r"INR [\d,]+", "INR [AMOUNT]", safe)
print("What you CAN paste (structure kept, people removed):\n"); print(safe)
print("\nThree questions before every paste:  1) Whose data is this?  2) Is this tool approved for it?  3) Would I be comfortable if this text appeared in a newspaper?")
say("The tool did not leak the salaries. A person pasted them. The control is the ten seconds before you press Enter.")
