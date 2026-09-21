"""AI Delivery Framework engine — modules M1–M12 as plain functions over editable YAML content.
Deterministic by design: same intake + same content files = same numbers. Every result is stamped with the content versions it used."""
from __future__ import annotations
import hashlib, math
from datetime import date
from pathlib import Path
import yaml
from app.core.config import settings
from app.services.governance import engine as gov
from .schemas import Intake

CONTENT = Path(__file__).with_name("content")
FILES = ["tiers", "patterns", "wbs", "rate_card", "llm_rates", "gates", "security_controls", "deliverables"]
TIER_ORDER = ["bronze", "silver", "gold"]; STAGE_FOR_TARGET = {"poc": 2, "mvp": 3, "production": 4, "scale": 5}
ENGINE_VERSION = "1.0.0"

def content(name: str) -> dict: return yaml.safe_load((CONTENT / f"{name}.yaml").read_text())
def stamp() -> dict:
    """Which content produced this result — so a pack can always be reproduced or explained."""
    v = {n: str(content(n).get("version", "?")) for n in FILES}
    h = hashlib.sha256("".join((CONTENT / f"{n}.yaml").read_text() for n in FILES).encode()).hexdigest()[:12]
    return {"engine": ENGINE_VERSION, "content_versions": v, "content_hash": h, "generated": date.today().isoformat()}
def staleness() -> list[str]:
    out = []
    for n in FILES:
        c = content(n); d = c.get("verified") or c.get("last_reviewed")
        if not d: continue
        age = (date.today() - date.fromisoformat(str(d))).days; limit = 100 if n == "llm_rates" else 183
        if age > limit: out.append(f"{n}.yaml last reviewed {d} ({age} days ago) — review before quoting")
    rc = content("rate_card")
    if "placeholder" in str(rc.get("status", "")).lower(): out.append("rate_card.yaml holds PLACEHOLDER day rates — confirm before sending a price to a client")
    return out
def _override(i: Intake, field: str):
    return next((o for o in i.overrides if o.field == field), None)

# ── M9a risk pre-screen (reuses the Governance engine's classifier) ─────────────────────────────────────────────────
def risk(i: Intake) -> dict:
    s = gov.AISystem(name=i.project, purpose=i.problem, **{k: getattr(i, k) for k in ("affects_individuals_rights", "uses_biometrics_or_surveillance", "safety_critical", "interacts_with_public",
                     "generates_content", "processes_personal_data", "fully_automated_decisions", "manipulative_or_social_scoring")})
    tier = gov.classify(s); lib = gov.library(); ctrls = [c for c in lib["controls"] if tier in c.get("tiers", [])]
    drivers = [k.replace("_", " ") for k in ("manipulative_or_social_scoring", "affects_individuals_rights", "uses_biometrics_or_surveillance", "safety_critical", "fully_automated_decisions", "interacts_with_public", "processes_personal_data", "generates_content") if getattr(i, k)]
    return {"risk_tier": tier, "drivers": drivers, "required_controls": ctrls}

# ── M2 sizing and tiering ───────────────────────────────────────────────────────────────────────────────────────────
def size(i: Intake, r: dict | None = None) -> dict:
    t = content("tiers"); r = r or risk(i); sheet = []; total = 0
    for d in t["dimensions"]:
        v = int(i.sizing.get(d["id"], 0))
        if v not in (1, 2, 3): raise ValueError(f"sizing.{d['id']} must be 1, 2 or 3")
        total += v; sheet.append({"dimension": d["title"], "answer": d["options"][v - 1], "points": v})
    base = next(k for k, (lo, hi) in t["bands"].items() if lo <= total <= hi); tier = base; floors = []
    if r["risk_tier"] == "prohibited": return {"score": total, "base_tier": base, "tier": None, "stop": True, "score_sheet": sheet, "floors_applied": ["Prohibited use: the engine stops. A decline note is produced; no pack."], "depth": {}}
    def lift(to, why):
        nonlocal tier
        if TIER_ORDER.index(tier) < TIER_ORDER.index(to): tier = to
        floors.append(why)
    if i.sizing.get("data_sensitivity") == 3: lift("silver", "Regulated or special-category data → minimum Silver")
    if i.writes_to_production_systems: lift("silver", "Agent writes to production systems → minimum Silver, agentic controls added")
    depth = {"governance": tier, "security": tier}
    if r["risk_tier"] == "high": depth = {"governance": "gold", "security": "gold"}; floors.append("High-impact risk tier → governance and security at Gold depth; DPIA, model card and vendor assessment added")
    ov = _override(i, "tier")
    if ov and str(ov.value) in TIER_ORDER:
        if TIER_ORDER.index(str(ov.value)) < TIER_ORDER.index(tier) and floors: floors.append(f"Override to {ov.value} REFUSED — a risk floor applies; the tier can go up, never down")
        else: floors.append(f"Tier overridden {tier} → {ov.value} by {ov.by}: {ov.reason}"); tier = str(ov.value)
    return {"score": total, "base_tier": base, "tier": tier, "stop": False, "score_sheet": sheet, "floors_applied": floors, "depth": depth, "tier_profile": t["tiers"][tier]}

