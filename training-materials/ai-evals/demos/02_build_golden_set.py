"""AI Evaluation & Quality Engineering · Demo 2 — Golden sets: coverage, labelling agreement, versioning (25 min) · Module 2
Shows: a golden set audited for distribution coverage against real traffic, two-labeller agreement, leakage from the prompt examples and a version hash
Lab: Draft your 50-query set: 60% typical, 15% paraphrase, 10% multi-document, 10% out-of-scope, 5% adversarial. Have a second person label ten. Compute agreement.
Run: python 02_build_golden_set.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Evaluation & Quality Engineering · Demo 2 — Golden sets: coverage, labelling agreement, versioning")
import csv, pathlib; G = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parents[2] / "agentic-ai-workshop/demos/test_sheet.csv"))); docs = [d for d in load_docs() if "draft" not in d["id"].lower()]

import hashlib, collections; TRAFFIC = {"simple": 0.45, "paraphrase": 0.30, "exact": 0.08, "multi": 0.07, "comparison": 0.04, "out_of_scope": 0.05, "adversarial": 0.01}; have = collections.Counter(t["type"] for t in G)
rows = [[ty, f"{share:.0%}", have.get(ty, 0), f"{have.get(ty, 0) / len(G):.0%}", "UNDER-COVERED" if have.get(ty, 0) / len(G) < share * 0.6 else "ok"] for ty, share in TRAFFIC.items()]; table(["Type", "Share of real traffic", "In golden set", "Share", "Coverage"], rows)
print(f"\n  {len(G)} queries. Paraphrases are 30% of what users type but under-represented — and there is no adversarial case at all.")
hr(); L1 = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1]; L2 = [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1]; k = evals.cohen_kappa(L1, L2); dis = [G[i]["question"][:50] for i in range(len(G)) if L1[i] != L2[i]]
print(f"Two people labelled the same 14 answers pass/fail: agreement {sum(a == b for a, b in zip(L1, L2)) / 14:.0%} · kappa {k:.2f}\n  They disagreed on: {dis}\n  → the labelling guide is ambiguous for comparison/partial answers. Fix the guide before you add more queries.")
hr(); FEWSHOT = ["How many days of annual leave do permanent employees get?"]; leak = [t["question"] for t in G if t["question"] in FEWSHOT]; print(f"Leakage check: {len(leak)} golden question(s) also appear as examples in the prompt → {leak} — remove from one side.")
v = hashlib.sha256("".join(t["question"] + t["expected"] for t in G).encode()).hexdigest()[:10]; print(f"\nGolden set version: gs-{v}  · stored in git next to the code · results are only comparable within the same version.")
say("A golden set is a product. It has coverage, an owner, a version — and it gets stale.")
