"""AI Engineer · Demo 8 — Capstone: review an end-to-end feature against the Definition of Done (20 min) · Module 8
Shows: an automated Definition-of-Done review across data, model, service, ops and governance evidence — the checklist reviewers use on capstone day
Lab: Present your capstone against this checklist. For every unticked line, state whether it is 'not done', 'not needed and why', or 'next sprint'.
Run: python 08_capstone_definition_of_done.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 8 — Capstone: review an end-to-end feature against the Definition of Done")
EVID = {"problem framed with business metric": True, "baseline recorded": True, "no leakage (time-aware split / feature audit)": True, "data quality report attached": True, "PII masked or justified": True, "model card written": True, "calibration checked": False,
        "typed API with input validation": True, "tests run in CI without network": True, "secrets in environment only": True, "registry + promotion gates defined": True, "rollback tested": False, "drift monitors + alert owner named": True, "run-cost estimate": False, "risk tier recorded and controls mapped": True}
AREAS = {"Data": list(EVID)[:5], "Model": list(EVID)[5:7], "Service": list(EVID)[7:10], "Operations": list(EVID)[10:14], "Governance": list(EVID)[14:]}
for ar, items in AREAS.items():
    print(f"\n{ar}"); [print(f"  [{'x' if EVID[i] else ' '}] {i}") for i in items]
done = sum(EVID.values()); print(f"\n  {done}/{len(EVID)} evidenced → {'PASS' if done == len(EVID) else 'CONDITIONAL — close: ' + '; '.join(k for k, v in EVID.items() if not v)}")
say("Done is not 'it runs on my laptop'. Done is evidence in fifteen boxes that someone else can check.")
