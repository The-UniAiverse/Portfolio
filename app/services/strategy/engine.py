from __future__ import annotations
import re, uuid
from pathlib import Path
import yaml
from app.core import llm, report
from app.core.config import settings
from .schemas import StrategyRequest, UseCase

CFG = Path(__file__).with_name("config.yaml")
def cfg() -> dict: return yaml.safe_load(CFG.read_text())

def score(u: UseCase, w: dict) -> float:
    return round(u.value * w["value"] + u.feasibility * w["feasibility"] + u.strategic_fit * w["strategic_fit"]
                 + u.risk * w["risk"] + u.effort_weeks * w["effort_per_week"], 2)

def quadrant(u: UseCase, q: dict) -> str:
    if u.value >= q["quick_win"]["value_min"] and u.feasibility >= q["quick_win"]["feasibility_min"]: return "quick_win"
    if u.value >= q["strategic"]["value_min"]: return "strategic"
    if u.feasibility >= q["fill_in"]["feasibility_min"]: return "fill_in"
    return "deprioritise"

def kpis_for(u: UseCase, c: dict) -> list[str]:
    text = f"{u.name} {u.description} {u.function}".lower()
    for k in c["kpi_library"]:
        if any(m in text for m in k["match"]): return k["kpis"]
    return c["default_kpis"]

def budget_for(u: UseCase, c: dict) -> dict:
    b = c["budget_bands_usd"]; build = u.effort_weeks * b["build_per_week"]
    text = f"{u.name} {u.description}".lower()
    run = b["run_monthly"]["assistant"] if any(k in text for k in ["assistant", "chatbot", "support", "knowledge"]) else \
          b["run_monthly"]["model"] if any(k in text for k in ["forecast", "predict", "model", "churn"]) else \
          b["run_monthly"]["automation"] if any(k in text for k in ["automation", "extraction", "invoice", "workflow"]) else b["run_monthly"]["default"]
    return {"build_usd": build, "build_range_usd": [round(build * 0.8), round(build * 1.3)], "run_monthly_usd": run}

def business_case(u: UseCase, c: dict) -> dict:
    b = budget_for(u, c)
    annual_benefit = (u.monthly_benefit_usd or 0) * 12
    tco_year1 = b["build_usd"] + b["run_monthly_usd"] * 12
    roi = round(100 * (annual_benefit - tco_year1) / tco_year1, 1) if tco_year1 else None
    payback = round(b["build_usd"] / max(1, (u.monthly_benefit_usd or 0) - b["run_monthly_usd"]), 1) if u.monthly_benefit_usd and u.monthly_benefit_usd > b["run_monthly_usd"] else None
    return {**b, "annual_benefit_usd": annual_benefit, "tco_year1_usd": tco_year1, "roi_year1_pct": roi, "payback_months": payback,
            "kpis": kpis_for(u, c), "risks": [r for r in [
                "Data access not yet confirmed" if u.data_ready < 3 else None,
                "Regulatory / people impact — governance review required" if u.risk >= 4 else None,
                "Large effort — split into milestones" if u.effort_weeks > 10 else None,
                "Benefit not quantified — set baseline before build" if not u.monthly_benefit_usd else None] if r]}

