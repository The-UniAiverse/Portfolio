"""Training & Mentorship — serves the versioned curriculum (training-materials/curriculum.yaml)."""
from __future__ import annotations
from datetime import date
import yaml
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings

router = APIRouter()
CUR = settings.materials_dir / "curriculum.yaml"

def _cur() -> dict:
    return yaml.safe_load(CUR.read_text())

def _stale(c: dict) -> bool:
    try:
        y, m, _ = (int(x) for x in c["last_reviewed"].split("-"))
        return (date.today().year - y) * 12 + (date.today().month - m) >= 6
    except Exception:
        return True

def _outline(c: dict) -> str:
    L = [f"# {c['title']}", f"*v{c['version']} · level {c['level']} · {c['hours']}h · {', '.join(c['formats'])} · owner {c['owner']} · reviewed {c['last_reviewed']}*", "",
         f"**Audience:** {c['audience']}", f"**Prerequisites:** {', '.join(c['prerequisites']) or 'none'}", f"**Certification:** {c['certification']}", "",
         "## Learning outcomes"] + [f"- {o}" for o in c["outcomes"]] + ["", "## Modules", "", "| # | Module | Hours | Topics | Lab |", "|---|---|---|---|---|"]
    for i, m in enumerate(c["modules"], 1):
        L.append(f"| {i} | {m['title']} | {m['hours']} | {', '.join(m['topics'])} | {m.get('lab') or '—'} |")
    L += ["", f"## Assessment", str(c["assessment"]), "", "*uniAIverse Academy — curriculum framework v" + _cur()["version"] + "*"]
    return "\n".join(L)

@router.get("/curriculum")
def curriculum():
    """Full framework: governance, tracks, courses (with staleness flags), certifications, emerging topics."""
    cur = _cur()
    for c in cur["courses"]:
        c["stale"] = _stale(c); c["module_count"] = len(c["modules"])
    cur["summary"] = {"courses": len(cur["courses"]), "tracks": len(cur["tracks"]),
                      "total_hours": sum(c["hours"] for c in cur["courses"]),
                      "stale_courses": [c["id"] for c in cur["courses"] if c["stale"]]}
    return cur

@router.get("/tracks")
def tracks():
    cur = _cur(); by_id = {c["id"]: c for c in cur["courses"]}
    return [{**t, "hours": sum(by_id[i]["hours"] for i in t["courses"] if i in by_id),
             "courses_detail": [{"id": i, "title": by_id[i]["title"], "hours": by_id[i]["hours"], "level": by_id[i]["level"]} for i in t["courses"] if i in by_id]}
            for t in cur["tracks"]]

@router.get("/course/{course_id}")
def course(course_id: str):
    for c in _cur()["courses"]:
        if c["id"] == course_id:
            folder = settings.materials_dir / c["folder"]
            return {**c, "stale": _stale(c), "outline_markdown": _outline(c),
                    "materials": sorted(p.name for p in folder.iterdir()) if folder.exists() else []}
    raise HTTPException(404, "course not found")

@router.get("/course/{course_id}/file/{filename}")
def course_file(course_id: str, filename: str):
    for c in _cur()["courses"]:
        if c["id"] == course_id:
            p = (settings.materials_dir / c["folder"] / filename).resolve()
            if p.exists() and str(p).startswith(str(settings.materials_dir.resolve())):
                return FileResponse(p)
    raise HTTPException(404, "file not found")

@router.get("/by-tier/{tier}")
def by_tier(tier: str):
    """Which courses a service tier includes (bronze/silver/gold/platinum)."""
    cs = [c for c in _cur()["courses"] if tier in c["tiers"]]
    if not cs:
        raise HTTPException(404, "unknown tier or no courses")
    return {"tier": tier, "courses": [{"id": c["id"], "title": c["title"], "hours": c["hours"], "level": c["level"]} for c in cs],
            "total_hours": sum(c["hours"] for c in cs)}

@router.post("/recommend")
def recommend_path(track: str, goal: str = ""):
    cur = _cur(); t = next((x for x in cur["tracks"] if x["id"] == track), None)
    if not t:
        raise HTTPException(400, f"track must be one of {[x['id'] for x in cur['tracks']]}")
    by_id = {c["id"]: c for c in cur["courses"]}
    return {"track": t, "goal": goal, "path": [{"id": i, "title": by_id[i]["title"], "hours": by_id[i]["hours"], "certification": by_id[i]["certification"]} for i in t["courses"]]}

from .course_finder import Profile, find

@router.post("/course-finder")
def course_finder(profile: Profile):
    """Profile / CV → recommended track and first course (free) or full personalised path (paid)."""
    return find(profile)

@router.get("/course-finder/sample")
def course_finder_sample(kind: str = "developer"):
    samples = {
        "developer": Profile(name="Riya", current_role="Backend developer", education="B.Tech CS", years_experience=3,
                             programming=["python", "javascript"], tech_stack=["fastapi", "postgres", "aws"],
                             interests=["build chatbots", "rag"], goal="Become a GenAI engineer and build LLM apps", hours_per_week=6),
        "student": Profile(name="Arjun", current_role="Final year student", education="BSc Computer Science", years_experience=0,
                           programming=["python"], tech_stack=[], interests=["ai", "getting a job"], goal="First AI job in 12 months", hours_per_week=10),
        "analyst": Profile(name="Meera", current_role="Business analyst", education="MBA", years_experience=5,
                           programming=[], tech_stack=["excel", "power bi"], interests=["lead AI projects"], goal="Own AI initiatives in my company", hours_per_week=4),
        "leader": Profile(name="Vikram", current_role="Head of Operations", education="MBA", years_experience=14,
                          programming=[], tech_stack=[], interests=["strategy"], goal="Decide where to invest in AI", hours_per_week=2),
        "compliance": Profile(name="Sana", current_role="Compliance manager", education="LLB", years_experience=7,
                              programming=[], tech_stack=[], interests=["governance", "risk"], goal="Become the AI governance lead", hours_per_week=4),
    }
    return samples.get(kind, samples["developer"]).model_dump()
