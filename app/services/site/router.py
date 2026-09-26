"""Public site service (v2.8): services and success stories, demo showcase and playground with a freemium gate, AI engineering news with
daily top-5 summaries, newsletter (subscribe, confirm, unsubscribe, compose, send — dry-run without an email provider), chat widget fallback."""
from __future__ import annotations
import datetime as dt, hashlib, html, re, secrets, uuid
from pathlib import Path
import yaml
from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from app.core import db, llm
from app.core.config import settings
from app.services.quest import news as newsmod

router = APIRouter(); HERE = Path(__file__).parent
def content() -> dict: return yaml.safe_load((HERE / "content.yaml").read_text())
def _admin(t):
    if not settings.admin_token or t != settings.admin_token: raise HTTPException(401, "admin token required")
def _today(): return dt.date.today().isoformat()

# ── services + stories ────────────────────────────────────────────────────────────────────────────────────────────────
def _prices():
    try: return yaml.safe_load((settings.materials_dir.parent / "pricing/tiers.yaml").read_text())["services"]
    except Exception: return {}
@router.get("/services")
def services():
    P = _prices(); C = content(); out = []
    for s in C["services"]:
        tiers = (P.get(s["pricing_service"]) or {}).get("tiers", {}); out.append({**s, "tiers": {k: {"price_usd": v.get("price_usd"), "price_inr": v.get("price_inr"), "duration": v.get("duration")} for k, v in tiers.items()} if isinstance(tiers, dict) else {}, "story_count": len(s.get("stories", []))})
    return {"services": out, "version": C["version"]}
@router.get("/services/{sid}")
def service(sid: str):
    C = content(); s = next((x for x in C["services"] if x["id"] == sid), None)
    if not s: raise HTTPException(404, "service not found")
    P = _prices(); return {**s, "tiers": (P.get(s["pricing_service"]) or {}).get("tiers", {}), "stories": [x for x in C["stories"] if x["id"] in s.get("stories", [])]}
@router.get("/stories")
def stories(): return {"stories": content()["stories"], "note": "Entries marked 'illustrative' are placeholders until real case studies replace them."}
@router.get("/showcase")
def showcase(): return {"items": content()["showcase"]}

