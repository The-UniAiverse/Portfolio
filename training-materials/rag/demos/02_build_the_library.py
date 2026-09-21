"""Build Your Own AI Bot (RAG for non-technical people) · Demo 2 — Day 2 — building the library: clean, chunk, label, permit (20 min) · Module 2
Shows: a document folder audited for drafts and duplicates, chunked two ways, given a contextual prefix and permission labels — and what a restricted user can no longer see
Lab: Audit your own 20-document folder with this script (put .md/.txt files in the workshop sample_docs folder). Read five of your chunks aloud: would a new colleague understand each one alone?
Run: python 02_build_the_library.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Build Your Own AI Bot (RAG for non-technical people) · Demo 2 — Day 2 — building the library: clean, chunk, label, permit")
docs = load_docs(); print(f"{len(docs)} documents in the folder\n")
table(["Document", "Chars", "Sections", "Flag"], [[d["title"][:40], len(d["text"]), len(chunk_by_heading(d)), "DRAFT — exclude" if "draft" in d["id"].lower() or "draft" in d["title"].lower() else ""] for d in docs])
dups = dataq.near_duplicates([{"id": d["id"], "text": d["text"]} for d in docs], thr=0.35); print("\nNear-duplicates (the bot will quote whichever it finds first):"); [print(f"  {a} ~ {b}  similarity {s}") for a, b, s in dups] or print("  none")
hr(); keep = [d for d in docs if "draft" not in d["id"].lower()]; fixed = [c for d in keep for c in chunk_fixed(d)]; head = [c for d in keep for c in chunk_by_heading(d)]
print(f"Fixed 400-char chunks: {len(fixed)} · Heading chunks: {len(head)}\n\n  fixed  : {fixed[2]['text'][:120]!r}\n  heading: {head[2]['text'][:150]!r}")
hr(); ACL = {"security_policy": ["it", "managers"]}
for c in head: c["acl"] = ACL.get(c["id"].split("#")[0], [])
for user, groups in [("Asha (manager)", {"managers"}), ("Ravi (agent)", {"agents"})]: print(f"  {user:<16} can search {len(guard.acl_filter(head, groups))}/{len(head)} chunks")
say("Rubbish in the folder is rubbish in the answer. Curating twenty good documents beats indexing two thousand.")
