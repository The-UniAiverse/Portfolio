"""Data Foundations for AI · Demo 4 — Knowledge bases for GenAI: curate, version, dedup, refresh, permit (25 min) · Module 4
Shows: a document folder turned into a curated knowledge base: drafts and superseded versions removed, near-duplicates resolved, review dates checked, ACL metadata attached — with retrieval before and after
Lab: Run the curation report on a real shared folder. How many documents survive? Who owns the refresh of each survivor?
Run: python 04_curated_knowledge_base.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Data Foundations for AI · Demo 4 — Knowledge bases for GenAI: curate, version, dedup, refresh, permit")
docs = load_docs(); META = {"leave_policy": {"version": "v3", "effective": "2026-04-01", "review_by": "2027-04-01", "owner": "HR", "acl": []}, "refund_policy": {"version": "v2", "effective": "2025-11-01", "review_by": "2026-05-01", "owner": "Claims", "acl": []},
        "security_policy": {"version": "v1", "effective": "2026-01-15", "review_by": "2027-01-15", "owner": "Security", "acl": ["it", "managers"]}, "zz_old_leave_policy_DRAFT": {"version": "draft", "effective": None, "review_by": None, "owner": None, "acl": []}}
rows = []; keep = []
for d in docs:
    m = META.get(d["id"], {}); why = "draft / no owner" if not m.get("owner") else "REVIEW OVERDUE" if m["review_by"] < "2026-09-21" else ""; rows.append([d["id"], m.get("version", "?"), m.get("owner") or "—", m.get("review_by") or "—", "EXCLUDE" if "draft" in why else "KEEP + flag" if why else "KEEP", why])
    if "draft" not in why: keep.append(d)
table(["Document", "Version", "Owner", "Review by", "Decision", "Why"], rows); dups = dataq.near_duplicates([{"id": d["id"], "text": d["text"]} for d in docs], 0.3); print(f"\n  Near-duplicates: {dups or 'none'} → keep the effective version only")
hr(); q = "How many days of annual leave do employees get?"
for label, pool in (("before curation", docs), ("after curation", keep)):
    ch = [c for d in pool for c in chunk_by_heading(d)]; top = [c for _, c in rrf(bm25(q, ch), semantic(q, ch))[:3]]; print(f"  {label:<16} top sources: {[c['doc'][:34] for c in top]}")
print("\n  Before curation the draft competes with the policy — and drafts often win, because they are wordier.")
print("  Refresh plan: owner per document · re-index on change (hash) · overdue reviews shown to users as a warning, not hidden.")
say("A knowledge base is a publication. It needs an editor, not just an uploader.")
