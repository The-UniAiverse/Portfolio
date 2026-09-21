"""Printing and small helpers shared by every demo."""
from __future__ import annotations
import random, sys

def rng(seed: int = 7) -> random.Random:
    """Seeded randomness: the room sees the same numbers the trainer rehearsed."""
    return random.Random(seed)

def table(headers: list[str], rows: list[list], indent: int = 2) -> None:
    rows = [[("" if c is None else (f"{c:,.2f}" if isinstance(c, float) else str(c))) for c in r] for r in rows]
    w = [max(len(str(h)), *(len(r[i]) for r in rows)) if rows else len(str(h)) for i, h in enumerate(headers)]
    pad = " " * indent
    print(pad + "  ".join(str(h).ljust(w[i]) for i, h in enumerate(headers)))
    print(pad + "  ".join("─" * w[i] for i in range(len(headers))))
    for r in rows: print(pad + "  ".join(r[i].ljust(w[i]) for i in range(len(headers))))

def bar(value: float, scale: float = 1.0, width: int = 30) -> str:
    n = max(0, min(width, round(value / scale * width))) if scale else 0
    return "█" * n + "·" * (width - n)

def step(n: int, text: str) -> None: print(f"\n[{n}] {text}")
def say(line: str) -> None: print(f"\nSay it: '{line}'")
def arg(flag: str, default, cast=float):
    """Tiny flag reader: python demo.py --daily 500"""
    if flag in sys.argv:
        try: return cast(sys.argv[sys.argv.index(flag) + 1])
        except (IndexError, ValueError): pass
    return default
def money(x: float, cur: str = "$") -> str: return f"{cur}{x:,.0f}" if abs(x) >= 100 else f"{cur}{x:,.2f}"
def pct(x: float) -> str: return f"{x * 100:.0f}%"

def api():
    """The real uniAIverse engine, in-process — demos call the same endpoints the website does."""
    import warnings; warnings.filterwarnings("ignore")
    from fastapi.testclient import TestClient; from app.main import app; return TestClient(app)
def data_path(file: str, name: str):
    import pathlib; return pathlib.Path(file).with_name("data") / name

SYNONYMS = {"money back": "refund", "get my money": "refund", "broken": "damaged damage claim", "parcel": "goods shipment", "holiday": "annual leave", "vacation": "leave paid out", "time off": "leave",
            "temps": "contractors", "freelancer": "contractor", "contract ends": "termination", "password expired": "expired sso session sign in", "difference between": "", "chatgpt": "chatgpt personal accounts company data approved"}
def grounded(question: str, passages: list[dict], max_sentences: int = 2) -> tuple[str, int, int]:
    """Grounded answer for labs. LIVE → the real model with the grounding instruction. OFFLINE → extractive: the best sentences
    from the retrieved passages (after synonym expansion), with the source, or an honest refusal when the evidence is weak."""
    import re
    from common import answer as _answer, LIVE as _LIVE, _terms as _t, tokens as _tok, GROUNDING as _G
    if _LIVE: return _answer(question, passages)
    q = question.lower()
    for k, v in SYNONYMS.items(): q = q.replace(k, v)
    qt = set(_t(q)); scored = []
    for p in passages:
        body = re.sub(r"^\[From:[^\]]*\]\s*", "", p["text"]); body = "\n".join(l for l in body.splitlines() if not l.startswith("#"))
        for sent in re.split(r"(?<=[.!?])\s+", body.replace("\n", " ")):
            st = set(_t(sent)); hits = len(qt & st)
            if hits: scored.append((max(hits / (len(qt) or 1), 0.34 if hits >= 3 else 0.0), sent.strip(), p))
    scored.sort(key=lambda x: -x[0]); ctx = " ".join(p["text"] for p in passages)
    if not scored or scored[0][0] < 0.34: out = "I could not find this in the available documents."
    else:
        best = [x for x in scored if x[0] >= max(0.34, scored[0][0] * 0.6)][:max_sentences]
        out = " ".join(dict.fromkeys(s for _, s, _ in best)) + f" (Source: {best[0][2]['doc']} › {best[0][2]['heading']})"
    return out, _tok(_G + ctx + question), _tok(out)

__all__ = ["grounded", "SYNONYMS", "api", "data_path", "rng", "table", "bar", "step", "say", "arg", "money", "pct"]
