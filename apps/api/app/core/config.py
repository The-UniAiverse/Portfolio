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
        "ENABLED_SERVICES", "readiness_audit,training,strategy,governance,automation,pricing"
    )
    llm_provider: str = os.getenv("LLM_PROVIDER", "none").lower()
    llm_model: str = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
    anthropic_key: str | None = os.getenv("ANTHROPIC_API_KEY") or None
    openai_key: str | None = os.getenv("OPENAI_API_KEY") or None
    outputs_dir: Path = ROOT / "outputs"
    materials_dir: Path = ROOT / "training-materials"
    pricing_dir: Path = ROOT / "pricing"

settings = Settings()
settings.outputs_dir.mkdir(exist_ok=True)