# ── M3 readiness baseline ───────────────────────────────────────────────────────────────────────────────────────────
def readiness(i: Intake) -> dict:
    s = i.readiness_score
    if s is None: return {"score": None, "level": "not measured", "effect": "Medium risk profile assumed. Run the AI Readiness Audit (/) — the tier-matched audit is deliverable 6.", "foundation_sprint": False}
    lvl = "low" if s < 40 else "medium" if s < 65 else "high"
    return {"score": s, "level": lvl, "effect": {"low": "Foundation sprint added before the POC; contingency at the top of its band; data engineering factor raised.", "medium": "Standard plan; watch data access at G1.", "high": "Standard plan; lower end of the contingency band."}[lvl], "foundation_sprint": lvl == "low"}

# ── M4 delivery strategy ────────────────────────────────────────────────────────────────────────────────────────────
def select_pattern(i: Intake) -> tuple[str, str]:
    P = content("patterns")["patterns"]; ov = _override(i, "pattern")
    if ov and str(ov.value) in P: return str(ov.value), f"Overridden by {ov.by}: {ov.reason}"
    if i.pattern in P: return i.pattern, "Chosen at intake. " + P[i.pattern]["choose_when"]
    if i.needs_actions_in_systems or i.writes_to_production_systems: k = "multi_agent" if i.use_cases >= 5 else "agent"
    elif i.structured_prediction: k = "classical_ml"
    elif i.extract_from_documents: k = "extraction"
    elif i.answer_in_documents: k = "rag"
    else: k = "assistant"
    return k, "Selected by rule. " + P[k]["choose_when"]
def plan(i: Intake, sz: dict, rd: dict, est: dict | None = None) -> dict:
    w = content("wbs"); P = content("patterns")["patterns"]; k, why = select_pattern(i); n = STAGE_FOR_TARGET.get(i.target_stage, 4); tier = sz["tier"]
    gates_in = sz["tier_profile"]["gates"]; stages = w["stages"][:n]; phases = []
    for idx, st in enumerate(stages):
        lo, hi = w["stage_weeks"][st]; f = {"bronze": 0.8, "silver": 1.0, "gold": 1.25}[tier]; g = f"G{idx}"
        phases.append({"stage": w["stage_titles"][st], "weeks": f"{max(1, round(lo * f))}–{round(hi * f)}", "weeks_lo": max(1, round(lo * f)), "weeks_hi": round(hi * f), "commercial_model": w["commercial_model"][st],
                       "exit_gate": g if g in gates_in else f"{g} (light checklist)", "estimate_accuracy": w["accuracy"][st]})
    if rd["foundation_sprint"]: phases.insert(1, {"stage": "Foundation sprint (data access, policy, tooling)", "weeks": "2–4", "weeks_lo": 2, "weeks_hi": 4, "commercial_model": "Fixed fee", "exit_gate": "readiness re-check", "estimate_accuracy": "—"})
    rc = content("rate_card")["roles"]; team = [{"role": rc[r]["title"], "fte": fte} for r, fte in sz["tier_profile"]["team"].items()]
    resize = "Bronze reaching Production triggers a re-size (usually to Silver)." if tier == "bronze" and n >= 4 else ""
    return {"pattern": k, "pattern_title": P[k]["title"], "pattern_rationale": why, "components": P[k]["components"], "key_risks": P[k]["key_risks"], "evaluation_approach": P[k]["evaluation"], "reuse": P[k]["reuse"],
            "phases": phases, "duration_weeks": [sum(p["weeks_lo"] for p in phases), sum(p["weeks_hi"] for p in phases)], "team": team, "gate_formality": sz["tier_profile"]["gate_formality"], "note": resize,
            "two_lifecycles": "Software lifecycle (app, APIs, integrations, infra) and AI lifecycle (data, experiments, prompts/training, evaluation) are planned as separate workstreams."}

