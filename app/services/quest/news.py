"""Curated AI news: fetch RSS → pending queue → admin approval → public feed. Optional LLM summary + quiz-question drafts."""
from __future__ import annotations
import hashlib, json, re
import xml.etree.ElementTree as ET
from pathlib import Path
import httpx, yaml
from app.core import db, llm

HERE = Path(__file__).parent

def sources() -> dict: return yaml.safe_load((HERE / "news_sources.yaml").read_text())

def _text(el, *names):
    for n in names:
        x = el.find(n)
        if x is not None and (x.text or "").strip(): return re.sub(r"<[^>]+>", "", x.text).strip()
    return ""

def parse_feed(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text); items = []
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for it in root.iter("item"):  # RSS 2.0
        items.append({"title": _text(it, "title"), "url": _text(it, "link"), "summary": _text(it, "description")[:600], "published": _text(it, "pubDate")})
    for e in root.findall(".//atom:entry", ns):  # Atom
        link = e.find("atom:link", ns); href = link.get("href") if link is not None else ""
        items.append({"title": _text(e, "{http://www.w3.org/2005/Atom}title"), "url": href,
                      "summary": _text(e, "{http://www.w3.org/2005/Atom}summary", "{http://www.w3.org/2005/Atom}content")[:600],
                      "published": _text(e, "{http://www.w3.org/2005/Atom}updated", "{http://www.w3.org/2005/Atom}published")})
    return [i for i in items if i["title"] and i["url"]]

def refresh(timeout: float = 10.0) -> dict:
    cfg = sources(); added, errors = 0, {}
    for s in cfg["sources"]:
        try:
            r = httpx.get(s["url"], timeout=timeout, follow_redirects=True, headers={"User-Agent": "uniAIQuest/1.0"}); r.raise_for_status()
            items = parse_feed(r.text)[: cfg["max_items_per_source"]]
        except Exception as e:
            errors[s["id"]] = str(e)[:120]; continue
        with db.conn() as c:
            for it in items:
                nid = hashlib.sha1(it["url"].encode()).hexdigest()[:12]
                if c.execute("SELECT 1 FROM news WHERE id=?", (nid,)).fetchone(): continue
                c.execute("INSERT INTO news (id, source, title, url, summary, published, status, tags, fetched_at) VALUES (?,?,?,?,?,?,?,?,?)",
                          (nid, s["title"], it["title"], it["url"], it["summary"], it["published"], "pending", json.dumps(s["tags"]), db.now()))
                added += 1
    return {"added": added, "errors": errors}

def add_manual(title: str, url: str, summary: str, source: str = "Admin", tags: list[str] | None = None) -> dict:
    nid = hashlib.sha1(url.encode()).hexdigest()[:12]
    with db.conn() as c:
        c.execute("INSERT OR REPLACE INTO news (id, source, title, url, summary, published, status, tags, fetched_at) VALUES (?,?,?,?,?,?,?,?,?)",
                  (nid, source, title, url, summary, "", "pending", json.dumps(tags or []), db.now()))
    return {"id": nid, "status": "pending"}

def queue(status: str = "pending", limit: int = 50) -> list[dict]:
    with db.conn() as c:
        rows = c.execute("SELECT * FROM news WHERE status=? ORDER BY fetched_at DESC LIMIT ?", (status, limit)).fetchall()
    return [dict(r) | {"tags": json.loads(r["tags"])} for r in rows]

def moderate(news_id: str, action: str, summary: str | None = None) -> dict:
    status = {"approve": "approved", "reject": "rejected"}[action]
    with db.conn() as c:
        c.execute("UPDATE news SET status=?, approved_at=?, summary=COALESCE(?, summary) WHERE id=?", (status, db.now(), summary, news_id))
    return {"id": news_id, "status": status}

def public_feed(tier: str, limit: int = 20) -> list[dict]:
    items = queue("approved", limit)
    if tier == "free":  # headlines only
        return [{"title": i["title"], "source": i["source"], "url": i["url"], "published": i["published"]} for i in items]
    return items

def draft_question(news_id: str) -> dict:
    """Turn an approved news item into a quiz-question draft (LLM if available, else a template) for admin review."""
    with db.conn() as c:
        n = c.execute("SELECT * FROM news WHERE id=?", (news_id,)).fetchone()
    if not n: raise KeyError("news not found")
    prompt = (f"Write ONE multiple-choice quiz question (4 options, one correct, a playful one-sentence 'why') about this AI news item. "
              f"Return JSON only: {{\"topic\": <one of ai-basics|genai|llms|tokens-cost|prompt-engineering|rag|agents|mlops|ai-ethics>, "
              f"\"d\": 1|2|3, \"q\": str, \"options\": [4 str], \"answer\": int, \"why\": str, \"tags\": [str]}}\n\nTitle: {n['title']}\nSummary: {n['summary']}")
    text = llm.complete(prompt, max_tokens=500)
    q = None
    if text:
        try: q = json.loads(re.sub(r"```json|```", "", text).strip())
        except Exception: q = None
    if not q:
        q = {"topic": "genai", "d": 1, "q": f"What did {n['source']} announce in '{n['title'][:60]}'?", "options": ["(edit me)", "(edit me)", "(edit me)", "(edit me)"],
             "answer": 0, "why": "Draft from news — edit before approving.", "tags": ["news"]}
    with db.conn() as c:
        c.execute("INSERT INTO question_drafts (topic, question, status, source_url, created_at) VALUES (?,?,?,?,?)",
                  (q["topic"], json.dumps(q), "pending", n["url"], db.now()))
        did = c.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    return {"draft_id": did, "draft": q, "note": "Approve via /api/quest/admin/drafts/{id}/approve — it is appended to question_bank.yaml."}

def approve_draft(draft_id: int) -> dict:
    with db.conn() as c:
        d = c.execute("SELECT * FROM question_drafts WHERE id=?", (draft_id,)).fetchone()
        if not d: raise KeyError("draft not found")
        q = json.loads(d["question"])
        c.execute("UPDATE question_drafts SET status='approved' WHERE id=?", (draft_id,))
    path = HERE / "question_bank.yaml"; bank = yaml.safe_load(path.read_text())
    topic = next(t for t in bank["topics"] if t["id"] == q["topic"])
    topic["questions"].append({k: q[k] for k in ["d", "q", "options", "answer", "why", "tags"]})
    path.write_text(yaml.safe_dump(bank, sort_keys=False, allow_unicode=True, width=200))
    return {"draft_id": draft_id, "appended_to": q["topic"], "bank_questions": sum(len(t["questions"]) for t in bank["topics"])}
