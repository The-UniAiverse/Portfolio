"""MLOps & LLMOps · Demo 3 — Monitoring: drift, quality, cost, SLOs — and the runbook (25 min) · Module 3
Shows: a week of production telemetry turned into a dashboard with four alert rules (quality, drift, cost, SLO burn) and the runbook step each alert triggers
Lab: Define one alert in each of the four families for your system, each with an owner and a first action. An alert without a runbook line is noise.
Run: python 03_dashboards_and_alerts.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("MLOps & LLMOps · Demo 3 — Monitoring: drift, quality, cost, SLOs — and the runbook")
W = [dict(day="Mon", req=9800, ok=9780, p95=2.1, cost=41.0, notfound=0.06, thumbs_down=0.021), dict(day="Tue", req=10100, ok=10085, p95=2.0, cost=42.5, notfound=0.06, thumbs_down=0.020), dict(day="Wed", req=10400, ok=10120, p95=2.4, cost=44.0, notfound=0.07, thumbs_down=0.024),
     dict(day="Thu", req=10250, ok=10230, p95=2.2, cost=71.9, notfound=0.07, thumbs_down=0.023), dict(day="Fri", req=9900, ok=9880, p95=2.1, cost=43.1, notfound=0.15, thumbs_down=0.041)]
rows = []
for i, d in enumerate(W):
    s = ops.slo_burn(d["ok"], d["req"], 0.995); base = sum(x["cost"] / x["req"] for x in W[:max(1, i)]) / max(1, i); al = []
    if s["burn_rate"] >= 2: al.append(f"SLO burn {s['burn_rate']:.1f}× → {s['action']}")
    if d["cost"] / d["req"] > 1.4 * base: al.append("COST per request +40%")
    if d["notfound"] > 0.12: al.append("NOT-FOUND rate doubled")
    if d["thumbs_down"] > 0.035: al.append("QUALITY thumbs-down spike")
    rows.append([d["day"], f"{d['req']:,}", f"{d['ok'] / d['req']:.2%}", f"{d['p95']}s", f"${d['cost'] / d['req'] * 1000:.2f}", f"{d['notfound']:.0%}", f"{d['thumbs_down']:.1%}", "; ".join(al) or "—"])
table(["Day", "Requests", "Success", "p95", "Cost / 1k", "Not found", "Thumbs down", "Alerts"], rows)
print("\nRUNBOOK\n  SLO burn      → check provider status, last deploy; roll back first, investigate second\n  COST +40%     → top users/teams by tokens; look for a loop, a missing cache, or history growth (Thursday: one integration looping)\n  NOT-FOUND ×2  → was a document removed or the index rebuilt? (Friday: refund policy dropped from the index during refresh)\n  QUALITY spike → sample 30 thumbs-down, tag causes, add to golden set")
say("Dashboards are for Monday morning. Alerts are for 2 a.m. Every alert needs a name next to it and a first step.")
