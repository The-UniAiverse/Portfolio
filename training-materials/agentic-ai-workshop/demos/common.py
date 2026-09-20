"""Shared helpers for the workshop demos.
Every demo runs in two modes:
  LIVE     — an LLM API key is set (ANTHROPIC_API_KEY or OPENAI_API_KEY) → real model calls
  OFFLINE  — no key → deterministic stand-ins so the room can still see every step of the machinery
Set the key in the repo's .env or export it in the shell. Nothing else changes."""
from __future__ import annotations
import json, math, os, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from app.core import llm  # noqa: E402  (provider-agnostic; reads .env)

DOCS = Path(__file__).with_name("sample_docs")
LIVE = llm.available()
RATES = {"cheap": (0.25, 1.25), "mid": (3.0, 15.0), "flagship": (15.0, 75.0)}   # $/M input, $/M output — verify quarterly

def banner(title: str):
    print("\n" + "═" * 78 + f"\n  {title}   [{'LIVE — real model' if LIVE else 'OFFLINE — deterministic stand-in'}]\n" + "═" * 78)

def tokens(text: str) -> int:
    """Good-enough tokenizer for teaching: ~4 characters per token in English."""
    return max(1, round(len(text) / 4))

def cost(in_tok: int, out_tok: int, tier: str = "mid") -> float:
    i, o = RATES[tier]; return in_tok / 1e6 * i + out_tok / 1e6 * o

def load_docs() -> list[dict]:
    return [{"id": p.stem, "title": p.read_text().splitlines()[0].lstrip("# "), "text": p.read_text()} for p in sorted(DOCS.glob("*.md"))]

def chunk_by_heading(doc: dict, contextual: bool = True) -> list[dict]:
    """Structure-aware chunking: split on ## headings; optionally prepend a contextual prefix."""
    parts = re.split(r"\n(?=## )", doc["text"]); out = []
    for i, p in enumerate(parts):
        p = p.strip()
        if not p or p.startswith("# "): continue
        heading = p.splitlines()[0].lstrip("# ")
        body = p if not contextual else f"[From: {doc['title']} › {heading}]\n{p}"
        out.append({"id": f"{doc['id']}#{i}", "doc": doc["title"], "heading": heading, "text": body})
    return out

def chunk_fixed(doc: dict, size_chars: int = 400) -> list[dict]:
    t = doc["text"]; return [{"id": f"{doc['id']}@{i}", "doc": doc["title"], "heading": "", "text": t[i:i + size_chars]} for i in range(0, len(t), size_chars)]

_STOP = set("the a an and or of to in is are for with on by at from that this it as be if do does what how which who when".split())
def _stem(w: str) -> str:
    for suf in ("ies", "ing", "ed", "es", "s"):
        if len(w) > 4 and w.endswith(suf): return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w
def _terms(s: str) -> list[str]: return [_stem(w) for w in re.findall(r"[a-z0-9_]+", s.lower()) if w not in _STOP]

def bm25(query: str, chunks: list[dict], k1: float = 1.5, b: float = 0.75) -> list[tuple[float, dict]]:
    """Keyword search (exact terms — great for codes, numbers, 'not')."""
    docs = [_terms(c["text"]) for c in chunks]; N = len(docs); avg = sum(map(len, docs)) / max(1, N)
    df = {}; [df.__setitem__(w, df.get(w, 0) + 1) for d in docs for w in set(d)]
    scores = []
    for c, d in zip(chunks, docs):
        s = 0.0; tf = {}; [tf.__setitem__(w, tf.get(w, 0) + 1) for w in d]
        for q in _terms(query):
            if q in tf: s += math.log(1 + (N - df[q] + 0.5) / (df[q] + 0.5)) * tf[q] * (k1 + 1) / (tf[q] + k1 * (1 - b + b * len(d) / avg))
        scores.append((s, c))
    return sorted(scores, key=lambda x: -x[0])

