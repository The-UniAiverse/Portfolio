"""AI Security for Builders · Demo 4 — Governance hooks: security review in the lifecycle and the metrics (15 min) · Module 4
Shows: security checkpoints mapped to delivery gates, a release blocked by an open high finding, and five security metrics for the monthly report
Lab: Map these checkpoints onto your own release process. Which gate has no security evidence today?
Run: python 04_security_gates_and_metrics.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Security for Builders · Demo 4 — Governance hooks: security review in the lifecycle and the metrics")
GATES = [("G0 Initiate", "data classification · risk tier · threat model started"), ("G1 POC exit", "no production data outside approved environments · provider data terms reviewed"), ("G2 Pilot exit", "threat model complete · 5 baseline controls on · red-team run #1"), ("G3 Production", "findings closed or accepted by a named owner · incident runbook · logging + alerting live"), ("G4 Scale", "re-run red team per new tool/region · vendor review refreshed")]
table(["Gate", "Security evidence required"], [list(g) for g in GATES]); hr(); REL = {"name": "support-assistant 1.3", "findings": [("F-1", "HIGH", "open"), ("F-2", "MEDIUM", "accepted by CISO until 2026-12-01"), ("F-3", "LOW", "closed")], "runbook": True, "alerts": False}
blockers = [f"{i} {sev} is {st}" for i, sev, st in REL["findings"] if sev == "HIGH" and st == "open"] + ([] if REL["alerts"] else ["cost/abuse alerts not configured"]); print(f"Release {REL['name']} at G3: {'APPROVED' if not blockers else 'BLOCKED'}"); [print(f"   ✗ {b}") for b in blockers]
hr(); M = [("Attack success rate (weekly probe)", "19% → 6%", "↓ good"), ("Open HIGH findings older than 30 days", "1", "target 0"), ("Requests blocked by input policy", "0.4%", "watch for spikes"), ("PII redactions per 1,000 requests", "7.2", "trend, not target"), ("Mean time to revoke a tool/credential", "3 h", "target < 1 h")]
table(["Security metric", "This month", "Note"], [list(m) for m in M])
say("Security that lives outside the delivery gates gets done after launch. Which is to say, after the incident.")
