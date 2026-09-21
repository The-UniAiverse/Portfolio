"""Evaluation toolkit: retrieval metrics, answer metrics, a rubric judge with calibration, and a CI gate."""
from __future__ import annotations
import math, re
from common import _terms, llm, LIVE

def recall_at_k(ranked_ids, relevant, k): return len(set(ranked_ids[:k]) & set(relevant)) / (len(set(relevant)) or 1)
def precision_at_k(ranked_ids, relevant, k): return len(set(ranked_ids[:k]) & set(relevant)) / k
def mrr(ranked_ids, relevant):
    for i, d in enumerate(ranked_ids, 1):
        if d in relevant: return 1 / i
    return 0.0
def ndcg(ranked_ids, gains: dict, k: int):
    dcg = sum(gains.get(d, 0) / math.log2(i + 1) for i, d in enumerate(ranked_ids[:k], 1))
    ideal = sum(g / math.log2(i + 1) for i, g in enumerate(sorted(gains.values(), reverse=True)[:k], 1)); return dcg / ideal if ideal else 0.0

REFUSAL = "could not find"
def faithfulness(answer: str, passages: list[str]) -> float:
    """Share of answer sentences whose content words are mostly present in the retrieved passages."""
    ctx = set(_terms(" ".join(passages))); sents = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\(Source:[^)]*\)", "", answer)) if s.strip()]
    if not sents: return 0.0
    ok = 0
    for s in sents:
        t = _terms(s)
        if not t or sum(1 for w in t if w in ctx) / len(t) >= 0.7: ok += 1
    return ok / len(sents)
def correctness(answer: str, expected: str) -> float:
    """Term coverage: for each ';'-separated key fact, the share of its content words found in the text. 1.0 = every fact fully present."""
    keys = [k for k in expected.split(";") if k.strip()]; a = set(_terms(answer)); cov = []
    for k in keys:
        t = _terms(k); cov.append(sum(1 for w in t if w in a) / len(t) if t else 1.0)
    return sum(cov) / (len(cov) or 1)
def refusal_correct(answer: str, should_refuse: bool) -> bool: return (REFUSAL in answer.lower()) == should_refuse

RUBRIC = [("grounded", "cites a source or section", lambda a: bool(re.search(r"source:|according to|§|›", a.lower()))),
          ("specific", "contains a number, limit or date", lambda a: bool(re.search(r"\d", a))),
          ("concise", "under 60 words", lambda a: len(a.split()) <= 60),
          ("no_hedging", "no filler such as 'it depends' / 'generally'", lambda a: not re.search(r"it depends|generally speaking|as an ai", a.lower()))]
def judge(question: str, answer_text: str, reference: str = "") -> dict:
    """Rubric judge. LIVE: asks the model to score each criterion 0/1 (and we parse strictly). OFFLINE: deterministic checks.
    Either way the judge is only trusted after calibrate() against human labels."""
    if LIVE:
        crit = "\n".join(f"- {n}: {d}" for n, d, _ in RUBRIC)
        r = llm.complete(f"Score the ANSWER on each criterion with 0 or 1. Reply only as name=0/1 lines.\n{crit}\nQUESTION: {question}\nREFERENCE: {reference}\nANSWER: {answer_text}", max_tokens=80) or ""
        got = dict(re.findall(r"(\w+)\s*=\s*([01])", r))
        if len(got) == len(RUBRIC): s = {n: int(got[n]) for n, _, _ in RUBRIC}; return {"scores": s, "total": sum(s.values()) / len(s)}
    s = {n: int(f(answer_text)) for n, _, f in RUBRIC}; return {"scores": s, "total": sum(s.values()) / len(s)}
def cohen_kappa(a: list[int], b: list[int]) -> float:
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n; pe = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b)); return (po - pe) / (1 - pe) if pe < 1 else 1.0

def gate(results: dict, thresholds: dict, baseline: dict | None = None, max_drop: float = 0.03) -> tuple[bool, list[str]]:
    """CI gate: absolute floors + no regression versus the last released baseline."""
    fails = [f"{m} {results.get(m, 0):.2f} < floor {t:.2f}" for m, t in thresholds.items() if results.get(m, 0) < t]
    for m, b in (baseline or {}).items():
        if results.get(m, 0) < b - max_drop: fails.append(f"{m} regressed {b:.2f} → {results.get(m, 0):.2f} (allowed drop {max_drop:.2f})")
    return (not fails), fails
