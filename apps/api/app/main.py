import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .core.config import settings, ROOT
from .core import registry, llm
from .core.ratelimit import RateLimitMiddleware, SlidingWindowLimiter

log = logging.getLogger("uniaiverse.api")

app = FastAPI(
    title="uniAIverse AI Services API",
    version="0.2.0",
    description="Backend for AI Readiness Audit, Training, Strategy, Governance and Automation services.",
)

limiter = SlidingWindowLimiter(settings.rate_limit_per_minute)
app.add_middleware(RateLimitMiddleware, limiter=limiter, trust_proxy=settings.trust_proxy_headers)
# CORS is added last so it wraps everything (429 responses also carry CORS headers).
app.add_middleware(
    CORSMiddleware, allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"],
)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    # Never leak stack traces or internals to clients; log server-side only.
    log.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": {"code": "internal_error",
                                                             "message": "Something went wrong on our side. Please try again."}})


LOADED = []
for spec, router in registry.load(settings.enabled_services):
    app.include_router(router, prefix=f"/api/{spec.id}", tags=[spec.title])
    LOADED.append(spec)

@app.get("/api/health")
def health():
    return {"ok": True, "env": settings.app_env, "llm": settings.llm_provider,
            # Whether AI-enhanced mode can run on this server (provider + key present). Never exposes keys.
            "ai_enhanced_available": llm.available(),
            "services": [{"id": s.id, "title": s.title, "priority": s.priority, "status": s.status} for s in LOADED]}

# Demo UI (static, no build step). Your Next.js site can call the same /api routes.
UI = ROOT / "ui"
app.mount("/static", StaticFiles(directory=UI), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(UI / "index.html")