def semantic(query: str, chunks: list[dict]) -> list[tuple[float, dict]]:
    """'Meaning' search. LIVE: could call an embedding API; OFFLINE: a tiny synonym-expanded overlap so the effect is visible."""
    SYN = {"money back": "refund", "get my money": "refund", "reimburse": "refund", "holiday": "leave annual", "vacation": "leave paid out", "time off": "leave",
           "broken": "damaged claim", "parcel": "goods", "late": "late delivery", "lost": "lost shipment", "password expired": "expired sso session sign in", "temps": "contractors",
           "temp ": "contractor ", "freelancer": "contractor", "contract ends": "termination"}
    q = query.lower()
    for k, v in SYN.items(): q = q.replace(k, v)
    qt = set(_terms(q)); out = []
    for c in chunks:
        ct = set(_terms(c["text"])); ht = set(_terms(c["heading"]))
        out.append(((len(qt & ct) + 2 * len(qt & ht)) / math.sqrt(len(qt) * len(ct) + 1), c))
    return sorted(out, key=lambda x: -x[0])

def rrf(*ranked_lists: list[tuple[float, dict]], k: int = 60) -> list[tuple[float, dict]]:
    """Reciprocal Rank Fusion: combine lists by rank, not score. Agreement is evidence."""
    acc: dict[str, float] = {}; by_id = {}
    for lst in ranked_lists:
        for rank, (score, c) in enumerate(lst, 1):
            if score <= 0: continue                      # no evidence, no vote
            acc[c["id"]] = acc.get(c["id"], 0) + 1 / (k + rank); by_id[c["id"]] = c
    return sorted(((s, by_id[i]) for i, s in acc.items()), key=lambda x: -x[0])

def rerank(query: str, cands: list[dict], top: int = 3) -> list[dict]:
    """Cross-encoder stand-in. LIVE: ask the model to rank; OFFLINE: exact-phrase + heading bonus."""
    if LIVE and cands:
        listing = "\n".join(f"[{i}] {c['text'][:300]}" for i, c in enumerate(cands))
        r = llm.complete(f"Rank these passages by how well they answer the question. Return only the indices, best first, comma-separated.\nQuestion: {query}\n{listing}", max_tokens=60)
        try:
            order = [int(x) for x in re.findall(r"\d+", r or "")]
            picked = [cands[i] for i in order if i < len(cands)]; return (picked + [c for c in cands if c not in picked])[:top]
        except Exception: pass
    def s(c):
        t = c["text"].lower(); ht = _terms(c["heading"])
        return (sum(2 for w in _terms(query) if w in t) + 3 * sum(1 for w in _terms(query) if w in ht) + 0.5 * (len(cands) - cands.index(c)))
    return sorted(cands, key=s, reverse=True)[:top]

GROUNDING = ("Answer using ONLY the information in the documents provided. For every fact, say which document and section it came from. "
             "If the documents do not contain the answer, reply exactly: 'I could not find this in the available documents.' Do not use your own knowledge.")

def answer(question: str, passages: list[dict], history: str = "") -> tuple[str, int, int]:
    """Grounded generation. Returns (text, input_tokens, output_tokens)."""
    ctx = "\n\n".join(f"<document id='{p['id']}' source='{p['doc']} › {p['heading']}'>\n{p['text']}\n</document>" for p in passages)
    prompt = f"{GROUNDING}\n\n{ctx}\n\n{history}Question: {question}"
    if LIVE:
        out = llm.complete(prompt, max_tokens=300) or "(model returned nothing)"
    else:
        # OFFLINE: extractive — pick the sentence with most query terms; refuse if nothing matches.
        best, score = None, 0.0; qt = set(_terms(question)) or {question.lower()}
        for p in passages:
            body = re.sub(r"^\[From:[^\]]*\]\s*", "", p["text"]).replace("\n", " ")
            for sent in re.split(r"(?<=[.!?])\s+", body):
                st = set(_terms(sent)); hits = len(qt & st)
                sc = hits / len(qt)
                if hits and sc > score: best, score = (sent.strip(), p), sc
        # answer when at least half the question's terms appear in one sentence (min 1 hit); otherwise refuse honestly
        out = f"{best[0]} (Source: {best[1]['doc']} › {best[1]['heading']})" if best and score >= 0.5 else "I could not find this in the available documents."
    return out, tokens(prompt), tokens(out)

def hr(): print("─" * 78)
