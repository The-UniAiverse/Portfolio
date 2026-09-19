"""DEMO 7 · From workflow numbers to approach, ROI and a phased plan — using the uniAIverse engines the consultants use.
Module 10 / Lab 5. Runs offline. Change the numbers on the flipchart, re-run, watch payback move."""
from __future__ import annotations
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3]))          # repo root → import app.*
from common import banner, hr
from app.services.automation.engine import AutomationRequest, Workflow, analyse
from app.services.strategy.engine import build as build_roadmap
from app.services.strategy.schemas import StrategyRequest, UseCase

banner("Demo 7 · Workflow → approach → ROI → plan")
a = analyse(AutomationRequest(organisation="Workshop client", workflows=[
    Workflow(name="Supplier invoice processing", function="Finance", volume_per_month=2000, minutes_per_item=6, hourly_cost=22,
             error_rate_pct=3, cost_per_error=40, rule_based=False, needs_judgement=True, data_access="export"),
    Workflow(name="Customer status enquiries", function="Customer service", volume_per_month=4500, minutes_per_item=5, hourly_cost=20,
             needs_judgement=True, multi_step=True, cross_system=True, data_access="api"),
    Workflow(name="Weekly KPI report compilation", function="Operations", volume_per_month=4, minutes_per_item=240, hourly_cost=30,
             rule_based=True, needs_judgement=False, data_access="api")]))
print(f"{'Workflow':32s} {'Approach':30s} {'Saving/mo':>10s} {'Run/mo':>8s} {'Payback':>8s}")
for w in a["workflows"]:
    print(f"{w['workflow']:32s} {w['approach_label']:30s} ${w['monthly_saving']:>9,.0f} ${w['monthly_run']:>7,.0f} {str(w['payback_months'])+' mo':>8s}")
t = a["totals"]; hr()
print(f"Portfolio: hours freed {t['hours_freed_per_month']}/mo · saving ${t['monthly_saving']:,}/mo · build ${t['build_cost']:,} · top-3 year-1 net ${t['year1_net_top3']:,}")
print("\nSay it: 'The approach column is the decision. Agentic only where the row says multi-step AND cross-system AND judgement.'")

hr(); print("Now the same numbers as a roadmap (strategy engine):")
r = build_roadmap(StrategyRequest(organisation="Workshop client", company_size="medium", readiness_score=35, use_cases=[
    UseCase(name=w["workflow"], function=w["function"], value=4 if w["monthly_saving"] > 3000 else 2, feasibility=5 if w["approach"] in ("rpa", "llm") else 3,
            risk=3 if w["approach"] == "agent" else 2, effort_weeks=max(2, round(w["build_cost"] / 3500)), monthly_benefit_usd=w["monthly_saving"]) for w in a["workflows"]]))
for p in r["phases"]:
    print(f"  {p['title']} ({p['months']} months): " + (", ".join(i["name"] for i in p["initiatives"]) or "foundations only") + (f"  + {len(p['foundations'])} foundations" if p["foundations"] else ""))
print(f"  Year-1 build ${r['totals']['build_usd']:,} · run ${r['totals']['run_monthly_usd']:,}/mo · quantified benefit ${r['totals']['annual_benefit_usd']:,.0f}/yr")
print("\nSay it: 'Foundations first because the readiness score is 35. Quick wins fund the strategic bet.'")
