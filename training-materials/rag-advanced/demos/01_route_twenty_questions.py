"""Advanced, Hybrid & Agentic RAG · Demo 1 — Hybrid systems: route 20 real questions to documents, SQL, live API or refusal (25 min) · Module 2
Shows: a router over four back-ends — documents, a SQL table, a live API and refusal — with text-to-SQL that is computed, not guessed, and a misroute log
Lab: Take 20 questions from your own logs. Label the correct route by hand, run the router, and read the misroute log. Each misroute is a rule or an example you are missing.
Run: python 01_route_twenty_questions.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("Advanced, Hybrid & Agentic RAG · Demo 1 — Hybrid systems: route 20 real questions to documents, SQL, live API or refusal")
import sqlite3, re; db = sqlite3.connect(":memory:"); db.execute("create table refunds(id, month, amount, reason)"); db.executemany("insert into refunds values(?,?,?,?)", [(i, m, a, r) for i, (m, a, r) in enumerate([("2026-07", 450, "late"), ("2026-07", 8200, "lost"), ("2026-08", 450, "late"), ("2026-08", 3100, "damaged"), ("2026-08", 450, "late"), ("2026-09", 12500, "damaged")])])
ch = [c for d in load_docs() if "draft" not in d["id"].lower() for c in chunk_by_heading(d)]; LIVE_API = {"SH-1042": "delayed 26h at Pune hub", "SH-2210": "delivered 19 Sep 14:02"}
def route(q):
    ql = q.lower()
    if re.search(r"sh-\d+", ql): return "live_api"
    if re.search(r"\b(how many|total|average|sum|count|most common)\b", ql) and re.search(r"refund|claim", ql): return "sql"
    if re.search(r"salary|weather|stock price|competitor", ql): return "refuse"
    return "documents"
def to_sql(q):
    ql = q.lower(); m = re.search(r"(july|august|september)", ql); mon = {"july": "2026-07", "august": "2026-08", "september": "2026-09"}.get(m.group(1)) if m else None; w = f" where month='{mon}'" if mon else ""
    if "most common" in ql: return f"select reason, count(*) from refunds{w} group by reason order by 2 desc limit 1"
    return f"select {'count(*)' if 'how many' in ql else 'sum(amount)' if 'total' in ql else 'avg(amount)'} from refunds{w}"
QS = [("How late must a delivery be for a fee refund?", "documents"), ("How many refunds did we pay in August?", "sql"), ("Where is SH-1042?", "live_api"), ("What is the total refund amount in September?", "sql"), ("What does ERR_SVC_4471 mean?", "documents"), ("What is the CEO's salary?", "refuse"),
      ("What is the most common refund reason?", "sql"), ("Was SH-2210 delivered?", "live_api"), ("How much did we refund for damaged goods?", "sql"), ("Can contractors carry over leave?", "documents")]
mis = []
for q, want in QS:
    r = route(q)
    if r == "sql": s = to_sql(q); out = f"{db.execute(s).fetchone()}   ← {s}"
    elif r == "live_api": out = LIVE_API.get(re.search(r"SH-\d+", q).group(0), "unknown")
    elif r == "refuse": out = "out of scope — refused"
    else: out = grounded(q, rerank(q, [c for _, c in rrf(bm25(q, ch), semantic(q, ch))[:8]], 3))[0][:90]
    print(f"  {r:<10}{'✓' if r == want else '✗'} {q[:48]:<48} → {out}"); mis += [(q, want, r)] if r != want else []
print(f"\n  {len(QS) - len(mis)}/{len(QS)} routed correctly. MISROUTE LOG:"); [print(f"    '{q}' should be {w}, went to {r} → add a rule/example") for q, w, r in mis]
say("'How many' is a database question. If the model counts from retrieved text, it is guessing with confidence.")
