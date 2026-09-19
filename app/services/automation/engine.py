"""Automation engine: workflow inventory → ROI → approach → current/future-state → implementation plan → PDF."""
from __future__ import annotations
import uuid
from datetime import date
from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from app.core import llm
from app.core.config import settings
from app.core.report import markdown_to_pdf

PB = Path(__file__).with_name("playbook.yaml")
def playbook() -> dict: return yaml.safe_load(PB.read_text())

class Step(BaseModel):
    name: str
    kind: str = Field("read", description="receive | read | lookup | decide | write | update | notify | review")
    minutes: float = 2
    system: str = ""

class Workflow(BaseModel):
    name: str
    function: str = "Operations"
    owner: str = ""
    trigger: str = ""
    volume_per_month: int = Field(..., ge=1)
    minutes_per_item: float = Field(..., ge=0.1)
    people_involved: int = Field(1, ge=1)
    hourly_cost: float = Field(25.0)
    error_rate_pct: float = Field(2.0, ge=0, le=100)
    cost_per_error: float = Field(20.0, ge=0)
    turnaround_hours: float = Field(24)
    rule_based: bool = False
    needs_judgement: bool = True
    multi_step: bool = False
    cross_system: bool = False
    data_access: str = Field("api", description="api | export | manual | none")
    steps: list[Step] = Field(default_factory=list)
    build_cost_usd: float | None = None
    monthly_run_usd: float | None = None

class AutomationRequest(BaseModel):
    organisation: str
    industry: str = "General"
    currency: str = "USD"
    default_build_cost_usd: float = 15000
    default_monthly_run_usd: float = 300
    workflows: list[Workflow]

def _approach(w: Workflow) -> str:
    env = w.model_dump()
    for r in playbook()["approach_rules"]:
        if eval(r["when"], {}, env): return r["approach"]
    return "hybrid"

def analyse(req: AutomationRequest) -> dict:
    pb = playbook(); rows = []
    for w in req.workflows:
        ap = _approach(w)
        pats = pb["step_patterns"]
        if w.steps:
            auto = sum(pats.get(s.kind, {"automation": 0.5})["automation"] * s.minutes for s in w.steps) / max(0.1, sum(s.minutes for s in w.steps))
        else:
            auto = {"rpa": 0.85, "llm": 0.6, "hybrid": 0.7, "agent": 0.65, "manual": 0.0}[ap]
        hours = w.volume_per_month * w.minutes_per_item / 60
        labour = hours * w.hourly_cost
        errors = w.volume_per_month * w.error_rate_pct / 100 * w.cost_per_error
        saving = (labour + errors) * auto
        build = w.build_cost_usd if w.build_cost_usd is not None else req.default_build_cost_usd * {"rpa": 0.6, "llm": 1.0, "hybrid": 1.1, "agent": 1.8, "manual": 0}[ap]
        run = w.monthly_run_usd if w.monthly_run_usd is not None else req.default_monthly_run_usd * {"rpa": 0.3, "llm": 1.0, "hybrid": 1.0, "agent": 3.0, "manual": 0}[ap]
        net = saving - run
        future = [{"step": s.name, "kind": s.kind, "now_minutes": s.minutes, "future": pats.get(s.kind, {"future": "Automate where deterministic"})["future"],
                   "automation_pct": round(100 * pats.get(s.kind, {"automation": 0.5})["automation"])} for s in w.steps]
        rows.append({"workflow": w.name, "function": w.function, "owner": w.owner, "approach": ap, "approach_label": pb["approaches"][ap]["label"],
                     "tools": pb["approaches"][ap]["tools"], "automation_pct": round(100 * auto), "hours_per_month": round(hours, 1),
                     "labour_cost": round(labour), "error_cost": round(errors), "monthly_saving": round(saving), "build_cost": round(build), "monthly_run": round(run),
                     "net_monthly": round(net), "payback_months": round(build / net, 1) if net > 0 else None,
                     "year1_net": round(net * 12 - build), "turnaround_hours_now": w.turnaround_hours, "turnaround_target_hours": round(w.turnaround_hours * (1 - auto * 0.8), 1),
                     "future_state": future, "priority_score": round(net / max(1, w.people_involved) - (build / 12) / 4, 1)})
    rows.sort(key=lambda r: r["priority_score"], reverse=True)
    top = [r for r in rows if r["approach"] != "manual"][:3]
    totals = {"monthly_saving": sum(r["monthly_saving"] for r in rows), "build_cost": sum(r["build_cost"] for r in top), "monthly_run": sum(r["monthly_run"] for r in top),
              "net_monthly_top3": sum(r["net_monthly"] for r in top), "year1_net_top3": sum(r["year1_net"] for r in top), "hours_freed_per_month": round(sum(r["hours_per_month"] * r["automation_pct"] / 100 for r in rows))}
    waves = [{"wave": i + 1, "workflow": r["workflow"], "approach": r["approach_label"], "plan": pb["implementation_plan"]} for i, r in enumerate(top)]
    return {"workflows": rows, "top3": top, "totals": totals, "waves": waves, "risks": pb["risks"]}

