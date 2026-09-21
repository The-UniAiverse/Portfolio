"""AI for Sales · Demo 6 — Guardrails and the stage-by-stage prompt playbook (10 min) · Module 6
Shows: a pre-send guardrail check (PII, pricing, unsupported claims, disclosure) and a five-stage prompt playbook scored for completeness
Lab: Write one prompt per pipeline stage for your own team. Run the guardrail on a real draft before it goes out.
Run: python 06_guardrails_playbook.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI for Sales · Demo 6 — Guardrails and the stage-by-stage prompt playbook")
DRAFT = "Hi Mr. Desai, as discussed with Anita (anita.rao@zenith.in, 9820098200) we guarantee the best price of INR 32,00,000 and 100% on-time delivery. Our AI wrote this proposal."
hits = dataq.find_pii(DRAFT); cl = text.check_claims(DRAFT, {"sla": "99.2% on-time delivery in FY26"}); import re
CHECKS = [("No third-party personal data", not hits, f"{len(hits)} item(s): " + ", ".join(k for k, _ in hits)), ("Price entered/approved by a human", not re.search(r"INR [\d,]+", DRAFT), "price present → needs manager approval tag"),
          ("No unsupported claims", all(c["status"] == "supported" for c in cl), "; ".join(c["status"] for c in cl)), ("Sent from approved tool only", True, "")]
print(DRAFT + "\n"); [print(f"  [{'x' if ok else ' '}] {n}" + ("" if ok else f"   ← {why}")) for n, ok, why in CHECKS]; print(f"\n  {'SEND' if all(c[1] for c in CHECKS) else 'HOLD — fix before sending'}"); hr()
PLAY = {"Prospect": "Brief on {account} from these facts: {facts}. Source each line. Say 'unknown' where blank.", "Outreach": "In my voice ({samples}), one trigger ({trigger}), one ask. Under 80 words. No claims beyond {approved_facts}.",
        "Discovery": "From {transcript} fill {crm_schema}. Leave unknown fields empty. List my open questions.", "Proposal": "Skeleton from {past_win}; leave [PRICE] and [TERMS] blank for me.", "Close/Renew": "Summarise usage {data} and risks; draft a renewal note. Flag anything I should verify."}
table(["Stage", "Saved prompt"], [[k, v] for k, v in PLAY.items()])
say("Pricing stays human. Customer data stays in approved tools. Everything else, save the prompt and reuse it.")