def build(req: StrategyRequest) -> dict:
    c = cfg(); w = c["scoring"]; q = c["quadrants"]
    items = []
    for u in req.use_cases:
        qd = quadrant(u, q)
        items.append({"name": u.name, "function": u.function, "description": u.description, "owner": u.owner, "score": score(u, w),
                      "quadrant": qd, "quadrant_label": q[qd]["label"], "inputs": u.model_dump(), "business_case": business_case(u, c)})
    items.sort(key=lambda x: -x["score"])
    for i, it in enumerate(items, 1): it["rank"] = i
    # phases
    used, phases = set(), []
    for ph in c["phases"]:
        picked = [it for it in items if it["quadrant"] in ph["takes"] and it["name"] not in used][: ph["max_items"]]
        used |= {it["name"] for it in picked}
        foundations = []
        if ph["id"] == "p1" and req.readiness_score is not None:
            for band in c["foundations_by_readiness"]:
                if req.readiness_score < band["below"]: foundations = band["items"]; break
        phases.append({"id": ph["id"], "title": ph["title"], "months": ph["months"], "foundations": foundations,
                       "initiatives": [{"name": it["name"], "quadrant": it["quadrant_label"], "owner": it["owner"] or "TBC",
                                        "kpis": it["business_case"]["kpis"][:2], "build_usd": it["business_case"]["build_usd"]} for it in picked],
                       "budget_usd": sum(it["business_case"]["build_usd"] for it in picked)})
    deprioritised = [it["name"] for it in items if it["name"] not in used]
    om = next((o for o in c["operating_model_options"] if (req.company_size in ("small", "startup") and o["id"] == "central") or
               (req.company_size in ("medium", "large") and o["id"] == "hub_spoke") or (req.company_size == "enterprise" and o["id"] == "federated")), c["operating_model_options"][0])
    total_build = sum(p["budget_usd"] for p in phases); total_run = sum(it["business_case"]["run_monthly_usd"] for it in items if it["name"] in used)
    total_benefit = sum(it["business_case"]["annual_benefit_usd"] for it in items if it["name"] in used)
    narrative = llm.complete(
        f"Write a 200-word executive rationale for this AI roadmap for {req.organisation} ({req.company_size}). Goal: {req.top_goal}. "
        f"Readiness: {req.readiness_score}. Ranked backlog: {[(i['name'], i['quadrant_label'], i['score']) for i in items]}. Phases: {[(p['title'], [x['name'] for x in p['initiatives']]) for p in phases]}. "
        f"Year-1 build ${total_build}, run ${total_run}/mo, benefit ${total_benefit}/yr. Plain prose, three paragraphs, no bullets.") or (
        f"{req.organisation}'s backlog is ranked on value, feasibility and strategic fit, with risk and effort as penalties. "
        f"Phase 1 starts with {', '.join(x['name'] for x in phases[0]['initiatives']) or 'foundations only'}"
        f"{' after the foundations the readiness score calls for' if phases[0]['foundations'] else ''}, proving value inside a quarter. "
        f"Strategic bets follow once delivery rhythm, evaluation discipline and governance exist. Indicative year-one build is ${total_build:,} "
        f"with ${total_run:,}/month run cost against ${total_benefit:,}/year of quantified benefit; unquantified initiatives need baselines before build. "
        f"The recommended operating model is {om['title'].lower()} because {om['fits'].lower()}.")
    return {"strategy_id": uuid.uuid4().hex[:10], "organisation": req.organisation, "company_size": req.company_size, "top_goal": req.top_goal,
            "readiness_score": req.readiness_score, "backlog": items, "phases": phases, "deprioritised": deprioritised,
            "operating_model": om, "totals": {"build_usd": total_build, "run_monthly_usd": total_run, "annual_benefit_usd": total_benefit},
            "narrative": narrative, "config_version": c["version"]}

def render(r: dict) -> tuple[str, str]:
    S = [report.section("Executive summary", report.para(r["narrative"]),
                        report.para(f"<b>Year-one indicative budget:</b> build ${r['totals']['build_usd']:,} · run ${r['totals']['run_monthly_usd']:,}/month · quantified benefit ${r['totals']['annual_benefit_usd']:,}/year.")),
         report.section("Ranked use-case backlog", report.table(["#", "Use case", "Function", "Quadrant", "Score", "Build $", "Payback (mo)"],
             [[it["rank"], it["name"], it["function"], it["quadrant_label"], it["score"], f"{it['business_case']['build_usd']:,}", it["business_case"]["payback_months"] or "n/a"] for it in r["backlog"]],
             [8, 55, 30, 28, 17, 22, 18]))]
    for p in r["phases"]:
        blocks = []
        if p["foundations"]: blocks.append(report.bullets([f"Foundation: {f}" for f in p["foundations"]]))
        blocks.append(report.table(["Initiative", "Type", "Owner", "KPIs", "Build $"], [[i["name"], i["quadrant"], i["owner"], ", ".join(i["kpis"]), f"{i['build_usd']:,}"] for i in p["initiatives"]] or [["—", "", "", "", ""]], [60, 28, 30, 40, 20]))
        S.append(report.section(f"{p['title']} (months {p['months']}) — budget ${p['budget_usd']:,}", *blocks))
    S.append(report.section("Business cases", report.table(["Use case", "Annual benefit $", "TCO yr-1 $", "ROI yr-1", "KPIs", "Risks"],
             [[it["name"], f"{it['business_case']['annual_benefit_usd']:,}", f"{it['business_case']['tco_year1_usd']:,}",
               f"{it['business_case']['roi_year1_pct']}%" if it["business_case"]["roi_year1_pct"] is not None else "n/a",
               ", ".join(it["business_case"]["kpis"]), "; ".join(it["business_case"]["risks"]) or "—"] for it in r["backlog"]], [40, 22, 22, 16, 40, 38])))
    om = r["operating_model"]
    S.append(report.section("Operating model", report.para(f"<b>{om['title']}</b> — fits: {om['fits']}. Pros: {om['pros']}. Cons: {om['cons']}.")))
    if r["deprioritised"]: S.append(report.section("Deprioritised (revisit next quarter)", report.bullets(r["deprioritised"])))
    S.append(report.section("Next steps", report.bullets(["Confirm owners and baselines for Phase 1 initiatives", "Approve Phase 1 budget and steering cadence",
                                                          "Run governance risk classification for each initiative", "Schedule Phase 1 gate review at month 3"])))
    return report.write_both(settings.outputs_dir / "strategy", r["strategy_id"], f"AI Strategy & Roadmap — {r['organisation']}", f"{r['company_size']} · goal: {r['top_goal'] or '—'}", S)