# ── M6 effort estimator ─────────────────────────────────────────────────────────────────────────────────────────────
def risk_profile(i: Intake, r: dict, rd: dict, pattern: str) -> tuple[str, list[str]]:
    if i.risk_profile in ("low", "medium", "high"): return i.risk_profile, ["set at intake"]
    pts = 0; why = []
    if rd["level"] == "low": pts += 2; why.append("low readiness")
    elif rd["level"] in ("medium", "not measured"): pts += 1; why.append("readiness medium or unmeasured")
    if pattern in ("agent", "multi_agent"): pts += 2; why.append("agent autonomy")
    if r["risk_tier"] == "high": pts += 1; why.append("high-impact risk tier")
    if i.integrations >= 6: pts += 1; why.append("6+ integrations")
    if i.data_readiness_score is not None and i.data_readiness_score < 40: pts += 1; why.append("data readiness under 40")
    return ("low" if pts <= 1 else "medium" if pts <= 3 else "high"), why
def estimate(i: Intake, sz: dict, r: dict, rd: dict, pl: dict) -> dict:
    w = content("wbs"); f = w["factors"]; t = content("tiers"); tier = sz["tier"]; n = STAGE_FOR_TARGET.get(i.target_stage, 4); stages = w["stages"][:n]; pf = content("patterns")["patterns"][pl["pattern"]]["effort_factor"]
    uc = 1 + f["per_extra_use_case"] * (i.use_cases - 1); ig = max(f["min_integration_factor"], 1 + f["per_extra_integration"] * (i.integrations - 2)); ds = max(f["min_data_source_factor"], 1 + f["per_extra_data_source"] * (i.data_sources - 3)) * content("patterns")["patterns"][pl["pattern"]]["data_factor"]
    low_data = f["low_data_readiness"] if ((i.data_readiness_score is not None and i.data_readiness_score < 40) or rd["level"] == "low") else 1.0
    ov = _override(i, "effort_factor"); man = float(ov.value) if ov else 1.0
    scale = {"use_cases": uc, "data_sources": ds * low_data, "use_cases_pattern": uc * pf, "integrations_pattern": ig * (0.6 + 0.4 * pf), "integrations": ig, "risk": f["risk"][r["risk_tier"]] * f["tier_depth"][sz["depth"]["security"]],
             "gate_formality": f["gate_formality"][tier]}
    rows = []; by_stage = {s: 0.0 for s in stages}; roles: dict[str, float] = {}
    for ws in w["workstreams"]:
        k = scale[ws["scales_with"]] * man * (f["tier_depth"][tier] if ws["id"] in ("discovery", "mlops") else 1.0) * ({"bronze": 0.75, "silver": 1.0, "gold": 1.2}[tier] if ws["id"] in ("data", "ai", "app") else 1.0)
        sf = lambda s: f["bronze_light_mvp"] if (tier == "bronze" and s == "mvp") else 1.0
        L = sum(ws["days"][s] * k * sf(s) for s in stages); O = L * f["optimistic"]; Pp = L * f["pessimistic"][tier]; E = (O + 4 * L + Pp) / 6; sd = (Pp - O) / 6
        for s in stages: by_stage[s] += ws["days"][s] * k * sf(s) * (E / L if L else 1)
        for role, share in ws["roles"].items(): roles[role] = roles.get(role, 0) + E * share
        rows.append({"id": ws["id"], "workstream": ws["title"], "optimistic": round(O, 1), "likely": round(L, 1), "pessimistic": round(Pp, 1), "expected": round(E, 1), "sigma": round(sd, 1), "driver": ws["scales_with"].replace("_", " "), "factor": round(k, 2)})
    E = sum(x["expected"] for x in rows); sd = math.sqrt(sum(x["sigma"] ** 2 for x in rows)); prof, why = risk_profile(i, r, rd, pl["pattern"]); lo, hi = t["contingency"][prof]
    cpct = hi if rd["level"] == "low" else lo if rd["level"] == "high" else (lo + hi) / 2; ov = _override(i, "contingency_pct")
    if ov: cpct = float(ov.value)
    cont = E * cpct / 100; method = sz["tier_profile"]["estimation"]
    out = {"method": method, "stages_in_scope": [w["stage_titles"][s] for s in stages], "workstreams": rows, "by_stage": [{"stage": w["stage_titles"][s], "person_days": round(v, 1), "accuracy": w["accuracy"][s]} for s, v in by_stage.items()],
           "role_days": {k: round(v, 1) for k, v in sorted(roles.items(), key=lambda kv: -kv[1])}, "expected_days": round(E, 1), "sigma_days": round(sd, 1), "range_80": [round(E - 1.28 * sd, 1), round(E + 1.28 * sd, 1)],
           "risk_profile": prof, "risk_profile_reasons": why, "contingency_pct": round(cpct, 1), "contingency_band": [lo, hi], "contingency_days": round(cont, 1), "total_days": round(E + cont, 1),
           "drivers": {"use_cases": i.use_cases, "integrations": i.integrations, "data_sources": i.data_sources, "pattern_factor": pf, "manual_factor": man}, "flags": []}
    if method == "tshirt":
        sz_ = next(k for k, (a, b) in w["tshirt"].items() if a <= E + cont < b); a, b = w["tshirt"][sz_]; out["tshirt"] = {"size": sz_, "range_days": [a, b if b < 10000 else None]}
        out["presentation"] = f"T-shirt size {sz_}: {a}–{b if b < 10000 else '…'} person-days. Bronze quotes a range, not a point."
    if method == "pert_analogous":
        ref = w["analogous"][pl["pattern"]] * (1 + f["analogous_per_extra_use_case"] * (i.use_cases - 1)) * {"poc": 0.2, "mvp": 0.6, "production": 1.0, "scale": 1.25}.get(i.target_stage, 1.0) * f["analogous_tier"][tier]; diff = abs(ref - E) / ref if ref else 0
        out["analogous"] = {"reference_days": round(ref, 1), "difference_pct": round(diff * 100, 1), "note": w["analogous"]["note"]}
        if diff > 0.25: out["flags"].append(f"PERT ({E:.0f} d) and analogous ({ref:.0f} d) differ by {diff:.0%} — reconcile before quoting")
    return out

