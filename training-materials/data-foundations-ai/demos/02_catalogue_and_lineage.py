"""Data Foundations for AI · Demo 2 — Catalogue, lineage, stewardship: entries that answer 'can I use this?' (25 min) · Module 2
Shows: catalogue entries validated for completeness, a lineage graph walked upstream to find why a number changed, and downstream to find who to warn
Lab: Write catalogue entries for three datasets in the YAML format. Trace one KPI on your dashboard back to its source tables. How many hops? How many owners?
Run: python 02_catalogue_and_lineage.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Data Foundations for AI · Demo 2 — Catalogue, lineage, stewardship: entries that answer 'can I use this?'")
import yaml; cat = yaml.safe_load(data_path(__file__, "catalogue.yaml").read_text()); REQ = ["owner", "steward", "description", "classification", "refresh", "allowed_uses", "quality_sla"]
table(["Dataset", "Owner", "Class", "Refresh", "Missing fields"], [[d["name"], d.get("owner", "—"), d.get("classification", "—"), d.get("refresh", "—"), ", ".join(k for k in REQ if not d.get(k)) or "complete"] for d in cat["datasets"]])
up = {d["name"]: d.get("upstream", []) for d in cat["datasets"]}
def walk(n, depth=0, seen=None):
    seen = seen or set(); out = [("  " * depth + n, next((d.get("owner", "?") for d in cat["datasets"] if d["name"] == n), "external"))]
    for u in up.get(n, []):
        if u not in seen: seen.add(u); out += walk(u, depth + 1, seen)
    return out
hr(); print("'On-time delivery %' dropped 4 points overnight. Walk the lineage upstream:"); [print(f"  {n:<38} owner: {o}") for n, o in walk("kpi_on_time_delivery")]
print("\n  → `hub_scan_events` changed its timezone handling last night (see its change log). Three hops, three owners — without lineage this is a two-day hunt.")
down = [d["name"] for d in cat["datasets"] if "hub_scan_events" in d.get("upstream", [])]; print(f"  Downstream of hub_scan_events — warn these owners: {down}")
g = cat["glossary"]; print(f"\nGlossary: 'on-time' = {g['on-time']}.  If sales and ops define it differently, the AI will be 'wrong' for one of them forever.")
say("A catalogue entry answers three questions: what is it, who owns it, and am I allowed to use it for this.")
