"""GenAI Engineer · Demo 2 — Ingestion: a messy two-column export, cleaned, deduplicated, with metadata and ACLs (25 min) · Module 2
Shows: layout-aware repair of a two-column text export, boilerplate and hidden-text removal, near-duplicate detection and metadata/ACL capture — with before/after retrieval
Lab: Export one of your own PDFs to text. Find three kinds of damage (columns, headers/footers, hyphenation). Fix one in code and re-test retrieval.
Run: python 02_ingestion_messy_documents.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("GenAI Engineer · Demo 2 — Ingestion: a messy two-column export, cleaned, deduplicated, with metadata and ACLs")
RAW = data_path(__file__, "two_column_export.txt").read_text(); print("RAW EXPORT (first lines):\n" + "\n".join("  " + l for l in RAW.splitlines()[:6])); import re
def fix_columns(t):
    L, R = [], []
    for line in t.splitlines():
        if re.match(r"\s*(Page \d+|ACME CONFIDENTIAL)", line): continue                      # header/footer boilerplate
        m = re.match(r"(.{0,38}?)\s{3,}(\S.*)$", line)
        if m: L.append(m.group(1).rstrip()); R.append(m.group(2).rstrip())
        else: L.append(line.rstrip())
    t = "\n".join(L + R); t = re.sub(r"(\w)-\n(\w)", r"\1\2", t); return re.sub(r"\n{2,}", "\n", t)
clean = fix_columns(RAW); clean, hidden = guard.strip_hidden(clean); print(f"\nCLEANED ({hidden} hidden characters stripped):\n" + "\n".join("  " + l for l in clean.splitlines()[:9]))
q = "What is the claim limit for damaged goods?"; hr()
for label, t in (("raw export", RAW), ("cleaned", clean)):
    ch = chunk_fixed({"id": "d", "title": "Claims", "text": t}, 220); a, *_ = answer(q, [c for _, c in bm25(q, ch)[:2]]); print(f"  {label:<11} → {a[:120]}")
hr(); META = {"doc_id": "POL-017", "title": "Claims policy", "version": "3.2", "effective": "2026-07-01", "owner": "Head of Claims", "acl": ["claims", "cs-leads"], "source_hash": __import__("hashlib").sha256(clean.encode()).hexdigest()[:10]}
print("Metadata captured at ingestion (you cannot add permissions later):"); [print(f"  {k:<12}{v}") for k, v in META.items()]
d = dataq.near_duplicates([{"id": "POL-017 v3.2", "text": clean}, {"id": "POL-017 v3.1 (old)", "text": clean.replace("50,000", "40,000")}], 0.6); print(f"\n  Near-duplicate found: {d[0] if d else 'none'} → index only the effective version, or the bot will quote both limits.")
say("Retrieval quality is decided at ingestion. No reranker recovers a sentence that was interleaved with the column next to it.")
