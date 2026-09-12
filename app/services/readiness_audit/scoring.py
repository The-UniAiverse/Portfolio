"""Question bank loader + capability/domain/overall scoring.

Question line format: "<TIER><flags> text" — TIER in F/B/S/G/P, flags: * evidence, ! critical.
"""
from __future__ import annotations
import re
from pathlib import Path
import yaml
from .schemas import DimensionResult, CapabilityResult

HERE = Path(__file__).parent
BANK = HERE / "question_bank.yaml"
TIERS = HERE / "audit_tiers.yaml"
_LINE = re.compile(r"^([FBSGP])([*!]*)\s+(.*)$")

def load_bank() -> dict:
    return yaml.safe_load(BANK.read_text())

def load_tiers() -> dict:
    return yaml.safe_load(TIERS.read_text())

def _parse(line: str, prefix: str, idx: int) -> dict:
    m = _LINE.match(line.strip())
    if not m:
        raise ValueError(f"Bad question line: {line!r}")
    tier, flags, text = m.groups()
    return {"id": f"{prefix}.{idx}", "tier": tier, "text": text,
            "evidence": "*" in flags, "critical": "!" in flags}

def questionnaire(tier: str = "free", industries: list[str] | None = None) -> dict:
    """Return the question set for a tier (cumulative), optionally with industry modules."""
    bank, tiers = load_bank(), load_tiers()
    if tier not in tiers["tiers"]:
        raise ValueError(f"unknown tier {tier}")
    letters = set(tiers["tiers"][tier]["letters"])
    feats = tiers["tiers"][tier]["features"]
    domains = []
    for d in bank["domains"]:
        caps = []
        for c in d["capabilities"]:
            qs = [q for i, s in enumerate(c["questions"], 1) if (q := _parse(s, f"{d['id']}.{c['id']}", i))["tier"] in letters]
            if qs:
                caps.append({"id": c["id"], "title": c["title"], "questions": qs})
        domains.append({"id": d["id"], "title": d["title"], "weight": d["weight"], "capabilities": caps})
    modules = []
    if feats["industry_modules"] and industries:
        for m in bank["industry_modules"]:
            if m["id"] in industries:
                qs = [q for i, s in enumerate(m["questions"], 1) if (q := _parse(s, f"industry.{m['id']}", i))["tier"] in letters]
                modules.append({"id": m["id"], "title": m["title"], "questions": qs})
    total = sum(len(c["questions"]) for d in domains for c in d["capabilities"]) + sum(len(m["questions"]) for m in modules)
    return {"version": bank["version"], "tier": tier, "tier_info": tiers["tiers"][tier], "scale": bank["scale"],
            "maturity_bands": bank["maturity_bands"], "question_count": total, "domains": domains,
            "industry_modules": modules,
            "available_industries": [{"id": m["id"], "title": m["title"]} for m in bank["industry_modules"]]}

def _pct(vals: list[int]) -> float:
    return round(100 * sum(vals) / (4 * len(vals)), 1) if vals else 0.0

def score(qn: dict, answers: dict[str, int]) -> tuple[list[DimensionResult], list[dict], list[str]]:
    """Returns (domain results, industry module results, red flags)."""
    bank = load_bank()
    cap_meta = {f"{d['id']}.{c['id']}": c for d in bank["domains"] for c in d["capabilities"]}
    dims, red_flags = [], []
    for d in qn["domains"]:
        caps = []
        for c in d["capabilities"]:
            got = [(q, answers[q["id"]]) for q in c["questions"] if q["id"] in answers]
            if not got:
                continue
            meta = cap_meta[f"{d['id']}.{c['id']}"]
            red_flags += [q["text"] for q, v in got if q["critical"] and v <= 1]
            caps.append(CapabilityResult(
                id=c["id"], title=c["title"], score=_pct([v for _, v in got]), answered=len(got),
                total=len(c["questions"]),
                strengths=[q["text"] for q, v in got if v >= 3], gaps=[q["text"] for q, v in got if v <= 1],
                evidence_missing=[q["text"] for q, v in got if q["evidence"] and v >= 3],
                low_action=meta["low_action"], mid_action=meta["mid_action"]))
        dscore = round(sum(c.score for c in caps) / len(caps), 1) if caps else 0.0
        dims.append(DimensionResult(id=d["id"], title=d["title"], weight=d["weight"], score=dscore,
                                    answered=sum(c.answered for c in caps), total=sum(len(c["questions"]) for c in d["capabilities"]),
                                    capabilities=caps))
    modules = []
    for m in qn.get("industry_modules", []):
        got = [(q, answers[q["id"]]) for q in m["questions"] if q["id"] in answers]
        if got:
            modules.append({"id": m["id"], "title": m["title"], "score": _pct([v for _, v in got]),
                            "gaps": [q["text"] for q, v in got if v <= 1]})
    return dims, modules, red_flags

def overall(dims: list[DimensionResult]) -> float:
    answered = [d for d in dims if d.answered]
    if not answered:
        return 0.0
    w = sum(d.weight for d in answered)
    return round(sum(d.score * d.weight for d in answered) / w, 1)

def band(bands: list[dict], score_: float) -> tuple[str, str]:
    for b in bands:
        if b["min"] <= score_ <= b["max"]:
            return b["level"], b["summary"]
    return "Unknown", ""
