"""DEMO 4 — Hybrid RAG: the router that sends each question to the right machinery (Module 4, ~10 min).
documents → RAG · counts/totals → SQL · 'right now' → live API · chit-chat → no retrieval.
Run: python 04_router.py"""
import re, sqlite3; from common import *

banner("Demo 4 · The router (documents / SQL / live / none)")
# a tiny 'database' — what RAG cannot count
db = sqlite3.connect(":memory:"); db.executescript("""CREATE TABLE refunds(id INTEGER, month TEXT, amount REAL, reason TEXT);
INSERT INTO refunds VALUES (1,'2026-07',1200,'late'),(2,'2026-07',800,'damaged'),(3,'2026-08',450,'late'),(4,'2026-08',2300,'lost'),(5,'2026-09',700,'late'),(6,'2026-09',300,'late');""")
LIVE_STATUS = {"AWB123": "Out for delivery, ETA 16:40", "AWB999": "Held at customs — documents requested"}

def route(q: str) -> str:
    if LIVE:
        r = (llm.complete(f"Classify this question into exactly one of: documents, sql, live, none.\n- documents: policy/how-to questions answered from documents\n- sql: counts, totals, averages, 'how many'\n- live: current status of a specific shipment/order\n- none: greetings/thanks/rephrase\nQuestion: {q}\nAnswer with one word.", max_tokens=5) or "").strip().lower()
        if r in {"documents", "sql", "live", "none"}: return r
    ql = q.lower()
    if re.search(r"\b(hi|hello|thanks|thank you|rephrase|simpler)\b", ql): return "none"
    if re.search(r"\b(how many|total|sum|average|count|last quarter|per month)\b", ql): return "sql"
    if re.search(r"\b(where is|status|right now|track|awb\d+)\b", ql): return "live"
    return "documents"

def handle(q: str) -> str:
    r = route(q)
    if r == "none": return "(no retrieval — cheap direct reply) Happy to help — what would you like to know?"
    if r == "sql":
        if "last quarter" in q.lower() or "q3" in q.lower(): rows = db.execute("SELECT COUNT(*), SUM(amount) FROM refunds WHERE month BETWEEN '2026-07' AND '2026-09'").fetchone()
        else: rows = db.execute("SELECT COUNT(*), SUM(amount) FROM refunds").fetchone()
        return f"(SQL) {rows[0]} refunds totalling INR {rows[1]:,.0f} — computed, not guessed."
    if r == "live":
        awb = (re.search(r"awb\d+", q, re.I) or [None])[0]; return f"(live API) {LIVE_STATUS.get(awb.upper() if awb else '', 'Shipment not found — ask for the AWB number')}"
    docs = load_docs(); chunks = [c for d in docs for c in chunk_by_heading(d)]
    top = rerank(q, [c for _, c in rrf(bm25(q, chunks), semantic(q, chunks))[:8]], 3); text, *_ = answer(q, top); return f"(documents) {text}"

for q in ["What is the refund policy for late deliveries?", "How many refunds did we issue last quarter?", "Where is AWB123 right now?", "thanks!", "Can contractors carry over leave?"]:
    print(f"\n  Q: {q}\n  → route={route(q):<9} {handle(q)}")
hr()
print("Say it: 'Two questions that look the same need different machinery. Log every misroute — that list is your roadmap.'")
