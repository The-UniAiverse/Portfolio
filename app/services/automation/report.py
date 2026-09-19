from __future__ import annotations
from pathlib import Path
from app.core.pdf import Doc

def to_markdown(r: dict) -> str:
    cur = r["currency"]; p = r["portfolio"]
    L = [f"# AI Automation & Workflow Optimisation — {r['organisation']}", f"*{r['industry']} · uniAIverse*", "", "## Executive summary", r["narrative"], "",
         "## Portfolio", f"- Workflows worth automating: {p['workflows_automatable']}", f"- Hours saved per month: {p['hours_saved_month']}", f"- Monthly saving: {cur} {p['monthly_saving']:,.0f}",
         f"- Monthly run cost: {cur} {p['monthly_run_cost']:,.0f} → net {cur} {p['net_monthly_benefit']:,.0f}", f"- Build: {cur} {p['build_usd'][0]:,}–{p['build_usd'][1]:,} · Payback {p['payback_months']} months · Year-1 ROI {p['year_one_roi_pct']}%", "",
         "## Workflow inventory and assessment", "", f"| # | Workflow | Function | Volume/mo | Min/item | Hours/mo | Approach | Complexity | Potential | Saving/mo | Payback |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {w['rank']} | {w['name']} | {w['function']} | {w['volume_per_month']:,} | {w['minutes_per_item']} | {w['hours_per_month']} | {w['approach_title']} | {w['complexity']}/5 | {w['automation_potential_pct']}% | {cur} {w['monthly_saving']:,.0f} | {w['payback_months']} mo |" for w in r["workflows"]]
    for w in r["workflows"]:
        L += ["", f"### {w['name']} — {w['approach_title']}", w["description"] or "", "", "**Current state:**"] + [f"{i}. {s}" for i, s in enumerate(w["steps"], 1)] + ["", "**Future state:**"] + [f"- {s}" for s in w["future_state"]]
        L += ["", f"**Human in the loop:** {w['human_in_the_loop']}", f"**Reliability:** {w['reliability']}", f"**Build:** {cur} {w['build_usd'][0]:,}–{w['build_usd'][1]:,} over {w['build_weeks'][0]}–{w['build_weeks'][1]} weeks · run {cur} {w['run_usd_month'][0]:,}–{w['run_usd_month'][1]:,}/month"]
    L += ["", "## Wave plan"] + [f"### {w['title']} (months {w['months']}) — {w['rule']}" + "\n" + ("\n".join(f"- {i}" for i in w["items"]) or "- (none)") for w in r["waves"]]
    L += ["", "## Risks"] + [f"- {x}" for x in r["risks"]] + ["", "---", "*uniAIverse — AI Automation & Workflow Optimisation.*"]
    return "\n".join(L)

def to_pdf(r: dict, path: Path) -> Path:
    cur = r["currency"]; p = r["portfolio"]
    d = Doc(f"AI Automation & Workflow Optimisation — {r['organisation']}", r["industry"]).h2("Executive summary").p(r["narrative"])
    d.h2("Portfolio").table([["Metric", "Value"], ["Workflows worth automating", str(p["workflows_automatable"])], ["Hours saved / month", str(p["hours_saved_month"])], ["Monthly saving", f"{cur} {p['monthly_saving']:,.0f}"],
        ["Monthly run cost", f"{cur} {p['monthly_run_cost']:,.0f}"], ["Net monthly benefit", f"{cur} {p['net_monthly_benefit']:,.0f}"], ["Build investment", f"{cur} {p['build_usd'][0]:,} – {p['build_usd'][1]:,}"],
        ["Payback", f"{p['payback_months']} months"], ["Year-1 ROI", f"{p['year_one_roi_pct']}%"]], [80, 70])
    d.h2("Workflow assessment").table([["#", "Workflow", "Vol/mo", "Hrs/mo", "Approach", "Cx", "Potential", "Saving/mo", "Payback"]] +
        [[str(w["rank"]), w["name"], f"{w['volume_per_month']:,}", str(w["hours_per_month"]), w["approach_title"], f"{w['complexity']}/5", f"{w['automation_potential_pct']}%", f"{w['monthly_saving']:,.0f}", f"{w['payback_months']} mo"] for w in r["workflows"]],
        [8, 40, 16, 14, 40, 10, 16, 20, 14])
    for w in r["workflows"]:
        d.h3(f"{w['name']} — {w['approach_title']}").p(w["description"] or "", small=True)
        if w["steps"]: d.p("<b>Current state</b>", small=True).bullets([f"{i}. {s}" for i, s in enumerate(w["steps"], 1)])
        d.p("<b>Future state</b>", small=True).bullets(w["future_state"])
        d.p(f"<b>Human in the loop:</b> {w['human_in_the_loop']} · <b>Reliability:</b> {w['reliability']} · <b>Build:</b> {cur} {w['build_usd'][0]:,}–{w['build_usd'][1]:,}, {w['build_weeks'][0]}–{w['build_weeks'][1]} weeks", small=True)
    d.page().h2("Wave plan")
    for w in r["waves"]: d.h3(f"{w['title']} (months {w['months']}) — {w['rule']}").bullets(w["items"] or ["(none)"])
    d.h2("Risks").bullets(r["risks"] or ["None identified"])
    return d.build(path)