# ── playground (freemium gate) ────────────────────────────────────────────────────────────────────────────────────────
class PlayAsk(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
def _trial(client_id: str) -> tuple[int, int]:
    cap = int(content()["playground"]["trial_questions_per_day"])
    with db.conn() as c:
        r = c.execute("SELECT n FROM playground_usage WHERE client_id=? AND day=?", (client_id, _today())).fetchone(); n = r["n"] if r else 0
    return n, cap
@router.get("/playground/status")
def playground_status(x_playground_id: str | None = Header(None)):
    cid = x_playground_id or "anon"; n, cap = _trial(cid); C = content()["playground"]
    return {"client_id": cid, "used_today": n, "remaining_today": max(0, cap - n), "cap": cap, "upgrade_url": C["upgrade_url"], "note": C["note"]}
@router.post("/playground/ask")
def playground_ask(a: PlayAsk, x_playground_id: str | None = Header(None)):
    """Anonymous trial: N questions a day per browser, answered by the advanced RAG demo on sample documents; then an upgrade prompt."""
    from app.services.platform import engine as pe
    cid = x_playground_id or "anon"; n, cap = _trial(cid); C = content()["playground"]
    if n >= cap: raise HTTPException(402, f"Trial limit of {cap} questions a day reached. Request access at {C['upgrade_url']} for your own documents and quotas.")
    pool = pe.check(None, "demo.rag_preloaded")
    if not pool["allowed"]: raise HTTPException(402, pool["reason"])
    from app.services.demos.router import rag_ask, Ask
    r = rag_ask(Ask(question=a.question)); adv = r.get("advanced", r)
    with db.conn() as c: c.execute("INSERT INTO playground_usage (client_id, day, n) VALUES (?,?,1) ON CONFLICT(client_id, day) DO UPDATE SET n=n+1", (cid, _today()))
    return {"answer": adv.get("answer"), "sources": adv.get("sources", adv.get("hits", [])), "tokens": adv.get("tokens"), "used_today": n + 1, "remaining_today": cap - n - 1, "upgrade_url": C["upgrade_url"], "upgrade_prompt": (cap - n - 1) <= 1}

# ── news: daily top-5 with summaries ──────────────────────────────────────────────────────────────────────────────────
def _summarise(title: str, summary: str) -> str:
    s = re.sub(r"<[^>]+>", " ", summary or ""); s = re.sub(r"\s+", " ", s).strip()
    out = llm.complete(f"Summarise for AI engineers in two plain sentences (max 45 words), no hype, keep numbers exact:\nTitle: {title}\nText: {s[:1500]}", max_tokens=90) if llm.available() else None
    return (out or ". ".join([x for x in re.split(r"(?<=[.!?])\s+", s) if x][:2]) or title).strip()[:400]
def top5(day: str | None = None) -> list[dict]:
    C = content()["newsletter"]; items = newsmod.queue("approved", 40); day = day or _today()
    todays = [i for i in items if str(i.get("published", ""))[:10] == day] or items
    ranked = sorted(todays, key=lambda i: (-(len(i.get("tags") or [])), i.get("published") or ""), reverse=False)[: C["top_n"]]
    return [{"title": i["title"], "url": i["url"], "source": i["source"], "published": i["published"], "summary": _summarise(i["title"], i.get("summary", "")), "tags": i.get("tags", [])} for i in ranked]
@router.get("/news")
def news(day: str | None = None): return {"day": day or _today(), "items": top5(day), "name": content()["newsletter"]["name"]}

# ── newsletter ────────────────────────────────────────────────────────────────────────────────────────────────────────
class Subscribe(BaseModel):
    email: EmailStr; name: str = ""
@router.post("/newsletter/subscribe")
def subscribe(s: Subscribe):
    """Double opt-in: creates a pending record and a confirm token. The confirm email is sent by the send job (dry-run without a provider)."""
    tok = secrets.token_urlsafe(16)
    with db.conn() as c: c.execute("INSERT INTO newsletter_subscribers (email, name, token, status, created_at) VALUES (?,?,?,?,?) ON CONFLICT(email) DO UPDATE SET status=CASE WHEN status='unsubscribed' THEN 'pending' ELSE status END, token=excluded.token", (s.email.lower(), s.name, tok, "pending", db.now()))
    return {"status": "pending", "confirm_url": f"{settings.public_url}/api/site/newsletter/confirm?token={tok}", "note": "Confirm link is emailed once an email provider is configured; until then it is returned here for testing."}
@router.get("/newsletter/confirm")
def confirm(token: str):
    with db.conn() as c:
        r = c.execute("SELECT email FROM newsletter_subscribers WHERE token=?", (token,)).fetchone()
        if not r: raise HTTPException(404, "unknown or used token")
        c.execute("UPDATE newsletter_subscribers SET status='confirmed', confirmed_at=? WHERE token=?", (db.now(), token))
    return {"status": "confirmed", "email": r["email"]}
@router.get("/newsletter/unsubscribe")
def unsubscribe(token: str):
    with db.conn() as c:
        r = c.execute("SELECT email FROM newsletter_subscribers WHERE token=?", (token,)).fetchone()
        if not r: raise HTTPException(404, "unknown token")
        c.execute("UPDATE newsletter_subscribers SET status='unsubscribed', unsubscribed_at=? WHERE token=?", (db.now(), token))
    return {"status": "unsubscribed"}
def _issue(day: str) -> dict:
    C = content()["newsletter"]; items = top5(day)
    subject = f"{C['name']} — {day}: " + (items[0]["title"][:60] if items else "no items today")
    text = "\n\n".join(f"{i + 1}. {x['title']} ({x['source']})\n{x['summary']}\n{x['url']}" for i, x in enumerate(items)) or "No approved items today."
    body = "".join(f"<h3 style='margin:14px 0 4px'>{i + 1}. <a href='{html.escape(x['url'])}'>{html.escape(x['title'])}</a> <small>{html.escape(x['source'])}</small></h3><p>{html.escape(x['summary'])}</p>" for i, x in enumerate(items))
    htmlb = f"<div style='font-family:Inter,Arial,sans-serif;max-width:640px;margin:auto'><h2>{html.escape(C['name'])}</h2><p style='color:#64748b'>{day} · the five things worth an engineer's morning</p>{body or '<p>No approved items today.</p>'}<p style='color:#64748b;font-size:12px'>You receive this because you subscribed. <a href='{{unsubscribe_url}}'>Unsubscribe</a>.</p></div>"
    script = f"Good morning. This is {C['name']} for {day}. " + " ".join(f"Number {i + 1}. {x['title']}. {x['summary']}" for i, x in enumerate(items)) + " That is all for today."
    return {"day": day, "subject": subject, "html": htmlb, "text": text, "script": script, "items": len(items)}
@router.post("/newsletter/compose")
def compose(day: str | None = None, x_admin_token: str | None = Header(None)):
    """Builds today's issue (HTML, text and the voice script) from the top-5 and stores it. Idempotent per day."""
    _admin(x_admin_token); iss = _issue(day or _today())
    with db.conn() as c: c.execute("INSERT INTO newsletter_issues (day, subject, html, text, script, items, sent_to, status, created_at) VALUES (?,?,?,?,?,?,0,'draft',?) ON CONFLICT(day) DO UPDATE SET subject=excluded.subject, html=excluded.html, text=excluded.text, script=excluded.script, items=excluded.items", (iss["day"], iss["subject"], iss["html"], iss["text"], iss["script"], iss["items"], db.now()))
    return {**iss, "html": iss["html"][:400] + "…", "status": "draft"}
def _send_email(to: str, subject: str, htmlb: str) -> str:
    key = getattr(settings, "resend_api_key", None) or __import__("os").getenv("RESEND_API_KEY")
    if not key: return "dry-run"
    import httpx
    r = httpx.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {key}"}, json={"from": content()["newsletter"]["from"], "to": [to], "subject": subject, "html": htmlb}, timeout=15)
    return "sent" if r.status_code < 300 else f"error {r.status_code}"
@router.post("/newsletter/send")
def send(day: str | None = None, x_admin_token: str | None = Header(None)):
    """Sends the day's issue to confirmed subscribers, and confirm links to pending ones. Without RESEND_API_KEY every send is a dry-run (counted, not delivered)."""
    _admin(x_admin_token); day = day or _today()
    with db.conn() as c:
        iss = c.execute("SELECT * FROM newsletter_issues WHERE day=?", (day,)).fetchone()
        if not iss: raise HTTPException(404, "compose the issue first")
        subs = [dict(r) for r in c.execute("SELECT email, token, status FROM newsletter_subscribers WHERE status IN ('confirmed','pending')").fetchall()]
    results = {"sent": 0, "confirm_links": 0, "dry_run": 0, "errors": 0}
    for s in subs:
        if s["status"] == "pending": r = _send_email(s["email"], "Confirm your subscription", f"<p>Confirm: <a href='{settings.public_url}/api/site/newsletter/confirm?token={s['token']}'>click here</a></p>"); results["confirm_links"] += 1
        else: r = _send_email(s["email"], iss["subject"], iss["html"].replace("{unsubscribe_url}", f"{settings.public_url}/api/site/newsletter/unsubscribe?token={s['token']}"))
        results["dry_run" if r == "dry-run" else "sent" if r == "sent" else "errors"] += 1
    with db.conn() as c: c.execute("UPDATE newsletter_issues SET sent_to=?, status=?, sent_at=? WHERE day=?", (results["sent"] + results["dry_run"], "dry-run" if results["dry_run"] else "sent", db.now(), day))
    return {"day": day, **results, "provider": "resend" if results["sent"] or results["errors"] else "none (dry-run)"}
@router.get("/newsletter/voice")
def voice(day: str | None = None, x_admin_token: str | None = Header(None)):
    """Voice edition: returns the read-aloud script; audio is produced when a TTS provider key is configured (not yet — dry-run)."""
    _admin(x_admin_token); day = day or _today()
    with db.conn() as c: iss = c.execute("SELECT script, subject FROM newsletter_issues WHERE day=?", (day,)).fetchone()
    if not iss: raise HTTPException(404, "compose the issue first")
    return {"day": day, "subject": iss["subject"], "script": iss["script"], "audio": None, "status": "dry-run: add a TTS provider key to produce audio"}
@router.get("/newsletter/subscribers")
def subscribers(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    with db.conn() as c: return {"by_status": {r["status"]: r["n"] for r in c.execute("SELECT status, COUNT(*) n FROM newsletter_subscribers GROUP BY status").fetchall()}, "issues": [dict(r) for r in c.execute("SELECT day, subject, items, sent_to, status FROM newsletter_issues ORDER BY day DESC LIMIT 30").fetchall()]}