# ── M7 LLM cost calculator ──────────────────────────────────────────────────────────────────────────────────────────
def per_request(rate: dict, tok: dict, cache: bool) -> dict:
    steps = max(1, tok.get("steps", 1)); sysc = tok["system"] / 1e6 * (rate["cached_in"] if cache else rate["in"]); dyn = (tok["context"] + tok["history"] + tok["question"]) / 1e6 * rate["in"]; out = tok["answer"] / 1e6 * rate["out"]
    return {"system": sysc * steps, "input": dyn * steps, "output": out * steps, "total": (sysc + dyn + out) * steps}
def llm_cost(i: Intake, tier: str, pattern: str) -> dict:
    R = content("llm_rates"); P = content("patterns")["patterns"][pattern]; tok = {**P["tokens"], **(i.tokens or {})}
    if pattern == "classical_ml" and not i.tokens: return {"applicable": False, "note": "Classical ML: no token cost. Serving cost is in the infrastructure line.", "monthly_expected": 0.0, "annual_expected": 0.0, "per_request": 0.0, "scenarios": [], "breakdown": [], "growth": [], "models": [], "fixed_lines": [], "controls": [], "tokens": tok}
    if i.model not in R["models"]: raise ValueError(f"model must be one of {list(R['models'])}")
    rate = R["models"][i.model]; pr = per_request(rate, tok, i.cache_system_prompt); over = 1 + (R["overheads"]["retries_pct"] + R["overheads"]["guardrail_calls_pct"]) / 100
    cheap = per_request(R["models"]["cheap"], {**tok, "context": int(tok["context"] * 0.4), "steps": 1}, i.cache_system_prompt)["total"]; blended = (pr["total"] * (1 - i.cheap_route_share) + cheap * i.cheap_route_share) * over
    fixed = [{"line": "Embeddings (index refresh, ~20M tokens/month)", "monthly": round(20 * R["embeddings_per_1m_tokens"], 2)} if pattern in ("rag", "multi_agent", "agent") else None, {"line": "Vector store", "monthly": R["vector_store_monthly_usd"][tier]} if pattern in ("rag", "multi_agent", "agent") else None,
             {"line": "Evaluation runs", "monthly": R["eval_runs_monthly_usd"][tier]}, {"line": "Self-hosted GPU (fixed)", "monthly": rate.get("fixed_monthly_usd", 0)} if rate.get("fixed_monthly_usd") else None]
    fixed = [x for x in fixed if x]; fx = sum(x["monthly"] for x in fixed)
    scen = [{"scenario": k, "requests_per_day": int(i.requests_per_day * m), "monthly": round(blended * i.requests_per_day * m * 30 + fx, 2), "annual": round((blended * i.requests_per_day * m * 30 + fx) * 12, 2)} for k, m in R["scenarios"].items()]
    g = i.monthly_growth_pct / 100; growth = [{"month": m, "requests_per_day": int(i.requests_per_day * (1 + g) ** (m - 1)), "monthly": round(blended * i.requests_per_day * (1 + g) ** (m - 1) * 30 + fx, 2)} for m in (1, 6, 12, 24, 36)]
    yr = [sum(blended * i.requests_per_day * (1 + g) ** (m - 1) * 30 + fx for m in range(a, a + 12)) for a in (1, 13, 25)]
    models = [{"model": v["title"], "per_request": round(per_request(v, tok, i.cache_system_prompt)["total"] * over, 5), "monthly": round(per_request(v, tok, i.cache_system_prompt)["total"] * over * i.requests_per_day * 30 + fx + v.get("fixed_monthly_usd", 0) * (k != i.model), 2)} for k, v in R["models"].items()]
    base = blended * i.requests_per_day * 30
    def alt(**kw): t2 = {**tok, **kw}; return (per_request(rate, t2, i.cache_system_prompt)["total"] * (1 - i.cheap_route_share) + cheap * i.cheap_route_share) * over * i.requests_per_day * 30
    sens = sorted([{"assumption": n, "minus_50": round(a, 2), "plus_50": round(b, 2), "swing": round(b - a, 2)} for n, a, b in (("requests per day", base * .5, base * 1.5), ("retrieved context tokens", alt(context=int(tok["context"] * .5)), alt(context=int(tok["context"] * 1.5))),
                   ("answer tokens", alt(answer=int(tok["answer"] * .5)), alt(answer=int(tok["answer"] * 1.5))), ("chat history tokens", alt(history=int(tok["history"] * .5)), alt(history=int(tok["history"] * 1.5))))], key=lambda x: -x["swing"])
    nocache = per_request(rate, tok, False)["total"] * over * i.requests_per_day * 30; trimmed = alt(history=min(tok["history"], 1500)); routed = (pr["total"] * 0.45 + cheap * 0.55) * over * i.requests_per_day * 30
    controls = [{"control": "Prompt caching of the system prompt", "monthly_saving": round(nocache - per_request(rate, tok, True)["total"] * over * i.requests_per_day * 30, 2), "status": "on" if i.cache_system_prompt else "OFF — switch on"},
                {"control": "Route ~55% simple requests to the cheap model", "monthly_saving": round(max(0, base - routed), 2), "status": f"{i.cheap_route_share:.0%} routed today"}, {"control": "Trim chat history to 1,500 tokens", "monthly_saving": round(max(0, base - trimmed), 2), "status": "check"},
                {"control": "Output limit (−30% answer tokens)", "monthly_saving": round(base - alt(answer=int(tok["answer"] * .7)), 2), "status": "check"}, {"control": "Batch API for offline jobs (~50% off that share)", "monthly_saving": None, "status": "applies to reports, backfills, evals"}]
    depth = {"bronze": 1, "silver": 3, "gold": 3}[tier]
    return {"applicable": True, "model": rate["title"], "tokens": tok, "per_request": round(blended, 5), "breakdown": [{"part": k, "usd": round(v, 5), "share": round(v / pr["total"], 3) if pr["total"] else 0} for k, v in pr.items() if k != "total"],
            "overheads_pct": R["overheads"], "fixed_lines": fixed, "scenarios": scen if depth == 3 else [s for s in scen if s["scenario"] == "expected"], "monthly_expected": scen[1]["monthly"], "annual_expected": scen[1]["annual"],
            "growth": growth if tier == "gold" else [], "yearly_with_growth": [round(y, 2) for y in yr], "sensitivity": sens if tier == "gold" else sens[:2], "models": models, "controls": controls, "rates_verified": R["verified"], "note": R["source_note"]}

