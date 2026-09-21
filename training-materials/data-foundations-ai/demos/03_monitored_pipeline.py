"""Data Foundations for AI · Demo 3 — Pipelines: incremental loads, CDC, validation and monitoring (25 min) · Module 3
Shows: a three-day incremental load with change-data-capture (insert/update/delete), validation gates, idempotent re-runs and a run log with alerts
Lab: Re-run day 2 twice. Is your target unchanged? Then break the schema on day 3 and decide: fail the load, or quarantine and continue?
Run: python 03_monitored_pipeline.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Data Foundations for AI · Demo 3 — Pipelines: incremental loads, CDC, validation and monitoring")
TARGET = {}; LOG = []
DAYS = {"day1": [("I", "C1", {"name": "Zenith", "tier": "gold"}), ("I", "C2", {"name": "Kaveri", "tier": "silver"}), ("I", "C3", {"name": "Metro", "tier": "bronze"})],
        "day2": [("U", "C2", {"name": "Kaveri", "tier": "gold"}), ("I", "C4", {"name": "Lotus", "tier": "silver"}), ("D", "C3", None)], "day3": [("U", "C1", {"name": "Zenith", "tier": "platinum!!"}), ("I", "C5", {"name": "", "tier": "bronze"}), ("I", "C6", {"name": "Orbit", "tier": "silver"})]}
def valid(row): return bool(row["name"]) and row["tier"] in ("bronze", "silver", "gold", "platinum")
def load(day, batch):
    ins = upd = dele = bad = 0
    for op, key, row in batch:
        if op == "D": dele += TARGET.pop(key, None) is not None; continue
        if not valid(row): bad += 1; continue
        if key in TARGET: upd += TARGET[key] != row
        else: ins += 1
        TARGET[key] = row
    rate = bad / len(batch); status = "ALERT: quarantine rate {:.0%} > 20% — page data owner".format(rate) if rate > 0.2 else "ok"; LOG.append([day, len(batch), ins, upd, dele, bad, len(TARGET), status])
for d, b in DAYS.items(): load(d, b)
load("day2 (re-run)", DAYS["day2"]); table(["Run", "Changes in", "Inserted", "Updated", "Deleted", "Quarantined", "Rows in target", "Status"], LOG)
print("\n  Re-running day 2 changed nothing (0/0/0): the load is IDEMPOTENT because it is keyed upserts, not appends.\n  Full reload would move every row every night; CDC moved 9 changes in three days.")
print("  The delete on day 2 matters for AI: if C3 asked to be forgotten, the row must also leave the feature store, the index and the embeddings.")
say("An AI system is only as fresh — and as forgetful — as the pipeline that feeds it.")
