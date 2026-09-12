"""Provider-agnostic LLM helper.

Every service must work WITHOUT an LLM (rule-based path). The LLM only adds narrative
polish. Swap providers by changing LLM_PROVIDER in .env — no code changes.
"""
from __future__ import annotations
from .config import settings

SYSTEM = (
    "You are a senior AI strategy consultant at uniAIverse. Write concise, concrete, "
    "board-ready prose. No hype. Use the client's numbers. Never invent facts not in the input."
)

def available() -> bool:
    if settings.llm_provider == "anthropic":
        return bool(settings.anthropic_key)
    if settings.llm_provider == "openai":
        return bool(settings.openai_key)
    return False

def complete(prompt: str, max_tokens: int = 1200) -> str | None:
    """Return model text, or None if no provider configured / call failed.
    Callers must always have a deterministic fallback."""
    if not available():
        return None
    try:
        if settings.llm_provider == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=settings.anthropic_key)
            msg = client.messages.create(
                model=settings.llm_model, max_tokens=max_tokens, system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        if settings.llm_provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_key)
            r = client.chat.completions.create(
                model=settings.llm_model, max_tokens=max_tokens,
                messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
            )
            return r.choices[0].message.content
    except Exception as exc:  # never let an LLM outage break a deliverable
        print(f"[llm] fallback to rule-based output: {exc}")
    return None