# ── M8 project cost calculator ──────────────────────────────────────────────────────────────────────────────────────
def project_cost(i: Intake, tier: str, r: dict, pl: dict, est: dict, llm: dict) -> dict:
    rc = content("rate_card"); pricing = yaml.safe_load((settings.pricing_dir / "tiers.yaml").read_text()); fx = rc["fx"].get(i.currency, 1.0)
    mult = max(rc["size_multiplier_floor"], pricing["size_multiplier"].get(i.company_size, 1.0)); people = []; tot = 0.0
    for role, days in est["role_days"].items():
        rate = rc["roles"][role]["day_rate_usd"] * mult; people.append({"role": rc["roles"][role]["title"], "days": days, "day_rate": round(rate * fx), "cost": round(days * rate * fx)}); tot += days * rate
    cont = tot * est["contingency_pct"] / 100; tools = rc["tools_and_licences_usd"][tier]; comp = rc["compliance_usd"].get(r["risk_tier"], 0); build = tot + cont + tools + comp
    sd_share = est["sigma_days"] / est["expected_days"] if est["expected_days"] else 0.15; lo, hi = build * (1 - 1.28 * sd_share), build * (1 + 1.28 * sd_share)
    infra = content("patterns")["patterns"][pl["pattern"]]["infra_monthly_usd"][tier]; support = build * rc["support_pct_of_build_per_year"][tier] / 12; retrain = rc["retrain_refresh_usd_per_year"][pl["pattern"]]
    run_m = llm["monthly_expected"] + infra + support; yl = llm.get("yearly_with_growth") or [llm["monthly_expected"] * 12] * 3; tco = build + sum(yl) + 36 * (infra + support) + 3 * retrain
    lines = [{"line": "People (build)", "usd": tot, "source": "M6 effort × rate card × company-size multiplier " + str(mult)}, {"line": f"Contingency ({est['contingency_pct']}%, {est['risk_profile']} risk profile)", "usd": cont, "source": "M6"},
             {"line": "Tools and licences", "usd": tools, "source": "rate_card.yaml by tier"}, {"line": f"Compliance and assurance ({r['risk_tier']} risk)", "usd": comp, "source": "rate_card.yaml by risk tier"}]
    sw = est["by_stage"]; tot_days = sum(s["person_days"] for s in sw) or 1; acc = {"Initiate": .75, "POC": .4, "Pilot / MVP": .2, "Production": .1, "Scale": .1}
    by_stage = [{"stage": s["stage"], "expected": round(build * s["person_days"] / tot_days * fx), "low": round(build * s["person_days"] / tot_days * (1 - acc[s["stage"]] * .5) * fx), "high": round(build * s["person_days"] / tot_days * (1 + acc[s["stage"]]) * fx), "accuracy": s["accuracy"]} for s in sw]
    out = {"currency": i.currency, "fx": fx, "size_multiplier": mult, "people": people, "build_lines": [{**l, "amount": round(l["usd"] * fx)} for l in lines], "build_expected": round(build * fx), "build_range": [sum(x["low"] for x in by_stage), sum(x["high"] for x in by_stage)], "build_range_basis": "cone of uncertainty by stage — narrows at every gate", "build_range_pert_80": [round(lo * fx), round(hi * fx)], "by_stage": by_stage,
           "run_monthly": {"llm": round(llm["monthly_expected"] * fx), "infrastructure": round(infra * fx), "support": round(support * fx), "total": round(run_m * fx)}, "retrain_refresh_per_year": round(retrain * fx),
           "tco_3y": round(tco * fx), "milestones": [{"milestone": m, "pct": p, "amount": round(build * p / 100 * fx)} for m, p in rc["payment_milestones"][tier]], "rate_card_status": rc["status"]}
    if tier == "bronze": out["tco_12m"] = round((build + 12 * run_m + retrain) * fx)
    if i.annual_benefit_usd > 0:
        ramp = (0.5, 1.0, 1.0); run_y = [yl[y] + 12 * (infra + support) + retrain for y in range(3)]; cash = [-build] + [i.annual_benefit_usd * ramp[y] - run_y[y] for y in range(3)]; ben = sum(i.annual_benefit_usd * x for x in ramp); cost3 = build + sum(run_y)
        cum, pay = -build, None
        for y in range(3):
            if pay is None and cash[y + 1] > 0 and cum + cash[y + 1] >= 0: pay = round((y + (-cum) / cash[y + 1]) * 12, 1)
            cum += cash[y + 1]
        out["roi"] = {"annual_benefit": round(i.annual_benefit_usd * fx), "ramp": list(ramp), "cashflows": [round(c * fx) for c in cash], "roi_3y_pct": round((ben - cost3) / cost3 * 100, 1), "npv_10pct": round(sum(c / 1.1 ** n for n, c in enumerate(cash)) * fx), "payback_months": pay,
                      "sensitivity": [{"case": f"benefit at {int(s * 100)}%", "roi_3y_pct": round((ben * s - cost3) / cost3 * 100, 1)} for s in (0.6, 0.8, 1.0, 1.2)] if tier == "gold" else []}
    else: out["roi"] = {"note": "No annual benefit supplied — ROI not computed. Add annual_benefit_usd at intake."}
    return out

