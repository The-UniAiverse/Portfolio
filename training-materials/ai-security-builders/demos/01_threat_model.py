"""AI Security for Builders · Demo 1 — Threat model your LLM system (25 min) · Module 1
Shows: a system described as components and data flows, mapped to LLM-specific threats with likelihood × impact scoring and the control that addresses each
Lab: Draw your system as boxes and arrows. For every arrow that carries untrusted text, name the threat and the control. No control = your backlog.
Run: python 01_threat_model.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Security for Builders · Demo 1 — Threat model your LLM system")
SYSTEM = {"components": ["web chat", "orchestrator", "vector index", "policy docs (uploaded by staff)", "email ingestion (from customers)", "tools: get_shipment, create_refund", "LLM provider"], "untrusted_inputs": ["web chat", "email ingestion (from customers)", "policy docs (uploaded by staff)"], "write_tools": ["create_refund"], "pii": True, "public": True}
T = [("Prompt injection (direct)", "web chat → orchestrator", 5, 3, "input classifier · instructions/data separation · no secrets in the prompt"), ("Prompt injection (indirect)", "email / documents → index → prompt", 4, 5, "strip hidden text · wrap as untrusted data · tools cannot be triggered by document content alone"),
     ("Sensitive information disclosure", "index → answer", 3, 5, "ACL filter BEFORE retrieval · PII redaction · per-user identity"), ("Excessive agency", "LLM → create_refund", 3, 5, "least-privilege scopes · human approval over a limit · amount caps in code"),
     ("Insecure output handling", "answer → browser", 3, 4, "escape markup · allow-list links · never render model HTML"), ("Data/model poisoning", "staff uploads → index", 2, 4, "upload review · provenance metadata · quarantine new sources"),
     ("Unbounded consumption (denial of wallet)", "web chat → LLM provider", 4, 3, "per-user budgets · max tokens · rate limits · alerts on cost per user"), ("Supply chain (model, MCP servers, packages)", "provider / plugins", 2, 4, "pin versions · vet MCP manifests · vendor review")]
rows = sorted(([n, flow, l, i, l * i, ctl] for n, flow, l, i, ctl in T), key=lambda r: -r[4]); table(["Threat", "Where", "L", "I", "Risk", "Primary controls"], [[r[0], r[1][:36], r[2], r[3], r[4], r[5][:70]] for r in rows])
print(f"\n  Top three by risk: {', '.join(r[0] for r in rows[:3])}.\n  Categories follow the OWASP Top 10 for LLM Applications — check the current edition for exact names and numbering before you cite it in a report.")
say("Anywhere untrusted text can reach your prompt is an input field for the attacker. Draw those arrows first.")
