"""AI Job Finder — job search, fit scoring and cover letters on top of the vendored
ai-job-search project (see vendor/README.md). Jobs come from freehire.me; every posting
returned links back to freehire, as its data licence requires."""
from __future__ import annotations
import re
import time
import uuid
from threading import Lock
from typing import Literal
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from app.core import llm
from app.core.config import settings
from app.core.auth import require_user
from . import cover_letter, matching, pdf, upstream
from .schemas import SLUG, CoverLetterRequest, LetterPdfRequest, MatchRequest

router = APIRouter()
OUT = settings.outputs_dir / "jobs"
OUT.mkdir(parents=True, exist_ok=True)
PDF_NAME = re.compile(r"^(?P<id>[0-9a-f]{32})\.pdf$")
ATTRIBUTION = {"source": "freehire.me", "url": "https://freehire.me",
               "note": "Job listings via freehire.me. Each listing links to its freehire page."}
# Filter value -> freehire seniority facet values.
LEVELS = {"any": [], "entry": ["intern", "junior"], "intern": ["intern"], "junior": ["junior"], "mid": ["middle"],
          "senior": ["senior"], "lead": ["lead", "staff", "principal"], "executive": ["c_level"]}

# Small TTL cache: identical searches and job lookups within a few minutes reuse the result.
_CACHE: dict[tuple, tuple[float, dict]] = {}
_LOCK = Lock()
TTL = 300


def _cached(key: tuple, fn):
    now = time.monotonic()
    with _LOCK:
        hit = _CACHE.get(key)
        if hit and now - hit[0] < TTL:
            return hit[1]
    value = fn()
    with _LOCK:
        if len(_CACHE) > 500:
            _CACHE.clear()
        _CACHE[key] = (now, value)
    return value


def _freehire_url(slug: str) -> str:
    return f"https://freehire.me/jobs/{slug}"


def _card(r: dict) -> dict:
    return {"id": r["id"], "title": r["title"], "company": r.get("company"), "location": r.get("location"),
            "date": r.get("date"), "work_mode": r.get("work_mode"), "skills": r.get("skills") or [],
            "apply_url": r.get("url"), "freehire_url": _freehire_url(r["id"])}


def _job(slug: str) -> tuple[dict, str, str]:
    """The job, its guarded description and the guard verdict line."""
    job = _cached(("detail", slug), lambda: upstream.detail(slug))
    clean, findings = upstream.guard(job.get("description") or "")
    return job, clean, findings.get("verdict", "")


@router.get("/search")
def search(
    q: str = Query("", max_length=100),
    city: str = Query("", max_length=60),
    level: Literal["any", "entry", "intern", "junior", "mid", "senior", "lead", "executive"] = "any",
    work_mode: Literal["", "remote", "hybrid", "onsite"] = "",
    posted_within_days: int = Query(0, ge=0, le=30),  # query strings arrive as text, so not a Literal[int]
    page: int = Query(1, ge=1, le=50),
):
    """Search open jobs in India (freehire.me via upstream's connector). No AI involved."""
    if posted_within_days not in {0, 1, 7, 14, 30}:
        raise HTTPException(422, "posted_within_days must be 0, 1, 7, 14 or 30")
    args = dict(query=q, city=city, seniority=LEVELS[level], work_mode=work_mode,
                posted_within_days=posted_within_days, page=page)
    data = _cached(("search", q, city, level, work_mode, posted_within_days, page), lambda: upstream.search(**args))
    return {"total": data["meta"].get("total", 0), "page": page,
            "results": [_card(r) for r in data["results"]], "attribution": ATTRIBUTION}


@router.get("/job/{slug}")
def job(slug: str):
    if not re.fullmatch(SLUG, slug):
        raise HTTPException(404, {"code": "job_not_found", "message": "This job is no longer available."})
    j, clean, verdict = _job(slug)
    return {**_card(j), "description": clean, "cities": j.get("cities") or [], "seniority": j.get("seniority"),
            "category": j.get("category"), "employment_type": j.get("employment_type"), "salary": j.get("salary"),
            "guard": verdict, "attribution": ATTRIBUTION}


@router.post("/match", dependencies=[Depends(require_user)])
def match(req: MatchRequest):
    use_ai = llm.use_ai(req.mode)  # 503 ai_unavailable if AI was required but not configured
    j, clean, verdict = _job(req.job_id)
    result, notice = None, None
    if use_ai:
        result = matching.ai_match(req.profile, j, clean)
        if result is None:
            notice = llm.AI_FALLBACK_NOTICE
    result = result or matching.rules_match(req.profile, j)
    return {**result, "notice": notice, "guard": verdict, "job_id": req.job_id, "mode": req.mode}


def _save_pdf(req_profile, letter) -> tuple[str, int]:
    file_id = uuid.uuid4().hex
    pages = pdf.render(req_profile, letter, OUT / f"{file_id}.pdf")
    return f"/api/jobs/file/{file_id}.pdf", pages


@router.post("/cover-letter", dependencies=[Depends(require_user)])
def make_cover_letter(req: CoverLetterRequest):
    llm.use_ai("ai")  # a cover letter is AI-only: 503 ai_unavailable when no provider is configured
    j, clean, verdict = _job(req.job_id)
    out = cover_letter.generate(req.profile, j, clean, req.notes.strip())
    if out is None:
        raise HTTPException(502, {"code": "ai_failed", "message": "We couldn't write the letter just now. Please try again."})
    letter, stretches = out
    url, pages = _save_pdf(req.profile, letter)
    return {"letter": letter.model_dump(), "review_notes": stretches, "word_count": cover_letter.word_count(letter),
            "pages": pages, "pdf_url": url, "guard": verdict, "job_id": req.job_id}


@router.post("/cover-letter/pdf", dependencies=[Depends(require_user)])
def cover_letter_pdf(req: LetterPdfRequest):
    """Render a letter the candidate edited. No AI involved."""
    url, pages = _save_pdf(req.profile, req.letter)
    return {"pdf_url": url, "pages": pages, "word_count": cover_letter.word_count(req.letter)}


@router.get("/file/{filename}")
def get_file(filename: str):
    # 128-bit random ids act as the access capability (no accounts yet), as for audit reports.
    m = PDF_NAME.match(filename)
    p = OUT / filename if m else None
    if not m or not p.is_file():
        raise HTTPException(404, "file not found or expired")
    return FileResponse(p, media_type="application/pdf", filename=f"cover-letter-{m['id'][:8]}.pdf",
                        headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"})