# ── M9 governance planner ───────────────────────────────────────────────────────────────────────────────────────────
def governance_plan(i: Intake, sz: dict, r: dict) -> dict:
    depth = sz["depth"]["governance"]; ctrls = [{"id": c["id"], "control": c["title"], "nist": c["nist"], "iso42001": c["iso42001"], "eu_ai_act": c["eu_ai_act"], "evidence": c["evidence"]} for c in r["required_controls"]]
    reg = []; j = " ".join(i.jurisdictions).lower()
    if i.processes_personal_data and ("india" in j or "dpdp" in j): reg.append("India DPDP Act 2023 and DPDP Rules: notice and consent basis, purpose limitation, data principal rights, breach notification, significant data fiduciary check")
    if i.processes_personal_data and ("eu" in j or "gdpr" in j or "uk" in j): reg.append("GDPR: lawful basis, DPIA for high-risk processing, Art. 22 automated decisions, transfers, processor terms")
    if "eu" in j: reg.append(f"EU AI Act: obligations for a '{r['risk_tier']}' risk system depend on role (provider/deployer) and phase-in dates — confirm current applicability with counsel")
    if not reg: reg.append("No personal-data regime triggered by the intake answers — reconfirm at G0")
    extras = [x for x, on in (("Data protection impact assessment (DPIA)", r["risk_tier"] == "high" or depth == "gold"), ("Model / system card", r["risk_tier"] == "high" or depth == "gold"), ("Vendor and third-party model assessment", r["risk_tier"] == "high" or depth == "gold")) if on]
    gate_ev = [{"gate": "G0", "evidence": "Risk pre-screen, risk tier, data classification, applicable regulations listed"}, {"gate": "G1", "evidence": "Lawful basis for POC data confirmed; no production data outside approved environments"},
               {"gate": "G2", "evidence": "Evaluation results incl. safety metrics; DPIA and model card drafted where required; threat model complete"}, {"gate": "G3", "evidence": "Controls implemented and tested; sign-offs recorded; monitoring and incident process live"}, {"gate": "G4", "evidence": "Risk re-tiered per new use or region; vendor review refreshed"}]
    out = {"risk_tier": r["risk_tier"], "drivers": r["drivers"], "depth": depth, "controls": ctrls if depth != "bronze" else ctrls[:8], "controls_total": len(ctrls), "regulatory_checks": reg, "extra_deliverables": extras, "gate_evidence": gate_ev,
           "oversight": {"high": "Human oversight with authority to override; explainability, bias testing and named sign-offs before production.", "limited": "Transparency notice, guardrails, monitoring and evaluation.", "minimal": "Baseline controls and light review."}.get(r["risk_tier"], ""),
           "disclaimer": "Framework-aligned guidance, not legal advice. Regulatory dates and obligations must be re-verified with counsel before they are quoted to a client."}
    if depth in ("silver", "gold"):
        req = gov.GovernanceRequest(organisation=i.client, industry=i.industry, size=i.company_size, jurisdictions=i.jurisdictions, systems=[gov.AISystem(name=i.project, purpose=i.problem, **{k: getattr(i, k) for k in ("affects_individuals_rights", "uses_biometrics_or_surveillance",
              "safety_critical", "interacts_with_public", "generates_content", "processes_personal_data", "fully_automated_decisions", "manipulative_or_social_scoring")})])
        a = gov.analyse(req); out["roadmap_30_60_90"] = {k: [str(x) for x in v][: (6 if depth == "silver" else 12)] for k, v in a.get("roadmap", {}).items() if v}
    return out