def narrative(req: AutomationRequest, a: dict) -> str:
    t = a["totals"]; top = ", ".join(f"{r['workflow']} ({r['approach_label']})" for r in a["top3"])
    txt = llm.complete(f"Write a 160-word executive summary for an automation assessment at {req.organisation}. Top 3: {top}. Totals: {t}. Plain prose.")
    if txt: return txt.strip()
    return (f"Across {len(a['workflows'])} workflows, automation can free about {t['hours_freed_per_month']} hours a month and save roughly ${t['monthly_saving']:,} monthly at full scope. "
            f"The first three waves — {top} — need about ${t['build_cost']:,} to build and ${t['monthly_run']:,} a month to run, for a net ${t['net_monthly_top3']:,} a month and "
            f"${t['year1_net_top3']:,} net in year one. Each wave follows a six-week pattern: baseline, build with a human-in-the-loop exception path, pilot on real items, roll out with monitoring. "
            f"The approach per workflow is chosen by its shape — deterministic steps go to scripts, reading and writing to LLM steps, multi-system judgement to an agent with caps — so cost and risk stay proportionate.")

def to_markdown(req: AutomationRequest, a: dict, nar: str) -> str:
    cur = req.currency
    L = [f"# AI Automation & Workflow Optimisation — {req.organisation}", f"*{req.industry} · {date.today().isoformat()} · uniAIverse*", "", "## Executive summary", nar, "",
         "## Workflow inventory and ROI", "", f"| # | Workflow | Function | Approach | Auto % | Hours/mo | Saving/mo ({cur}) | Build | Run/mo | Payback (mo) | Year-1 net |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {i} | {r['workflow']} | {r['function']} | {r['approach_label']} | {r['automation_pct']} | {r['hours_per_month']} | {r['monthly_saving']:,} | {r['build_cost']:,} | {r['monthly_run']:,} | {r['payback_months'] or 'n/a'} | {r['year1_net']:,} |" for i, r in enumerate(a["workflows"], 1)]
    t = a["totals"]
    L += ["", f"**Totals (top 3):** build {cur} {t['build_cost']:,} · run {cur} {t['monthly_run']:,}/mo · net {cur} {t['net_monthly_top3']:,}/mo · year-1 net {cur} {t['year1_net_top3']:,} · hours freed (all workflows) {t['hours_freed_per_month']}/mo", "",
          "## Current → future state (top 3)"]
    for r in a["top3"]:
        L += [f"### {r['workflow']} — {r['approach_label']}", f"Tools: {', '.join(r['tools']) or '—'}. Turnaround {r['turnaround_hours_now']}h → target {r['turnaround_target_hours']}h.", ""]
        if r["future_state"]:
            L += ["| Step | Now (min) | Future state | Automation |", "|---|---|---|---|"] + [f"| {s['step']} ({s['kind']}) | {s['now_minutes']} | {s['future']} | {s['automation_pct']}% |" for s in r["future_state"]] + [""]
        else: L += ["*No step breakdown provided — future state to be mapped in the design week.*", ""]
    L += ["## Implementation plan (per wave)", "", "| Week | Activities |", "|---|---|"] + [f"| {p['week']} | {'; '.join(p['activities'])} |" for p in playbook()["implementation_plan"]]
    L += ["", "## Waves"] + [f"- Wave {w['wave']}: {w['workflow']} — {w['approach']}" for w in a["waves"]]
    L += ["", "## Risks and mitigations"] + [f"- {x}" for x in a["risks"]] + ["", "---", "*Prepared by uniAIverse. Savings use owner-reported volumes and times; validate in week 1 of each wave.*"]
    return "\n".join(L)

def run(req: AutomationRequest) -> dict:
    a = analyse(req); nar = narrative(req, a); md = to_markdown(req, a, nar)
    rid = uuid.uuid4().hex[:10]; out = settings.outputs_dir / "automation"; out.mkdir(parents=True, exist_ok=True)
    (out / f"{rid}.md").write_text(md); markdown_to_pdf(md, out / f"{rid}.pdf")
    return {"report_id": rid, "organisation": req.organisation, "narrative": nar, **a, "report_markdown_url": f"/api/automation/report/{rid}.md", "report_pdf_url": f"/api/automation/report/{rid}.pdf"}
