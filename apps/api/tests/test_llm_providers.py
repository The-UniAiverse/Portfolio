"""Provider selection and fallback. The OpenAI client is faked; no network calls."""
import pytest
from app.core import llm
from app.core.config import settings


class FakeOpenAI:
    calls: list = []
    fail_for: set = set()

    def __init__(self, api_key, base_url=None, timeout=None):
        self.base_url = base_url
        self.chat = self
        self.completions = self

    def create(self, model, max_tokens, messages):
        FakeOpenAI.calls.append((self.base_url, model, max_tokens))
        if self.base_url in FakeOpenAI.fail_for:
            raise RuntimeError("provider down")
        msg = type("M", (), {"content": f"hello from {model}"})
        return type("R", (), {"choices": [type("C", (), {"message": msg})]})


@pytest.fixture
def providers(monkeypatch):
    import openai
    monkeypatch.setattr(openai, "OpenAI", FakeOpenAI)
    FakeOpenAI.calls, FakeOpenAI.fail_for = [], set()
    for k, v in {"llm_provider": "gemini", "llm_fallback_provider": "deepseek", "gemini_key": "g-test",
                 "deepseek_key": "d-test", "gemini_model": "gemini-x", "deepseek_model": "deepseek-chat"}.items():
        monkeypatch.setattr(settings, k, v)


def test_primary_provider_used(providers):
    assert llm.providers() == ["gemini", "deepseek"]
    assert llm.complete("hi", max_tokens=100) == "hello from gemini-x"
    base, model, max_tokens = FakeOpenAI.calls[0]
    assert "generativelanguage.googleapis.com" in base and max_tokens == 100 + llm.EXTRA_OUTPUT_TOKENS["gemini"]


def test_falls_back_to_deepseek_when_gemini_fails(providers):
    FakeOpenAI.fail_for = {llm.OPENAI_COMPATIBLE["gemini"]()[0]}
    assert llm.complete("hi") == "hello from deepseek-chat"
    assert FakeOpenAI.calls[-1][0] == "https://api.deepseek.com"


def test_missing_key_skips_provider(providers, monkeypatch):
    monkeypatch.setattr(settings, "gemini_key", None)
    assert llm.providers() == ["deepseek"] and llm.available()
    monkeypatch.setattr(settings, "deepseek_key", None)
    assert not llm.available() and llm.complete("hi") is None
