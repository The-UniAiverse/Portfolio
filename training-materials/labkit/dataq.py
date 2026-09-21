"""Data quality, PII and drift — the checks an AI-ready dataset must pass."""
from __future__ import annotations
import math, re, datetime as dt

PII = {"email": r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", "phone_in": r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", "pan": r"\b[A-Z]{5}\d{4}[A-Z]\b",
       "card": r"(?<!\d)(?:\d[ -]?){15,16}(?!\d)", "aadhaar": r"(?<!\d)\d{4}\s?\d{4}\s?\d{4}(?!\d)", "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"}
def luhn(num: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", num)][::-1]
    return len(d) >= 13 and sum(x if i % 2 == 0 else (x * 2 - 9 if x * 2 > 9 else x * 2) for i, x in enumerate(d)) % 10 == 0
def find_pii(text: str) -> list[tuple[str, str]]:
    hits = []
    for kind, pat in PII.items():
        for m in re.findall(pat, text):
            if kind == "card" and not luhn(m): continue
            if kind == "aadhaar" and any(m.strip() in text[max(0, text.find(h[1]) - 1): text.find(h[1]) + len(h[1]) + 1] for h in hits if h[0] == "card"): continue
            hits.append((kind, m.strip()))
    return hits
def redact(text: str) -> tuple[str, int]:
    n = 0
    for kind, val in sorted(find_pii(text), key=lambda h: -len(h[1])):
        if val in text: text = text.replace(val, f"[{kind.upper()}]"); n += 1
    return text, n

def profile(rows: list[dict], rules: dict | None = None, today: dt.date | None = None) -> dict:
    """Six quality dimensions on a list-of-dict table. rules: {col: {'required':bool,'unique':bool,'regex':str,'min':x,'max':y,'allowed':[...]}}, '_freshness': (date_col, max_age_days)"""
    rules = rules or {}; today = today or dt.date(2026, 9, 21); n = len(rows) or 1; cols = sorted({k for r in rows for k in r}); out = {"rows": len(rows), "columns": {}, "issues": []}
    for c in cols:
        vals = [r.get(c) for r in rows]; filled = [v for v in vals if v not in (None, "", "NA", "null")]; ru = rules.get(c, {})
        comp = len(filled) / n; uniq = len(set(map(str, filled))) / (len(filled) or 1); bad = 0
        for v in filled:
            if "regex" in ru and not re.fullmatch(ru["regex"], str(v)): bad += 1
            elif "allowed" in ru and v not in ru["allowed"]: bad += 1
            elif ("min" in ru or "max" in ru):
                try:
                    f = float(v)
                    if f < ru.get("min", -math.inf) or f > ru.get("max", math.inf): bad += 1
                except (TypeError, ValueError): bad += 1
        valid = 1 - bad / (len(filled) or 1); out["columns"][c] = {"completeness": comp, "uniqueness": uniq, "validity": valid}
        if ru.get("required") and comp < 0.98: out["issues"].append(f"{c}: {pct_(1 - comp)} missing (required)")
        if ru.get("unique") and uniq < 1: out["issues"].append(f"{c}: {len(filled) - len(set(map(str, filled)))} duplicate value(s) (must be unique)")
        if bad: out["issues"].append(f"{c}: {bad} invalid value(s)")
    if "_freshness" in rules:
        col, max_age = rules["_freshness"]; ages = []
        for r in rows:
            try: ages.append((today - dt.date.fromisoformat(str(r.get(col))[:10])).days)
            except ValueError: pass
        stale = sum(1 for a in ages if a > max_age); out["freshness"] = {"stale_rows": stale, "oldest_days": max(ages or [0])}
        if stale: out["issues"].append(f"{col}: {stale} row(s) older than {max_age} days")
    pii_cols = sorted({c for r in rows for c, v in r.items() if isinstance(v, str) and find_pii(v)}); out["pii_columns"] = pii_cols
    sc = [min(v["completeness"], v["validity"]) for v in out["columns"].values()]; out["score"] = round(100 * sum(sc) / (len(sc) or 1) - 3 * len(out["issues"]), 1)
    return out
def pct_(x): return f"{x * 100:.0f}%"

def shingles(t: str, k: int = 5) -> set: t = re.sub(r"\s+", " ", t.lower()); return {t[i:i + k] for i in range(max(1, len(t) - k + 1))}
def near_duplicates(docs: list[dict], thr: float = 0.7) -> list[tuple[str, str, float]]:
    sh = [(d["id"], shingles(d["text"])) for d in docs]; out = []
    for i in range(len(sh)):
        for j in range(i + 1, len(sh)):
            a, b = sh[i][1], sh[j][1]; s = len(a & b) / (len(a | b) or 1)
            if s >= thr: out.append((sh[i][0], sh[j][0], round(s, 2)))
    return out

def psi(expected: list[float], actual: list[float], bins: int = 6) -> float:
    """Population Stability Index. <0.1 stable · 0.1–0.25 watch · >0.25 drifted."""
    lo, hi = min(expected), max(expected); w = (hi - lo) / bins or 1
    def dist(v): 
        c = [0] * bins
        for x in v: c[min(bins - 1, max(0, int((x - lo) / w)))] += 1
        return [max(k / len(v), 1e-4) for k in c]
    e, a = dist(expected), dist(actual); return sum((ai - ei) * math.log(ai / ei) for ei, ai in zip(e, a))
def psi_label(v: float) -> str: return "stable" if v < 0.1 else "watch" if v < 0.25 else "DRIFTED"
