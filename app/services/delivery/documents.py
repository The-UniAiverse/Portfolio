"""M5 document generator and M12 pack assembler: every deliverable is built as report sections (see app/core/report.py),
then rendered to Markdown, PDF and Word. One builder per deliverable id; depth 'lite' keeps the first sections and trims tables."""
from __future__ import annotations
import json, re
from pathlib import Path
from app.core import report
from app.core.report import section as S, para as P, bullets as UL, table as T
from . import engine

def catalogue(sz: dict, r: dict) -> list[dict]:
    lib = engine.content("deliverables")["catalogue"]; tier = sz["tier"]; out = []
    for d in lib:
        depth = d.get(tier, ""); added = ""
        if not depth and d.get("risk_added") and r["risk_tier"] == "high": depth, added = "full", "added by the high-impact risk floor"
        out.append({"n": d["n"], "id": d["id"], "title": d["title"], "stage": d["stage"], "depth": depth or "—", "included": bool(depth), "note": added})
    return out

def _m(v, cur=""): return f"{cur} {v:,.0f}".strip() if isinstance(v, (int, float)) else str(v)

def build(did: str, i, R: dict, depth: str) -> tuple[str, list[dict]]:
    """Return (title, sections) for one deliverable."""
    L = engine.content("deliverables")["library"]; cat = {d["id"]: d for d in engine.content("deliverables")["catalogue"]}; title = cat[did]["title"]; sz, pl, est, llm, pc, gv, sec = (R[k] for k in ("sizing", "plan", "estimate", "llm_cost", "project_cost", "governance", "security")); cur = pc["currency"]
    full = depth == "full"; tier = R["tier"]
    if did == "discovery_questions":
        areas = list(dict.fromkeys(q["area"] for q in L["discovery"])); secs = [S("Purpose", P(f"Questions uniAIverse needs answered before a firm estimate for <b>{i.project}</b>. Already known: {i.problem}"))]
        secs += [S(a, T(["#", "Question", "Why it matters"], [[f"{a[0]}{n}", q["q"], q["why"]] for n, q in enumerate([q for q in L["discovery"] if q["area"] == a], 1)], [10, 98, 70])) for a in areas]
    elif did == "sizing_sheet":
        secs = [S("Result", P(f"Sizing score <b>{sz['score']}</b> of 24 → base tier <b>{sz['base_tier'].title()}</b>; final tier <b>{tier.title()}</b>. {sz['tier_profile']['for']}")), S("Score sheet", T(["Dimension", "Answer", "Points"], [[x["dimension"], x["answer"], x["points"]] for x in sz["score_sheet"]], [55, 100, 23])),
                S("Risk floors applied", UL(sz["floors_applied"] or ["None — the size score stands."])), S("What the tier sets", T(["Aspect", "This engagement"], [["Estimation method", sz["tier_profile"]["estimation"]], ["Gates", ", ".join(sz["tier_profile"]["gates"])], ["Gate formality", sz["tier_profile"]["gate_formality"]], ["Governance depth", sz["tier_profile"]["governance_depth"]], ["Security depth", sz["tier_profile"]["security_depth"]]], [50, 128]))]
    elif did == "use_case_canvas":
        secs = [S("Use case", T(["Element", "Content"], [["Problem", i.problem], ["Users and volume", f"{i.requests_per_day:,} requests/day expected"], ["Success metric", f"{i.success_metric or 'TO AGREE'} — baseline {i.baseline or 'TBC'} → target {i.target or 'TBC'}"], ["AI pattern", f"{pl['pattern_title']}. {pl['pattern_rationale']}"],
                 ["Data", f"{i.data_sources} source(s); classification: {sec['data_classification']}"], ["Human role", gv["oversight"]], ["Risk tier", gv["risk_tier"]], ["Value", _m(pc["roi"].get("annual_benefit", "not yet quantified"), cur)]], [40, 138]))]
        if full: secs += [S("Key risks of this pattern", UL(pl["key_risks"])), S("How success will be evaluated", P(pl["evaluation_approach"]))]
    elif did == "brd":
        secs = [S("Business context", P(f"{i.client} ({i.industry}). {i.problem}")), S("Objectives and measures", T(["Objective", "Metric", "Baseline", "Target"], [[i.project, i.success_metric or "TO AGREE", i.baseline or "TBC", i.target or "TBC"]], [60, 50, 34, 34])),
                S("Scope", P("<b>In scope</b>"), UL(i.in_scope or ["To be confirmed at G0"]), P("<b>Out of scope</b>"), UL(i.out_of_scope or ["To be confirmed at G0"]))]
        if full: secs += [S("Stakeholders", T(["Role", "Name"], [["Sponsor", i.sponsor or "TBC"], ["Product owner", i.product_owner or "TBC"]], [60, 118])), S("AI-specific requirements", UL(["Evaluation set and acceptance metric agreed before build", "Out-of-scope behaviour: refuse and route to a person", f"Human oversight: {gv['oversight']}", f"Cost ceiling: run cost within {_m(pc['run_monthly']['total'], cur)}/month expected", "Latency target agreed at G1", "Permissions enforced per user before retrieval"])),
                          S("Constraints and regulations", UL(gv["regulatory_checks"]))]
    elif did == "feasibility_note":
        rd = R["readiness"]; secs = [S("Verdict at initiation", P(f"Pattern: <b>{pl['pattern_title']}</b>. Feasibility is a hypothesis until the POC measures the metric on the evaluation set (gate G1). Readiness: {rd['score'] if rd['score'] is not None else 'not measured'} — {rd['effect']}")),
                S("Data readiness checklist", T(["Question", "Status"], [[q, "to confirm in discovery"] for q in ("Data exists for the task", "We can access it technically", "We are allowed to use it (lawful basis, contracts)", "Quality is known and acceptable", "Right answers / labels exist for evaluation", "Fresh enough", "Per-user permissions can be enforced")], [120, 58]))]
        if full: secs += [S("Components to prove in the POC", UL(pl["components"])), S("What would make us stop", UL(["Metric on the evaluation set below the agreed floor at G1", "No lawful basis for the data", "Cost per request above the business case ceiling"]))]
    elif did == "readiness_report":
        rd = R["readiness"]; secs = [S("Readiness baseline", P(f"Score: <b>{rd['score'] if rd['score'] is not None else 'not yet measured'}</b> ({rd['level']}). {rd['effect']}"), P(f"The tier-matched audit for this engagement is the <b>{tier.title()}</b> AI Readiness Audit, run on the audit page (/) or via POST /api/readiness_audit/run. Its PDF is attached to this pack when completed; its overall and data scores feed the estimate (contingency and data-engineering factor)."))]
    elif did == "effort_estimate":
        secs = [S("Summary", P(f"Method: <b>{est['method']}</b>. Stages in scope: {', '.join(est['stages_in_scope'])}. Expected <b>{est['expected_days']}</b> person-days (80% range {est['range_80'][0]}–{est['range_80'][1]}), plus contingency {est['contingency_pct']}% ({est['risk_profile']} risk profile: {', '.join(est['risk_profile_reasons']) or 'standard'}) = <b>{est['total_days']}</b> person-days." + (f" {est['presentation']}" if est.get("presentation") else "")))]
        secs.append(S("By workstream", T(["Workstream", "O", "L", "P", "Expected", "Driver"], [[w["workstream"], w["optimistic"], w["likely"], w["pessimistic"], w["expected"], f"{w['driver']} ×{w['factor']}"] for w in est["workstreams"]], [52, 18, 18, 18, 24, 48]) if tier != "bronze" else T(["Workstream", "Share of effort"], [[w["workstream"], f"{w['expected'] / est['expected_days']:.0%}"] for w in est["workstreams"]], [110, 68])))
        secs.append(S("By stage (cone of uncertainty)", T(["Stage", "Person-days", "Accuracy at this point"], [[s["stage"], s["person_days"], s["accuracy"]] for s in est["by_stage"]], [70, 40, 68])))
        if est.get("analogous"): secs.append(S("Analogous cross-check", P(f"Reference {est['analogous']['reference_days']} person-days; difference {est['analogous']['difference_pct']}%. {est['analogous']['note']}")))
        if est["flags"]: secs.append(S("Flags", UL(est["flags"])))
        secs.append(S("Formula", P("Three-point estimate per workstream: E = (O + 4L + P) / 6, σ = (P − O) / 6; workstream σ combined as root-sum-square.")))
    elif did == "llm_cost_model":
        if not llm["applicable"]: secs = [S("LLM run cost", P(llm["note"]))]
        else:
            secs = [S("Summary", P(f"Model class: <b>{llm['model']}</b>. Expected <b>${llm['per_request']:.4f}</b> per request → <b>${llm['monthly_expected']:,.0f}</b> per month at {i.requests_per_day:,} requests/day. Rates verified {llm['rates_verified']}. {llm['note']}")),
                    S("One request, line by line", T(["Part", "USD", "Share"], [[b["part"], f"{b['usd']:.5f}", f"{b['share']:.0%}"] for b in llm["breakdown"]], [70, 54, 54]), P("Tokens assumed: " + ", ".join(f"{k} {v}" for k, v in llm["tokens"].items()))),
                    S("Scenarios", T(["Scenario", "Requests/day", "Monthly USD", "Annual USD"], [[s["scenario"], f"{s['requests_per_day']:,}", f"{s['monthly']:,.0f}", f"{s['annual']:,.0f}"] for s in llm["scenarios"]], [45, 45, 44, 44]))]
            if tier != "bronze": secs += [S("Same workload on other model classes", T(["Model class", "Per request", "Monthly USD"], [[m["model"], f"{m['per_request']:.5f}", f"{m['monthly']:,.0f}"] for m in llm["models"]], [90, 44, 44])), S("Cost controls", T(["Control", "Monthly saving USD", "Status"], [[c["control"], "—" if c["monthly_saving"] is None else f"{c['monthly_saving']:,.0f}", c["status"]] for c in llm["controls"]], [90, 40, 48]))]
            if llm["growth"]: secs += [S("Growth", T(["Month", "Requests/day", "Monthly USD"], [[g["month"], f"{g['requests_per_day']:,}", f"{g['monthly']:,.0f}"] for g in llm["growth"]], [50, 64, 64])), S("Sensitivity (±50%)", T(["Assumption", "−50%", "+50%"], [[s["assumption"], f"{s['minus_50']:,.0f}", f"{s['plus_50']:,.0f}"] for s in llm["sensitivity"]], [90, 44, 44]))]
    elif did == "project_cost":
        secs = [S("Summary", P(f"Build: <b>{_m(pc['build_expected'], cur)}</b> (range at this point {_m(pc['build_range'][0], cur)} – {_m(pc['build_range'][1], cur)}, from the cone of uncertainty by stage; it narrows at every gate). Run: <b>{_m(pc['run_monthly']['total'], cur)}</b>/month. " + (f"12-month total {_m(pc['tco_12m'], cur)}." if tier == "bronze" else f"3-year TCO <b>{_m(pc['tco_3y'], cur)}</b>.") + f" Rate card status: {pc['rate_card_status']}.")),
                S("Build cost lines", T(["Line", f"Amount ({cur})", "Source"], [[l["line"], f"{l['amount']:,}", l["source"]] for l in pc["build_lines"]], [70, 36, 72])), S("Price range by stage", T(["Stage", "Low", "Expected", "High", "Accuracy"], [[s["stage"], f"{s['low']:,}", f"{s['expected']:,}", f"{s['high']:,}", s["accuracy"]] for s in pc["by_stage"]], [46, 30, 34, 30, 38])),
                S("Run cost per month", T(["Line", f"Amount ({cur})"], [[k.title(), f"{v:,}"] for k, v in pc["run_monthly"].items()], [110, 68])), S("Payment milestones", T(["Milestone", "%", f"Amount ({cur})"], [[m["milestone"], m["pct"], f"{m['amount']:,}"] for m in pc["milestones"]], [100, 20, 58]))]
        roi = pc["roi"]
        if tier != "bronze" and "roi_3y_pct" in roi: secs.append(S("Return", P(f"Annual benefit {_m(roi['annual_benefit'], cur)} (ramp 50% in year 1). 3-year ROI <b>{roi['roi_3y_pct']}%</b>, NPV at 10% {_m(roi['npv_10pct'], cur)}, payback <b>{roi['payback_months']}</b> months."), *([T(["Case", "3-year ROI %"], [[s["case"], s["roi_3y_pct"]] for s in roi["sensitivity"]], [110, 68])] if roi.get("sensitivity") else [])))
        elif "note" in roi: secs.append(S("Return", P(roi["note"])))
        if full and tier != "bronze": secs.append(S("People", T(["Role", "Days", "Day rate", "Cost"], [[p["role"], p["days"], f"{p['day_rate']:,}", f"{p['cost']:,}"] for p in pc["people"]], [80, 28, 34, 36])))
    elif did == "sow":
        secs = [S("Status", P("<b>DRAFT for human and legal review — not a contract.</b> Generated from the engagement record; every number traces to the estimate and cost sheets in this pack.")), S("1. Background and objectives", P(f"{i.client}: {i.problem} Objective: {i.success_metric or 'metric to agree'} from {i.baseline or 'baseline TBC'} to {i.target or 'target TBC'}.")),
                S("2. Scope and deliverables", UL(i.in_scope or ["As per BRD"]), P("Deliverables: " + "; ".join(d["title"] for d in R["deliverables"] if d["included"]))), S("3. Approach, phases and gates", T(["Stage", "Weeks", "Commercial model", "Exit gate"], [[p["stage"], p["weeks"], p["commercial_model"], p["exit_gate"]] for p in pl["phases"]], [60, 22, 60, 36])),
                S("4. Commercials", P(f"Indicative build price {_m(pc['build_range'][0], cur)} – {_m(pc['build_range'][1], cur)}; milestones per the project cost summary. Scope and price are re-baselined at each gate."))]
        if full: secs += [S(f"{n}. {h}", P("To be completed with legal: standard uniAIverse terms apply unless agreed otherwise.")) for n, h in enumerate(L["sow_sections"][5:], 5) if h not in ("Timeline", "Commercials and payment milestones")]
    elif did == "raid": secs = [S("Register", T(["Type", "Item", "Owner", "Response"], [[x["type"], x["item"], x["owner"], x["response"]] for x in L["raid"]] + [["Risk", k, "Delivery lead", "Mitigation in delivery plan"] for k in pl["key_risks"]], [24, 74, 30, 50])), S("Reserve", P(f"Contingency {est['contingency_pct']}% = {est['contingency_days']} person-days. " + ("Gold: reserve draw-down is reported at every gate." if tier == "gold" else "")))]
    elif did == "delivery_plan": secs = [S("Approach", P(pl["two_lifecycles"] + " " + pl["note"])), S("Phase plan", T(["Stage", "Weeks", "Commercial model", "Exit gate", "Estimate accuracy"], [[p["stage"], p["weeks"], p["commercial_model"], p["exit_gate"], p["estimate_accuracy"]] for p in pl["phases"]], [50, 18, 48, 30, 32]), P(f"Total duration {pl['duration_weeks'][0]}–{pl['duration_weeks'][1]} weeks. Gate formality: {pl['gate_formality']}.")),
                                         S("Team", T(["Role", "FTE"], [[t["role"], t["fte"]] for t in pl["team"]], [120, 58])), S("Reuse from uniAIverse", UL(pl["reuse"]))]
    elif did == "pattern_rationale":
        pats = engine.content("patterns")["patterns"]; secs = [S("Selected pattern", P(f"<b>{pl['pattern_title']}</b>. {pl['pattern_rationale']}")), S("Components", UL(pl["components"])), S("Alternatives considered", T(["Pattern", "Choose when", "Effort factor"], [[v["title"], v["choose_when"], v["effort_factor"]] for v in pats.values()], [50, 104, 24])), S("Evaluation", P(pl["evaluation_approach"]))]
    elif did == "risk_controls": secs = [S("Risk tier", P(f"<b>{gv['risk_tier'].title()}</b>" + (f" — driven by: {', '.join(gv['drivers'])}." if gv["drivers"] else ".") + f" {gv['oversight']}")), S("Required controls" + (f" (first {len(gv['controls'])} of {gv['controls_total']})" if len(gv["controls"]) < gv["controls_total"] else ""), T(["ID", "Control", "NIST", "ISO 42001", "Evidence"], [[c["id"], c["control"], c["nist"], c["iso42001"], c["evidence"]] for c in gv["controls"]], [12, 84, 20, 22, 40])),
                                         S("Regulatory checks", UL(gv["regulatory_checks"])), S("Note", P(gv["disclaimer"]))]
    elif did == "governance_gap": secs = [S("Governance evidence by gate", T(["Gate", "Evidence required"], [[g["gate"], g["evidence"]] for g in gv["gate_evidence"]], [20, 158]))] + [S(f"Plan — {h}", UL(v)) for h, v in gv.get("roadmap_30_60_90", {}).items()] + [S("Organisation-level gap questionnaire", P("Complete the gap questionnaire at /tools → Governance for maturity scores by NIST AI RMF function; the report attaches to this pack.")), S("Note", P(gv["disclaimer"]))]
    elif did == "rai_policy": secs = [S("Responsible AI policy — draft for " + i.client, P("Purpose: set out how AI is used safely, lawfully and accountably. Owner: to be named. Review: annual or on material change.")), S("Principles", UL(["Human accountability for every AI-supported decision", "Transparency to users and affected people", "Privacy and data minimisation", "Fairness testing where people are affected", "Security by design", "Proportionate governance by risk tier"])),
                                      S("Rules", UL(["Approved tools only; no personal or confidential data in unapproved tools", "Every AI system registered with owner, purpose, data and risk tier", "High-impact systems reviewed and signed off before production", "Incidents reported the same day", "Third-party models assessed before use"])), S("Tailored policy", P("A tailored policy PDF is generated by the Governance engine (/tools → Governance → policy)."))]
    elif did == "security_plan":
        secs = [S("Scope", P(f"Pattern: {pl['pattern_title']}. Data classification: <b>{sec['data_classification']}</b>. Depth: {sec['depth'].title()}. {sec['reference']}")), S("Data handling rules", UL(sec["handling_rules"])), S("Controls" + (" (checklist)" if sec["depth"] == "bronze" else ""), T(["ID", "Control", "Threat", "Due", "Owner"], [[c["id"], c["control"], c["threat"], c["due"], c["owner"]] for c in sec["controls"]], [12, 84, 40, 12, 30]))]
        if full: secs += [S("Threat model — threats in scope", UL(sec["threats"])), S("Security test plan", UL(sec["test_plan"]))] + ([S("Incident response", UL(sec["incident_outline"]))] if sec["incident_outline"] else [])
    elif did == "gate_checklists":
        secs = [S(g["title"] + ("" if g["mandatory"] else " — light checklist for this tier"), P(g["question"]), T(["ID", "Criterion", "Area", "Blocking", "Met?"], [[c["id"], c["text"], c["area"], "yes" if c["blocking"] else "no", "☐"] for c in g["criteria"]], [16, 100, 24, 18, 20])) for g in R["gates"].values()]
        secs.append(S("Gate review record (complete at each gate)", UL(["Date and attendees", "Evidence reviewed", "Criteria met and not met", "Risks carried forward", "Decision: go / conditional go / no-go / pivot", "Conditions and dates", "Named decision-maker"])))
    elif did == "evaluation_plan": secs = [S("Approach", P(pl["evaluation_approach"])), S("Test set definition", T(["Type", "Share", "Purpose"], [["Typical", "60%", "what users ask most"], ["Paraphrase", "15%", "same need, different words"], ["Multi-source", "10%", "needs two facts"], ["Out-of-scope", "10%", "must refuse"], ["Adversarial", "5%", "tries to break rules"]], [50, 28, 100])),
                                           S("Gates on quality", UL(["Floors agreed at G0 for correctness, faithfulness and refusal correctness", "No release if any metric drops more than 3 points vs the released baseline", "LLM judges used only after calibration against human labels (kappa ≥ 0.6)", "Weekly production sample: all thumbs-down, all 'not found', plus a random slice"]))]
    elif did == "engineering_standards": secs = [S("Standards", UL(L["engineering_standards"]))]
    elif did == "dpia": secs = [S("Status", P("<b>Working draft to be completed with the client's DPO — not a completed assessment.</b>")), S("Sections to complete", UL(L["dpia"])), S("Inputs from this engagement", UL([f"Purpose: {i.problem}", f"Data classification: {sec['data_classification']}", f"Risk tier: {gv['risk_tier']}"] + gv["regulatory_checks"]))]
    elif did == "model_card": secs = [S("System card — " + i.project, T(["Field", "Content"], [[f, "to complete at MVP"] for f in L["model_card"]], [90, 88])), S("Pre-filled", UL([f"Pattern: {pl['pattern_title']}", f"Intended use: {i.problem}", f"Human oversight: {gv['oversight']}", f"Evaluation: {pl['evaluation_approach']}"]))]
    elif did == "vendor_assessment": secs = [S("Assessment", T(["Check", "Question", "Finding"], [[v["check"], v["question"], "to complete"] for v in L["vendor"]], [28, 110, 40]))]
    elif did == "deployment_monitoring": secs = [S("Deployment", UL(["Blue/green or canary release with a tested rollback", "Stack manifest pinned: model, prompt, embedding model, index", "Release blocked by evaluation gate and open HIGH security findings"])), S("Monitoring", T(["Signal", "Metric", "Alert", "Owner"], [[m["signal"], m["metric"], m["alert"], m["owner"]] for m in L["monitoring"]], [24, 74, 50, 30]))]
    elif did == "ops_readiness": secs = [S("Operational readiness checklist", T(["Item", "Ready?"], [[x, "☐"] for x in ("Run team named and trained", "Alerts routed with owners", "Rollback rehearsed", "Support model and hours agreed", "Cost budget and alerts set", "Incident run-book tested (table-top)", "Backups and deletion procedure tested", "Handover accepted in writing")], [140, 38])), S("Run-book contents", UL(L["runbook"]))]
    elif did == "exec_readout":
        secs = [S("One-page read-out", UL([f"What: {i.project} for {i.client} — {pl['pattern_title']}", f"Tier: {tier.title()} (score {sz['score']}/24); risk tier {gv['risk_tier']}", f"Effort: {est['total_days']} person-days incl. {est['contingency_pct']}% contingency; duration {pl['duration_weeks'][0]}–{pl['duration_weeks'][1]} weeks",
                 f"Build {_m(pc['build_range'][0], cur)} – {_m(pc['build_range'][1], cur)}; run {_m(pc['run_monthly']['total'], cur)}/month; 3-year TCO {_m(pc['tco_3y'], cur)}"] + ([f"ROI {pc['roi']['roi_3y_pct']}% over 3 years; payback {pc['roi']['payback_months']} months"] if "roi_3y_pct" in pc["roi"] else []) + ["Decision asked: approve G0 and fund the POC"])),
                S("RACI", T(["Activity", "Sponsor", "Product owner", "Delivery lead", "AI team", "Security / governance"], [[x["activity"], x["sponsor"], x["product_owner"], x["delivery_lead"], x["ai_team"], x["security_gov"]] for x in L["raci"]], [68, 20, 24, 24, 18, 24]))]
    else: raise KeyError(did)
    if not full: secs = secs[:4]
    return title, secs

