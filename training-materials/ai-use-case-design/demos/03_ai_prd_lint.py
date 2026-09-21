"""AI Use-Case Design & Product Ownership · Demo 3 — Write an AI PRD — and lint it (20 min) · Module 3
Shows: an AI product requirements document checked for the nine sections that ordinary PRDs miss, with a generated evaluation-set skeleton
Lab: Write your PRD in data/prd.md. Run the linter until it passes. Then write the first ten rows of the evaluation set it prints.
Run: python 03_ai_prd_lint.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Use-Case Design & Product Ownership · Demo 3 — Write an AI PRD — and lint it")
import re; P = data_path(__file__, "prd.md").read_text()
NEED = [("Success metric with baseline and target", r"baseline.*target|from \d.* to \d"), ("Evaluation set (size, source, who labels)", r"evaluation set|golden set|test sheet"), ("Out-of-scope behaviour / refusal", r"out[- ]of[- ]scope|refus|must not answer"),
        ("Human-in-the-loop points", r"human|approval|review(er)?\b"), ("Failure modes and what the user sees", r"failure mode|when (it|the model) (is )?wrong|fallback"), ("Cost limit per request or per month", r"cost (limit|cap|ceiling)|per request|\$\s?\d"),
        ("Latency target", r"latency|seconds|p95"), ("Data and permissions", r"permission|access control|acl|data source"), ("Risk tier and required controls", r"risk tier|limited|high[- ]risk|minimal")]
rows = [[n, "✓" if re.search(p, P, re.I | re.S) else "MISSING"] for n, p in NEED]; table(["AI PRD section", "Status"], rows); miss = [r[0] for r in rows if r[1] != "✓"]
print(f"\n  {len(NEED) - len(miss)}/{len(NEED)} present" + (f" — add: {'; '.join(miss)}" if miss else " — ready for review"))
hr(); print("Evaluation-set skeleton to fill (CSV):\n  id,question,expected_answer,type,source_document\n  1,<typical question>,<key facts>,typical,<doc>\n  2,<hard wording of the same>,<key facts>,paraphrase,<doc>\n  3,<needs two documents>,<key facts>,multi_doc,<docs>\n  4,<not in any document>,REFUSE,out_of_scope,—\n  5,<tries to trick it>,REFUSE,adversarial,—")
print("  Mix to aim for: 60% typical · 15% paraphrase · 10% multi-document · 10% out-of-scope · 5% adversarial")
say("If the PRD has no evaluation set, 'done' will be decided by whoever is most tired.")
