from __future__ import annotations
from pathlib import Path
import yaml
from .schemas import DimensionResult

QFILE = Path(__file__).with_name("questionnaire.yaml")

def load_questionnaire() -> dict:
    return yaml.safe_load(QFILE.read_text())

def score_dimensions(q: dict, answers: dict[str, int]) -> list[DimensionResult]:
    results = []
    for dim in q["dimensions"]:
        qs = dim["questions"]
        got = [(x, answers[x["id"]]) for x in qs if x["id"] in answers]
        pts = sum(v for _, v in got)
        max_pts = 4 * len(got) if got else 1
        score = round(100 * pts / max_pts, 1) if got else 0.0
        strengths = [x["text"] for x, v in got if v >= 3]
        gaps = [x["text"] for x, v in got if v <= 1]
        results.append(DimensionResult(
            id=dim["id"], title=dim["title"], weight=dim["weight"], score=score,
            answered=len(got), total=len(qs), strengths=strengths, gaps=gaps,
        ))
    return results

def overall(dims: list[DimensionResult]) -> float:
    answered = [d for d in dims if d.answered]
    if not answered:
        return 0.0
    w = sum(d.weight for d in answered)
    return round(sum(d.score * d.weight for d in answered) / w, 1)

def band(q: dict, score: float) -> tuple[str, str]:
    for b in q["maturity_bands"]:
        if b["min"] <= score <= b["max"]:
            return b["level"], b["summary"]
    return "Unknown", ""