def to_docx(title: str, sub: str, docs: list[tuple[str, list[dict]]], path: Path):
    from docx import Document
    d = Document(); d.add_heading(title, 0); d.add_paragraph(sub); clean = lambda t: re.sub(r"<[^>]+>", "", str(t).replace("<br/>", "\n"))
    for n, (t, secs) in enumerate(docs):
        if n: d.add_page_break()
        d.add_heading(t, level=1)
        for s in secs:
            d.add_heading(clean(s["heading"]), level=2)
            for b in s["blocks"]:
                if b["type"] == "p": d.add_paragraph(clean(b["text"]))
                elif b["type"] == "ul":
                    for it in b["items"]: d.add_paragraph(clean(it), style="List Bullet")
                elif b["type"] == "table":
                    tb = d.add_table(rows=1, cols=len(b["headers"])); tb.style = "Table Grid"
                    for k, h in enumerate(b["headers"]): tb.rows[0].cells[k].text = str(h)
                    for r in b["rows"]:
                        cells = tb.add_row().cells
                        for k, c in enumerate(r): cells[k].text = clean(c)
    d.save(path)

def assemble(i, R: dict, out_dir: Path, stem: str, only: list[str] | None = None) -> dict:
    """M12 — one PDF, one Word file, one Markdown file and the machine-readable JSON for the whole pack."""
    out_dir.mkdir(parents=True, exist_ok=True); inc = [d for d in R["deliverables"] if d["included"] and (not only or d["id"] in only)]; docs = [build(d["id"], i, R, d["depth"]) for d in inc]
    st = R["stamp"]; title = f"AI Delivery Pack — {i.project}"; sub = f"{i.client} · {R['tier'].title()} tier · DRAFT for review · engine {st['engine']} · content {st['content_hash']}"
    cover = [report.section("About this pack", report.para(R["status"]), report.para(f"Generated from one engagement record. Tier <b>{R['tier'].title()}</b> (score {R['sizing']['score']}/24). {len(inc)} deliverable(s) follow."), report.table(["#", "Deliverable", "Stage", "Depth"], [[d["n"], d["title"], d["stage"], d["depth"] + (f" ({d['note']})" if d["note"] else "")] for d in inc], [10, 108, 30, 30]),
             *([report.para("<b>Overrides applied:</b> " + "; ".join(f"{o['field']} = {o['value']} ({o['reason']}, by {o['by']})" for o in R["overrides"]))] if R["overrides"] else []), *([report.para("<b>Content warnings:</b> " + " · ".join(R["stale_content"]))] if R["stale_content"] else []))]
    flat = cover + [{"heading": f"{d['n']}. {t} — {s['heading']}" if k == 0 else s["heading"], "blocks": ([report.page_break()] if k == 0 else []) + s["blocks"]} for d, (t, secs) in zip(inc, docs) for k, s in enumerate(secs)]
    report.write_both(out_dir, stem, title, sub, flat); to_docx(title, sub, [("About this pack", cover)] + [(f"{d['n']}. {t}", s) for d, (t, s) in zip(inc, docs)], out_dir / f"{stem}.docx")
    (out_dir / f"{stem}.json").write_text(json.dumps({"intake": i.model_dump(), "result": R}, indent=1, default=str))
    return {"documents": len(inc), "files": {k: f"{stem}.{k}" for k in ("pdf", "docx", "md", "json")}}
