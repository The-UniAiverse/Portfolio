"""AI Engineer · Demo 2 — Data pipelines: validate, quarantine, report (25 min) · Module 2
Shows: a batch pipeline with schema and quality rules that quarantines bad rows instead of failing silently, and a quality report you can attach to a release
Lab: Add two rules of your own (a range and a regex). Feed it tomorrow's file with one new kind of error. Does the pipeline stop, quarantine, or pass it silently?
Run: python 02_validated_pipeline.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Engineer · Demo 2 — Data pipelines: validate, quarantine, report")
import csv; rows = list(csv.DictReader(open(data_path(__file__, "customers_batch.csv"))))
RULES = {"customer_id": {"required": True, "unique": True, "regex": r"C\d{4}"}, "monthly_bill": {"required": True, "min": 0, "max": 5000}, "tenure_months": {"min": 0, "max": 600}, "plan": {"allowed": ["basic", "plus", "pro"]}, "email": {"regex": r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"}, "_freshness": ("updated_at", 45)}
rep = dataq.profile(rows, RULES); table(["Column", "Complete", "Unique", "Valid"], [[c, pct(v["completeness"]), pct(v["uniqueness"]), pct(v["validity"])] for c, v in rep["columns"].items()])
print("\nIssues:"); [print(f"  ✗ {i}") for i in rep["issues"]]; print(f"\n  PII columns detected: {rep['pii_columns']} → mask before this table reaches a feature store")
import re; seen = set(); good, bad = [], []
for r in rows:
    why = [k for k, ru in RULES.items() if k != "_freshness" and ((ru.get("required") and not r.get(k)) or ("regex" in ru and r.get(k) and not re.fullmatch(ru["regex"], r[k])) or ("allowed" in ru and r.get(k) not in ru["allowed"]))]
    try:
        if not 0 <= float(r["monthly_bill"] or "x") <= 5000: why.append("monthly_bill")
    except ValueError: why.append("monthly_bill")
    if r["customer_id"] in seen: why.append("duplicate id")
    seen.add(r["customer_id"]); (bad if why else good).append((r["customer_id"], sorted(set(why))))
print(f"\n  Loaded {len(good)} rows · quarantined {len(bad)}: " + "; ".join(f"{i} ({', '.join(w)})" for i, w in bad)); print(f"  Quality score {rep['score']}/100 · gate: {'PASS' if len(bad) / len(rows) <= 0.1 else 'FAIL — over 10% quarantined, stop the load and page the data owner'}")
say("A pipeline that never fails is a pipeline that is not checking. Quarantine loudly.")
