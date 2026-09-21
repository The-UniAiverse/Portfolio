"""Text machinery for the business courses: extraction, brand voice, claim checks, repurposing, clustering.
OFFLINE these are transparent rules so the room can see *what a good prompt asks the model to do*; LIVE the same task goes to a model."""
from __future__ import annotations
import re
from common import _terms, llm, LIVE

def extract_actions(transcript: str) -> list[dict]:
    """Owner · action · due date from meeting lines such as 'Priya: I'll send the revised quote by Friday.'"""
    out = []
    for line in transcript.splitlines():
        m = re.match(r"\s*(\w+):\s*(.*)", line)
        if not m: continue
        who, said = m.groups(); a = re.search(r"\b(?:I'll|I will|I can|let me)\s+(.+?)(?:\s+by\s+([\w\s]+?))?[.!]?$", said, re.I)
        b = re.search(r"\b(\w+),?\s+(?:can you|could you|please)\s+(.+?)(?:\s+by\s+([\w\s]+?))?[.?!]?$", said, re.I)
        if a: out.append({"owner": who, "action": a.group(1).strip(), "due": (a.group(2) or "not stated").strip()})
        elif b: out.append({"owner": b.group(1), "action": b.group(2).strip(), "due": (b.group(3) or "not stated").strip()})
    return out
def extract_fields(text: str, spec: dict[str, str]) -> dict:
    """Structured extraction with a schema: {field: regex}. Missing stays None — never guessed."""
    return {k: (m.group(1).strip() if (m := re.search(p, text, re.I)) else None) for k, p in spec.items()}
def voice_check(draft: str, guide: dict) -> dict:
    """guide: {'banned': [...], 'max_sentence_words': n, 'must_have_cta': bool, 'person': 'we'|'i', 'exemplar': text}"""
    sents = [s for s in re.split(r"(?<=[.!?])\s+", draft) if s.strip()]; issues = []
    for b in guide.get("banned", []):
        if re.search(rf"\b{re.escape(b)}\b", draft, re.I): issues.append(f"banned phrase: '{b}'")
    long_ = [s for s in sents if len(s.split()) > guide.get("max_sentence_words", 22)]
    if long_: issues.append(f"{len(long_)} sentence(s) over {guide.get('max_sentence_words', 22)} words")
    if guide.get("must_have_cta") and not re.search(r"\b(book|reply|call|download|register|try|see|start)\b", sents[-1] if sents else "", re.I): issues.append("no clear call to action in the last sentence")
    if draft.count("!") > 1: issues.append("more than one exclamation mark")
    ex = set(_terms(guide.get("exemplar", ""))); d = set(_terms(draft)); sim = len(ex & d) / (len(ex | d) or 1)
    return {"issues": issues, "similarity_to_exemplar": round(sim, 2), "pass": not issues}
def check_claims(draft: str, facts: dict[str, str]) -> list[dict]:
    """Every number or superlative in a draft must trace to an approved fact. Returns one row per claim."""
    rows = []
    for s in re.split(r"(?<=[.!?])\s+", draft):
        nums = [n.strip().rstrip(".,") for n in re.findall(r"(?:INR\s?|\$|₹)\s?\d[\d,.]*(?:\s?(?:lakh|crore|k|m))?|\d[\d,.]*\s?(?:%|x\b|×)", s)]; sup = re.findall(r"\b(best|fastest|guaranteed|#1|leading|only|always|never|cure|risk-free)\b", s, re.I)
        if not nums and not sup: continue
        src = next((k for k, v in facts.items() if nums and all(re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", v) for n in nums)), None)
        rows.append({"claim": s.strip()[:90], "status": "supported" if src and not sup else "UNSUPPORTED" if not src and nums else "REVIEW (superlative)", "source": src or "—"})
    return rows
def repurpose(article: str, title: str) -> dict:
    """One long piece → six assets, each with its own constraint. LIVE asks the model; OFFLINE extracts so the constraints are visible."""
    body = " ".join(l for l in article.splitlines() if l.strip() and not l.lstrip().startswith("#"))
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", body) if len(s.split()) > 5]
    key = sorted(sents, key=lambda s: -(len(re.findall(r"\d", s)) * 2 + len(set(_terms(s)) & set(_terms(title)))))
    if LIVE:
        r = llm.complete(f"Repurpose this article titled '{title}' into: linkedin (<=60 words), tweet (<=240 chars), email_subject (<=8 words), email_body (<=80 words), faq (3 Q&A), slide (title + 3 bullets). Keep every number exact.\n\n{article}", max_tokens=600)
        if r: return {"live": r}
    return {"linkedin": " ".join(key[:3])[:400], "tweet": (key[0][:200] + " #AI")[:240], "email_subject": " ".join(title.split()[:8]), "email_body": " ".join(key[:4])[:520],
            "faq": [f"Q: {('What about ' + ' '.join(_terms(s)[:3]) + '?')}  A: {s}" for s in key[:3]], "slide": [title] + [" ".join(s.split()[:12]) for s in key[:3]]}
def cluster_keywords(keywords: list[str], k_shared: int = 1) -> dict[str, list[str]]:
    """Group search terms that share a stem — the start of a content brief."""
    groups: dict[str, list[str]] = {}
    for kw in keywords:
        t = [w for w in _terms(kw) if w not in ("ai", "best", "top")]; head = next((g for g in groups if len(set(_terms(g)) & set(t)) >= k_shared), None)
        groups.setdefault(head or (t[0] if t else kw), []).append(kw)
    return groups
