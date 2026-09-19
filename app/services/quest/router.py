"""uniAI Quest — Your AI Interview Playground & Knowledge Hub."""
from __future__ import annotations
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from app.core import db
from app.core.config import settings
from . import engine, news

router = APIRouter()

def _admin(token: str | None):
    if not settings.admin_token or token != settings.admin_token:
        raise HTTPException(401, "admin token required (X-Admin-Token)")

@router.get("/tiers")
def tiers(): return engine.tiers()

@router.get("/topics")
def topics(user_id: str = "guest"): return {"tier": engine.tier_of(user_id), "topics": engine.topics_for(engine.tier_of(user_id))}

@router.get("/quiz")
def quiz(topic: str, user_id: str = "guest", n: int = 5, difficulty: int | None = None):
    try: return engine.build_quiz(user_id, topic, n, difficulty)
    except PermissionError as e: raise HTTPException(402, str(e))
    except KeyError as e: raise HTTPException(404, str(e))

class Submission(BaseModel):
    user_id: str = "guest"
    topic: str
    answers: dict[str, int] = Field(..., description="question_id -> option index")

@router.post("/quiz/submit")
def submit(s: Submission):
    try: return engine.grade(s.user_id, s.topic, s.answers)
    except KeyError as e: raise HTTPException(404, str(e))

@router.get("/challenges")
def challenges(user_id: str = "guest"): return engine.challenges(user_id)

class ChallengeSubmission(BaseModel):
    user_id: str; challenge_id: str; self_rating: int = Field(..., ge=1, le=5); notes: str = ""

@router.post("/challenges/submit")
def submit_challenge(s: ChallengeSubmission):
    try: return engine.submit_challenge(s.user_id, s.challenge_id, s.self_rating, s.notes)
    except PermissionError as e: raise HTTPException(402, str(e))
    except KeyError as e: raise HTTPException(404, str(e))

@router.get("/progress")
def progress(user_id: str = "guest"): return engine.progress(user_id)

@router.get("/news")
def news_feed(user_id: str = "guest", limit: int = 20): return {"tier": engine.tier_of(user_id), "items": news.public_feed(engine.tier_of(user_id), limit)}

class MentorRequest(BaseModel):
    user_id: str; topic: str; preferred_slots: list[str] = Field(..., description="e.g. ['Sat 15:00-16:00 IST']")

@router.post("/mentor/request")
def mentor_request(m: MentorRequest):
    ent = engine.entitlements(engine.tier_of(m.user_id))
    if ent["mentor_hours_per_month"] == 0:
        raise HTTPException(402, "Mentor sessions are part of Gold and Platinum.")
    with db.conn() as c:
        c.execute("INSERT INTO mentor_requests (user_id, tier, topic, preferred_slots, status, created_at) VALUES (?,?,?,?,?,?)",
                  (m.user_id, engine.tier_of(m.user_id), m.topic, "|".join(m.preferred_slots), "requested", db.now()))
    return {"status": "requested", "hours_available_per_month": ent["mentor_hours_per_month"], "note": "We confirm a mutually agreed slot by email within 48h."}

# ── Admin (X-Admin-Token) ────────────────────────────────────────────────────
@router.post("/admin/news/refresh")
def admin_refresh(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token); return news.refresh()

class ManualNews(BaseModel):
    title: str; url: str; summary: str = ""; source: str = "Admin"; tags: list[str] = []

@router.post("/admin/news")
def admin_add_news(n: ManualNews, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token); return news.add_manual(n.title, n.url, n.summary, n.source, n.tags)

@router.get("/admin/news/queue")
def admin_queue(status: str = "pending", x_admin_token: str | None = Header(None)):
    _admin(x_admin_token); return news.queue(status)

@router.post("/admin/news/{news_id}/{action}")
def admin_moderate(news_id: str, action: str, summary: str | None = None, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    if action not in {"approve", "reject"}: raise HTTPException(400, "action must be approve|reject")
    return news.moderate(news_id, action, summary)

@router.post("/admin/news/{news_id}/draft-question")
def admin_draft(news_id: str, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    try: return news.draft_question(news_id)
    except KeyError as e: raise HTTPException(404, str(e))

@router.get("/admin/drafts")
def admin_drafts(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    with db.conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM question_drafts WHERE status='pending' ORDER BY created_at DESC")]

@router.post("/admin/drafts/{draft_id}/approve")
def admin_approve_draft(draft_id: int, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    try: return news.approve_draft(draft_id)
    except KeyError as e: raise HTTPException(404, str(e))

@router.get("/admin/mentor-requests")
def admin_mentor(x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    with db.conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM mentor_requests ORDER BY created_at DESC")]

class TierSet(BaseModel):
    user_id: str; tier: str; email: str | None = None

@router.post("/admin/set-tier")
def admin_set_tier(t: TierSet, x_admin_token: str | None = Header(None)):
    _admin(x_admin_token)
    if t.tier not in engine.tiers()["tiers"]: raise HTTPException(400, "unknown tier")
    db.set_tier(t.user_id, t.tier, t.email); return {"user_id": t.user_id, "tier": t.tier}
