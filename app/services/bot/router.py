"""uniAI — website assistant. Rule-based intent matching over knowledge.yaml (works with no API key);
an LLM, if configured, rephrases within the same facts. Logs unanswered questions so the knowledge base grows."""
from __future__ import annotations
import re, uuid
from pathlib import Path
import yaml
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from app.core import db, llm
from app.core.config import settings

router = APIRouter()
KB = Path(__file__).with_name("knowledge.yaml")

def _kb() -> dict:
    return yaml.safe_load(KB.read_text())

def _fmt(s: str, kb: dict) -> str:
    b = kb["bot"]
    return (s.replace("{site}", settings.site_url).replace("{api}", settings.public_url)
             .replace("{calendly}", b["calendly_url"]).replace("{contact_email}", b["contact_email"]))

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower())

def match(question: str, kb: dict) -> tuple[dict | None, float]:
    q = _norm(question); best, score = None, 0.0
    for it in kb["intents"]:
        s = 0.0
        for t in it["triggers"]:
            t = _norm(t).strip()
            if not t: continue
            if f" {t} " in f" {q} ": s += 2 + len(t.split()) * 0.5      # phrase hit
            else:
                words = t.split()
                hits = sum(1 for w in words if len(w) > 3 and f" {w} " in f" {q} ")
                if hits and hits == len(words): s += 1.0
                elif hits: s += 0.4 * hits
        if s > score: best, score = it, s
    return best, score

class Chat(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    session: str | None = None

@router.get("/config")
def config():
    kb = _kb(); b = kb["bot"]
    return {"name": b["name"], "greeting": _fmt(b["greeting"], kb), "quick_replies": b["quick_replies"],
            "chatgpt_url": b.get("chatgpt_url") or None, "intents": [i["id"] for i in kb["intents"]]}

@router.post("/chat")
def chat(c: Chat):
    kb = _kb(); b = kb["bot"]; session = c.session or uuid.uuid4().hex[:10]
    it, score = match(c.message, kb)
    answered = it is not None and score >= 1.0
    if answered:
        text = _fmt(it["answer"], kb)
        polished = llm.complete(
            f"Rephrase this answer to the user's question in 2-3 friendly sentences. Keep every fact, number and name exactly; add nothing.\n"
            f"Question: {c.message}\nAnswer: {text}", max_tokens=250)
        reply = {"intent": it["id"], "text": (polished or text).strip(),
                 "link": {"label": it["link"]["label"], "url": _fmt(it["link"]["url"], kb)} if it.get("link") else None,
                 "quick_replies": it.get("quick_replies", b["quick_replies"][:3])}
    else:
        reply = {"intent": None, "text": _fmt(b["fallback"], kb), "link": {"label": "Book a call", "url": b["calendly_url"]},
                 "quick_replies": b["quick_replies"], "fallback_llm": False}
        if llm.available() and "platform" in settings.enabled_services:                     # v2.8: metered live fallback, capped by the free pool
            from app.services.platform import engine as _pe, gateway as _gw
            pool = _pe.check(None, "bot")
            if pool["allowed"]:
                ctx = "\n".join(f"- {_fmt(i['answer'], kb)}" for i in kb["intents"][:20])
                r = llm.complete_with_usage(f"You are uniAI, the uniAIverse website assistant. Answer in 2 sentences from these facts only; if the facts do not cover it, say so and suggest booking a call.\nFACTS:\n{ctx}\nQUESTION: {c.message}", max_tokens=150)
                if r:
                    cost = _gw._price("cheap", r["tokens_in"], r["tokens_out"]); _gw._record("public", "widget", r["provider"], r["model"], "cheap", r["tokens_in"], r["tokens_out"], cost, 0, "ok", "", "bot-fallback")
                    reply.update({"text": r["text"].strip(), "fallback_llm": True})
    with db.conn() as conn:
        conn.execute("INSERT INTO bot_log (session, question, intent, answered, created_at) VALUES (?,?,?,?,?)",
                     (session, c.message[:500], reply["intent"], int(answered), db.now()))
    return {"session": session, "bot": b["name"], **reply, "confidence": round(score, 2)}

@router.get("/admin/unanswered")
def unanswered(limit: int = 50, x_admin_token: str | None = Header(None)):
    """What people asked that uniAI couldn't answer — the to-do list for knowledge.yaml."""
    if not settings.admin_token or x_admin_token != settings.admin_token: raise HTTPException(401, "admin token required")
    with db.conn() as c:
        rows = c.execute("SELECT question, COUNT(*) n FROM bot_log WHERE answered=0 GROUP BY question ORDER BY n DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]
