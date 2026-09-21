"""AI Use-Case Design & Product Ownership · Demo 4 — Prototype without code — and test it with a test sheet (20 min) · Module 4
Shows: a grounded prototype on sample documents scored against a test sheet, showing pass/fail per question type before anyone says 'it feels good'
Lab: Build the same bot in your no-code tool on the same documents. Run the same ten questions by hand. Do your scores match the script's? Where they differ, why?
Run: python 04_prototype_and_test.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Use-Case Design & Product Ownership · Demo 4 — Prototype without code — and test it with a test sheet")
import csv, pathlib
docs = load_docs(); chunks = [c for d in docs for c in chunk_fixed(d)]   # a no-code tool's DEFAULT settings: fixed-size chunks, meaning-only search, drafts left in the folder
tests = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv")))
rows = []; by = {}
for t in tests:
    top = [c for _, c in semantic(t["question"], chunks)[:3]]; ans, *_ = grounded(t["question"], top)
    ok = ("could not find" in ans.lower()) if t["type"] == "out_of_scope" else evals.correctness(ans, t["expected"]) >= 0.6
    rows.append([t["question"][:50], t["type"], "PASS" if ok else "FAIL"]); by.setdefault(t["type"], []).append(ok)
table(["Question", "Type", "Result"], rows); print(); [print(f"  {k:<14}{sum(v)}/{len(v)}") for k, v in by.items()]
tot = sum(sum(v) for v in by.values()); print(f"\n  Overall {tot}/{len(tests)} = {tot / len(tests):.0%}.  Launch bar in the PRD: 85% overall AND 100% on out-of-scope.")
say("A demo shows the three questions that work. A test sheet shows the seven you did not think to ask.")
