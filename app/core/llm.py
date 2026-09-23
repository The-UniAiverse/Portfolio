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


def complete_with_usage(prompt: str, max_tokens: int = 800, model: str | None = None, system: str | None = None) -> dict | None:
    """Like complete(), but returns the token counts the provider reports, for metering. None when no provider is configured or the call fails."""
    if not available(): return None
    model = model or settings.llm_model; system = system or SYSTEM
    try:
        if settings.llm_provider == "anthropic":
            import anthropic
            msg = anthropic.Anthropic(api_key=settings.anthropic_key).messages.create(model=model, max_tokens=max_tokens, system=system, messages=[{"role": "user", "content": prompt}])
            return {"text": "".join(b.text for b in msg.content if getattr(b, "type", "") == "text"), "tokens_in": msg.usage.input_tokens, "tokens_out": msg.usage.output_tokens, "model": model, "provider": "anthropic"}
        if settings.llm_provider == "openai":
            from openai import OpenAI
            r = OpenAI(api_key=settings.openai_key).chat.completions.create(model=model, max_tokens=max_tokens, messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}])
            return {"text": r.choices[0].message.content, "tokens_in": r.usage.prompt_tokens, "tokens_out": r.usage.completion_tokens, "model": model, "provider": "openai"}
    except Exception as exc:
        print(f"[llm] gateway call failed: {exc}")
    return None
