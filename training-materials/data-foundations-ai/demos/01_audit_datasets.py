"""Data Foundations for AI · Demo 1 — AI-ready data: audit ten datasets (25 min) · Module 1
Shows: ten datasets scored on availability, quality, classification and permissions into an AI-readiness heat table, with the blocker and owner action for each
Lab: Audit ten datasets you actually depend on, with the data owner in the room if possible. The lowest line of the top-priority dataset is your first ticket.
Run: python 01_audit_datasets.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Data Foundations for AI · Demo 1 — AI-ready data: audit ten datasets")
DS = [("TMS shipments", 5, 4, "internal", 4, "Ops"), ("Customer master", 4, 2, "personal", 3, "Sales ops"), ("Claims history", 4, 3, "personal", 2, "Claims"), ("Policy documents", 5, 3, "internal", 5, "HR/Legal"), ("Support emails", 3, 2, "personal", 1, "CS"), ("Driver records", 3, 3, "sensitive-personal", 1, "HR"),
      ("Invoices (PDF)", 4, 3, "confidential", 4, "Finance"), ("Web analytics", 5, 4, "pseudonymous", 5, "Marketing"), ("Call recordings", 2, 2, "sensitive-personal", 1, "CS"), ("Vendor contracts", 3, 4, "confidential", 2, "Legal")]
CAP = {"sensitive-personal": 2, "personal": 4}; rows = []
for n, av, q, cls, perm, own in DS:
    raw = (av + q + perm) / 15 * 100; score = min(raw, CAP.get(cls, 5) / 5 * 100 if perm <= 2 else 100); blocker = min((("availability", av), ("quality", q), ("permissions", perm)), key=lambda x: x[1])
    rows.append([n, av, q, cls, perm, f"{score:.0f}", "READY" if score >= 75 else "FIXABLE" if score >= 50 else "BLOCKED", f"{blocker[0]} → {own}"])
table(["Dataset", "Avail", "Quality", "Classification", "Permissions", "Score", "Status", "Blocker → owner"], sorted(rows, key=lambda r: -float(r[5])))
print(f"\n  {sum(r[6] == 'READY' for r in rows)} ready · {sum(r[6] == 'FIXABLE' for r in rows)} fixable · {sum(r[6] == 'BLOCKED' for r in rows)} blocked.  Personal data with unclear permissions is capped however clean it is — quality cannot buy a lawful basis.")
say("'Do we have the data?' is four questions: can we get it, is it any good, what class is it, and are we allowed.")
