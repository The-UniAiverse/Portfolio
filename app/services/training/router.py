"""Training & Mentorship — serves the course catalogue and materials from training-materials/."""
from __future__ import annotations
import yaml
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings

router = APIRouter()
CAT = settings.materials_dir / "catalog.yaml"

def _catalog() -> dict:
    return yaml.safe_load(CAT.read_text())

@router.get("/catalog")
def catalog():
    return _catalog()

@router.get("/course/{course_id}")
def course(course_id: str):
    for c in _catalog()["courses"]:
        if c["id"] == course_id:
            md = settings.materials_dir / c["folder"] / "COURSE.md"
            return {**c, "outline_markdown": md.read_text() if md.exists() else None}
    raise HTTPException(404, "course not found")

@router.get("/course/{course_id}/file/{filename}")
def course_file(course_id: str, filename: str):
    for c in _catalog()["courses"]:
        if c["id"] == course_id:
            p = settings.materials_dir / c["folder"] / filename
            if p.exists() and ".." not in filename:
                return FileResponse(p)
    raise HTTPException(404, "file not found")

@router.post("/recommend")
def recommend_path(audience: str, goal: str = ""):
    """Map an audience (business / engineer / genai_engineer / sales / marketing / leadership) to a learning path."""
    paths = _catalog()["learning_paths"]
    if audience not in paths:
        raise HTTPException(400, f"audience must be one of {list(paths)}")
    return {"audience": audience, "goal": goal, "path": paths[audience]}
