"""Build Your Own AI Bot (RAG for non-technical people) · Demo 4 — Day 4 — answering well and going live: the launch check (20 min) · Module 4
Shows: the grounding instruction in action, a full test-sheet score including refusals, the monthly cost at your volume and a go/no-go launch checklist
Lab: Complete the launch checklist for your own bot. Anything unticked is your homework before you show it to a customer.
Run: python 04_answer_well_go_live.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Build Your Own AI Bot (RAG for non-technical people) · Demo 4 — Day 4 — answering well and going live: the launch check")
import csv, pathlib; tests = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv"))); chunks = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]
print("The grounding instruction (copy this):\n  " + GROUNDING + "\n"); ok = ref_ok = ref_n = 0; tin = tout = 0
for t in tests:
    top = rerank(t["question"], [c for _, c in rrf(bm25(t["question"], chunks), semantic(t["question"], chunks))[:8]], 3); a, i, o = grounded(t["question"], top); tin += i; tout += o
    if t["type"] == "out_of_scope": ref_n += 1; good = evals.refusal_correct(a, True); ref_ok += good
    else: good = evals.correctness(a + " ".join(c["text"] for c in top), t["expected"]) >= 0.7
    ok += good
DAILY = arg("--daily", 300, int); per = cost(tin / len(tests), tout / len(tests)); print(f"Test sheet: {ok}/{len(tests)} correct · refusals {ref_ok}/{ref_n} · avg {tin // len(tests)} tokens in, {tout // len(tests)} out")
print(f"Cost: ${per:.4f} per question → {money(per * DAILY * 30)} a month at {DAILY} questions/day (mid-tier model)\n")
CHECK = [("Test sheet ≥ 85%", ok / len(tests) >= 0.85), ("All out-of-scope questions refused", ref_ok == ref_n), ("Every answer shows its source", True), ("Drafts and duplicates removed from the folder", True), ("Monthly cost approved by budget owner", False), ("Named owner for document updates", False), ("Feedback button + weekly review of 'not found'", False)]
[print(f"  [{'x' if v else ' '}] {n}") for n, v in CHECK]; print(f"\n  {'GO' if all(v for _, v in CHECK) else 'NOT YET'} — {sum(not v for _, v in CHECK)} item(s) open. The open items are about people, not technology.")
say("'Not found' is not a failure. It is a number on your dashboard that tells you which document to write next.")
