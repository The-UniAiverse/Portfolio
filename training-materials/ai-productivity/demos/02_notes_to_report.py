"""AI Productivity Workflows · Demo 2 — Raw notes → report, with every number verified (15 min) · Module 2
Shows: schema-driven extraction into a report table, then a verification pass that traces each figure back to the notes
Lab: Add a field to SPEC (for example 'Headcount') and a sentence to the notes. Then deliberately change one number in the report and watch the verifier catch it.
Run: python 02_notes_to_report.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Productivity Workflows · Demo 2 — Raw notes → report, with every number verified")
NOTES = """Site visit Pune warehouse, 18 Sep. Throughput is 1,240 parcels per day against a target of 1,500. Error rate 2.3% (mostly address labels).
Overtime cost last month: INR 3.8 lakh. Manager says two scanners are broken. Proposed fix: label template + AI address check, estimated saving INR 1.1 lakh per month."""
SPEC = {"Site": r"visit\s+([\w\s]+?),", "Date": r"(\d{1,2}\s\w{3})", "Throughput/day": r"Throughput is ([\d,]+)", "Target/day": r"target of ([\d,]+)", "Error rate": r"Error rate ([\d.]+%)",
        "Overtime cost": r"Overtime cost[^:]*:\s*(INR [\d.]+ lakh)", "Est. saving/month": r"saving (INR [\d.]+ lakh)", "Customer complaints": r"complaints[^\d]*(\d+)"}
f = text.extract_fields(NOTES, SPEC); table(["Field", "Value (None = not in the notes)"], [[k, v] for k, v in f.items()])
gap = int(f["Target/day"].replace(",", "")) - int(f["Throughput/day"].replace(",", "")); print(f"\n  Computed by the spreadsheet, not the model: gap = {gap} parcels/day ({gap / 1500:.0%} below target)")
hr(); report = f"Pune warehouse runs {f['Throughput/day']} parcels/day vs target {f['Target/day']} ({gap} short). Error rate {f['Error rate']}. Overtime {f['Overtime cost']}. A label fix could save {f['Est. saving/month']} a month, paying back in under 4 months."
print("DRAFT PARAGRAPH:\n  " + report); import re
src = {x.rstrip(".,") for x in re.findall(r"\d[\d,.]*%?", NOTES)}
rows = [[n, "in notes" if n.rstrip(".,") in src else ("computed" if n == str(gap) else "NOT IN NOTES → challenge")] for n in re.findall(r"\d[\d,.]*%?", report)]; print(); table(["Figure in draft", "Trace"], rows)
say("Let AI write the sentence. Make it show you where each number came from. 'Under 4 months' was never in my notes.")
