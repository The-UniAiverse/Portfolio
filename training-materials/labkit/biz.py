"""Business maths used across the leadership and delivery courses: prioritisation, ROI, TCO, estimates."""
from __future__ import annotations

def priority(value, feasibility, risk, effort, w=(0.35, 0.30, 0.20, 0.15)) -> float:
    """1–5 scales. Risk and effort are inverted: low risk / low effort score high."""
    return round((value * w[0] + feasibility * w[1] + (6 - risk) * w[2] + (6 - effort) * w[3]) * 20, 1)
def quadrant(value, feasibility) -> str:
    return "Quick win" if value >= 3.5 and feasibility >= 3.5 else "Strategic bet" if value >= 3.5 else "Fill-in" if feasibility >= 3.5 else "Park"
def roi(build: float, run_per_year: float, benefit_per_year: float, years: int = 3, ramp=(0.5, 1.0, 1.0), discount: float = 0.10) -> dict:
    cash = [-build] + [benefit_per_year * (ramp[min(y, len(ramp) - 1)]) - run_per_year for y in range(years)]
    npv = sum(c / (1 + discount) ** i for i, c in enumerate(cash)); total_cost = build + run_per_year * years; total_ben = sum(benefit_per_year * ramp[min(y, len(ramp) - 1)] for y in range(years))
    cum, payback = -build, None
    for y in range(years):
        yr = cash[y + 1]
        if payback is None and cum + yr >= 0 and yr > 0: payback = round((y + (-cum) / yr) * 12, 1)
        cum += yr
    return {"cashflows": cash, "npv": npv, "roi": (total_ben - total_cost) / total_cost if total_cost else 0.0, "payback_months": payback, "tco": total_cost}
def pert(o, m, p) -> tuple[float, float]: return (o + 4 * m + p) / 6, (p - o) / 6
def tco_build_buy(years: int, build: dict, buy: dict) -> dict:
    """build: {'initial','team_per_year','infra_per_year'}; buy: {'setup','licence_per_user_year','users','integration','exit_cost'}"""
    b = build["initial"] + years * (build["team_per_year"] + build["infra_per_year"])
    v = buy["setup"] + buy["integration"] + years * buy["licence_per_user_year"] * buy["users"] + buy.get("exit_cost", 0)
    return {"build": b, "buy": v, "cheaper": "build" if b < v else "buy", "difference": abs(b - v)}
def hours_saved(tasks: list[dict], hourly_cost: float, weeks: int = 46) -> dict:
    """tasks: [{'name','hours_per_week','ai_share'(0-1 of the task AI can take),'review_share'(0-1 time spent checking)}]"""
    rows = [(t["name"], t["hours_per_week"], t["hours_per_week"] * t["ai_share"] * (1 - t.get("review_share", 0.25))) for t in tasks]
    saved = sum(r[2] for r in rows); return {"rows": rows, "hours_per_week": saved, "value_per_year": saved * weeks * hourly_cost}
