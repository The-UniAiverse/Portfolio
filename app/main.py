from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .core.config import settings, ROOT
from .core import registry

app = FastAPI(
    title="uniAIverse AI Services API",
    version="2.5.0",
    description="Backend for AI Readiness Audit, Training, Strategy, Governance and Automation services.",
)
app.add_middleware(
    CORSMiddleware, allow_origins=settings.cors_origins,
    allow_methods=["*"], allow_headers=["*"],
)

LOADED = []
for spec, router in registry.load(settings.enabled_services):
    app.include_router(router, prefix=f"/api/{spec.id}", tags=[spec.title])
    LOADED.append(spec)

@app.get("/api/health")
def health():
    return {"ok": True, "env": settings.app_env, "llm": settings.llm_provider,
            "services": [{"id": s.id, "title": s.title, "priority": s.priority, "status": s.status} for s in LOADED]}

# Demo UI (static, no build step). Your Next.js site can call the same /api routes.
UI = ROOT / "ui"
app.mount("/static", StaticFiles(directory=UI), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(UI / "index.html")

@app.get("/course-finder", include_in_schema=False)
def course_finder_page():
    return FileResponse(UI / "course-finder.html")

@app.get("/quest", include_in_schema=False)
def quest_page():
    return FileResponse(UI / "quest.html")

@app.get("/pay", include_in_schema=False)
def pay_page():
    return FileResponse(UI / "pay.html")

@app.get("/admin", include_in_schema=False)
def admin_page():
    return FileResponse(UI / "admin.html")

@app.get("/tools", include_in_schema=False)
def tools_page():
    return FileResponse(UI / "tools.html")

@app.get("/demos", include_in_schema=False)
def demos_page():
    return FileResponse(UI / "demos.html")

@app.get("/discovery", include_in_schema=False)
def discovery_page():
    return FileResponse(UI / "discovery.html")

@app.get("/delivery", include_in_schema=False)
def delivery_page():
    return FileResponse(UI / "delivery.html")
