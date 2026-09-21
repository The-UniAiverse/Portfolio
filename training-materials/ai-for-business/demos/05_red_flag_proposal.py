"""AI for Business Leaders · Demo 5 — Reading a proposal: the red-flag scanner (12 min) · Module 7
Shows: a vendor proposal scanned for the eight things a serious AI proposal must contain, with the question to ask for each gap
Lab: Bring a real proposal (or use the sample). Run the scanner, then write the three questions you will send back to the vendor.
Run: python 05_red_flag_proposal.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Business Leaders · Demo 5 — Reading a proposal: the red-flag scanner")
P = data_path(__file__, "proposal.txt").read_text()
CHECKS = [("Evaluation set / acceptance metric", r"evaluation set|test set|golden set|accuracy target|acceptance criteri", "How will we both know it works? On which questions, scored by whom?"), ("Run-cost model (tokens, per request)", r"per request|token|run cost|monthly cost|inference cost", "What does one request cost, and what is the monthly bill at our volume?"),
          ("Data plan (sources, quality, permissions)", r"data (plan|source|quality|access)|permission|lawful basis", "Which data, who prepares it, who is allowed to see what?"), ("Human oversight / escalation", r"human[- ]in[- ]the[- ]loop|escalat|approval|oversight", "What can it do without a person approving?"),
          ("Security & privacy controls", r"prompt injection|pii|redact|iso 27001|soc 2|dpdp|gdpr", "How is personal data protected and what happens on injection?"), ("Phased gates (POC → pilot → production)", r"poc|pilot|phase|gate|go/no-go", "Where can we stop, and what do we own if we do?"),
          ("Ownership of prompts, data, fine-tunes", r"ownership|intellectual property|\bip\b|export", "Who owns the prompts, the index and any fine-tuned model?"), ("Monitoring after go-live", r"monitor|drift|dashboard|sla|support", "Who watches quality and cost in month four?")]
import re; rows = []; flags = []
for name, pat, q in CHECKS:
    ok = bool(re.search(pat, P, re.I)); rows.append([name, "present" if ok else "MISSING"]); 
    if not ok: flags.append(q)
table(["A serious proposal contains", "Status"], rows); buzz = re.findall(r"\b(agentic|revolutionary|cutting-edge|fully autonomous|100% accura\w+|game[- ]chang\w+)\b", P, re.I)
print(f"\n  Selling words: {', '.join(sorted(set(b.lower() for b in buzz))) or 'none'}  ·  {len(flags)} of {len(CHECKS)} essentials missing")
print("\nQuestions to send back:"); [print(f"  {i}. {q}") for i, q in enumerate(flags, 1)]
say("A proposal with no evaluation set is a promise. A proposal with no cost model is a surprise.")