# ── M10 security planner ────────────────────────────────────────────────────────────────────────────────────────────
def security_plan(i: Intake, sz: dict, pattern: str) -> dict:
    lib = content("security_controls")["controls"]; depth = sz["depth"]["security"]; di = TIER_ORDER.index(depth); rc = content("rate_card")["roles"]; flags = {"pii": i.processes_personal_data, "public": i.interacts_with_public, "write_actions": i.writes_to_production_systems or pattern in ("agent", "multi_agent")}
    sel = []
    for c in lib:
        if c["applies"] != "all" and pattern not in c["applies"]: continue
        if c.get("when") and not flags.get(c["when"]): continue
        ci = TIER_ORDER.index(c["tier"])
        if ci > di: continue
        sel.append({"id": c["id"], "control": c["title"], "threat": c["threat"], "due": c["due"], "owner": rc[c["owner"]]["title"], "evidence": c["evidence"], "form": "checklist item" if depth == "bronze" else "planned control with evidence" if depth == "gold" else "planned control"})
    threats = sorted({c["threat"] for c in sel}); data_class = content("tiers")["dimensions"][3]["options"][i.sizing.get("data_sensitivity", 1) - 1]
    tests = {"bronze": ["Checklist walk-through at G1 and G2", "Out-of-scope and refusal tests in the evaluation set"], "silver": ["Adversarial prompt set run before each release; attack success rate tracked", "Two-user permission test on retrieval", "Secrets scan in CI"],
             "gold": ["Red-team exercise against the full system before G3", "Penetration test scope covering AI endpoints and tool integrations", "Adversarial prompt set in CI; attack success rate reported monthly", "Vendor assessment refreshed at G4"]}[depth]
    incident = {"bronze": [], "silver": ["Severity levels for AI failures (wrong answer, data leak, runaway action)", "Reporting path and first-hour actions", "Evidence preservation"], "gold": ["Full run-book: detection, triage, containment (kill switch, credential revocation), notification assessment by DPO, recovery, post-incident review", "Table-top exercise before go-live"]}[depth]
    return {"depth": depth, "pattern": pattern, "data_classification": data_class, "handling_rules": ["Classify every input and output", "Personal or confidential data only in approved tools and environments", "No production data in non-production without masking", "Retention and deletion rules apply to prompts, logs, indexes and embeddings"],
            "threats": threats, "controls": sel, "by_gate": {g: [c["id"] for c in sel if c["due"] == g] for g in ("G0", "G1", "G2", "G3")}, "test_plan": tests, "incident_outline": incident,
            "reference": "Threat themes follow the OWASP Top 10 for LLM Applications and ISO/IEC 27001 control themes — verify current naming before citing."}

