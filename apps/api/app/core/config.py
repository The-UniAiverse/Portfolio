"""Central settings. Everything is read from environment (.env) so nothing is hard-coded."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

def _list(name: str, default: str) -> list[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]

class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    port: int = int(os.getenv("APP_PORT", "8000"))
    cors_origins: list[str] = _list("CORS_ORIGINS", "http://localhost:3000")
    enabled_services: list[str] = _list(
        "ENABLED_SERVICES", "readiness_audit,training,strategy,governance,automation,pricing,jobs"
    )
    llm_provider: str = os.getenv("LLM_PROVIDER", "none").lower()
    llm_model: str = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
    anthropic_key: str | None = os.getenv("ANTHROPIC_API_KEY") or None
    openai_key: str | None = os.getenv("OPENAI_API_KEY") or None
    gemini_key: str | None = os.getenv("GEMINI_API_KEY") or None
    deepseek_key: str | None = os.getenv("DEEPSEEK_API_KEY") or None
    # Optional second provider, tried when the primary one fails (see app/core/llm.py).
    llm_fallback_provider: str = os.getenv("LLM_FALLBACK_PROVIDER", "none").lower()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    outputs_dir: Path = ROOT / "outputs"
    materials_dir: Path = ROOT / "training-materials"
    pricing_dir: Path = ROOT / "pricing"
    # Max POST requests per client IP per minute on /api/* (0 disables). See app/core/ratelimit.py.
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "30"))
    # Only enable behind a trusted reverse proxy that sets X-Forwarded-For.
    trust_proxy_headers: bool = os.getenv("TRUST_PROXY_HEADERS", "false").lower() in {"1", "true", "yes"}
    # Sign-in for AI tools (app/core/auth.py). Tokens are issued by the website (Better Auth JWT plugin).
    auth_required: bool = os.getenv("AUTH_REQUIRED", "true").lower() in {"1", "true", "yes"}
    auth_jwks_url: str = os.getenv("AUTH_JWKS_URL", "http://localhost:3000/api/auth/jwks")
    # Better Auth sets both claims to the website's BETTER_AUTH_URL.
    auth_issuer: str = os.getenv("AUTH_ISSUER", "http://localhost:3000")
    auth_audience: str = os.getenv("AUTH_AUDIENCE", "http://localhost:3000")

settings = Settings()
settings.outputs_dir.mkdir(exist_ok=True)
