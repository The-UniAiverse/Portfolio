"""AI Governance Practitioner · Demo 1 — Inventory and classification: classify 15 systems with the real engine (30 min) · Module 1
Shows: a 15-system register classified by the uniAIverse governance engine, with tier counts, controls required per tier and the systems whose tier people usually get wrong
Lab: Build your own register (15 rows minimum — include vendor tools with embedded AI). Classify by hand, then with /tools → Governance. Reconcile every difference.
Run: python 01_classify_fifteen_systems.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("AI Governance Practitioner · Demo 1 — Inventory and classification: classify 15 systems with the real engine")
import yaml; c = api(); S = yaml.safe_load(data_path(__file__, "register.yaml").read_text()); rows = []; tiers = {}
for s in S:
    guess = s.pop("team_guess"); r = c.post("/api/governance/classify", json=s).json(); tiers[r["risk_tier"]] = tiers.get(r["risk_tier"], 0) + 1; rows.append([s["name"][:40], guess, r["risk_tier"], "" if guess == r["risk_tier"] else "← reconcile", len(r["required_controls"])])
table(["System", "Team's guess", "Engine", "", "Controls required"], rows); print("\n  " + " · ".join(f"{k}: {v}" for k, v in sorted(tiers.items())) + f"   ·   {sum(1 for r in rows if r[3])} of {len(rows)} guessed wrong")
print("\n  Typical mistakes: 'it's only a vendor feature' (still your deployment) · 'a human is in the loop' (a rubber stamp is not oversight) · 'internal only' (employees have rights too).\n  Engine rules live in app/services/governance/ — framework-aligned guidance, not legal advice. Borderline cases go to counsel.")
say("The register is the foundation. You cannot govern, audit or insure a system nobody wrote down.")
