import pytest
from app.core.config import settings


@pytest.fixture(autouse=True)
def no_real_ai_providers(monkeypatch):
    """Tests never call a real AI provider, whatever keys are in the local .env.
    Tests that need AI fake llm.available/llm.complete or set providers themselves."""
    monkeypatch.setattr(settings, "llm_provider", "none")
    monkeypatch.setattr(settings, "llm_fallback_provider", "none")


@pytest.fixture(autouse=True)
def sign_in_not_required(monkeypatch):
    """Feature tests run signed-out; tests/test_auth.py turns sign-in enforcement back on."""
    monkeypatch.setattr(settings, "auth_required", False)