# ── M11 gates ───────────────────────────────────────────────────────────────────────────────────────────────────────
def gate_checklists(tier: str, depth_gov: str = "") -> dict:
    G = content("gates")["gates"]; ti = max(TIER_ORDER.index(tier), TIER_ORDER.index(depth_gov) if depth_gov in TIER_ORDER else 0); mandatory = content("tiers")["tiers"][tier]["gates"]; out = {}
    for g, spec in G.items():
        crit = [c for c in spec["criteria"] if TIER_ORDER.index(c["tier"]) <= ti]
        if crit: out[g] = {"title": spec["title"], "question": spec["question"], "mandatory": g in mandatory, "criteria": crit}
    return out
def evaluate_gate(checklist: dict, met: list[str]) -> dict:
    crit = checklist["criteria"]; miss = [c for c in crit if c["id"] not in met]; block = [c for c in miss if c["blocking"]]
    rec = "go" if not miss else "no_go" if block else "conditional_go"
    return {"met": len(crit) - len(miss), "total": len(crit), "missing": [c["id"] + " " + c["text"] for c in miss], "blocking_missing": [c["id"] for c in block], "recommendation": rec,
            "rationale": "All criteria evidenced." if rec == "go" else "Blocking criteria missing: " + ", ".join(c["id"] for c in block) if block else "Only non-blocking criteria open — proceed with written conditions and dates."}

# ── Orchestration ───────────────────────────────────────────────────────────────────────────────────────────────────
def run(i: Intake) -> dict:
    r = risk(i); sz = size(i, r)
    if sz["stop"]: return {"stop": True, "client": i.client, "project": i.project, "sizing": sz, "risk": {k: v for k, v in r.items() if k != "required_controls"},
                           "decline_note": f"The intended use of '{i.project}' falls in the PROHIBITED risk tier ({', '.join(r['drivers']) or 'manipulative or social scoring'}). uniAIverse does not deliver this use. No estimate or pack is produced. We can help redesign the use case so that it does not score or manipulate people.", "stamp": stamp()}
    rd = readiness(i); pl = plan(i, sz, rd); est = estimate(i, sz, r, rd, pl); llm = llm_cost(i, sz["tier"], pl["pattern"]); pc = project_cost(i, sz["tier"], r, pl, est, llm)
    from .documents import catalogue
    return {"stop": False, "client": i.client, "project": i.project, "tier": sz["tier"], "sizing": sz, "readiness": rd, "plan": pl, "estimate": est, "llm_cost": llm, "project_cost": pc, "governance": governance_plan(i, sz, r),
            "security": security_plan(i, sz, pl["pattern"]), "gates": gate_checklists(sz["tier"], sz["depth"]["governance"]), "deliverables": catalogue(sz, r), "overrides": [o.model_dump() for o in i.overrides], "stale_content": staleness(), "stamp": stamp(),
            "status": "DRAFT — every pack is a draft until a named reviewer approves it. The SOW always needs human and legal review."}
