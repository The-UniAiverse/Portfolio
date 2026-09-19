"""Governance engine: inventory → risk tiers → control gaps per system → organisation gap assessment → policy → remediation roadmap → PDF."""
from __future__ import annotations
import uuid
from datetime import date
from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from app.core import llm
from app.core.config import settings
from app.core.report import markdown_to_pdf

LIB = Path(__file__).with_name("controls.yaml")
def library() -> dict: return yaml.safe_load(LIB.read_text())

class AISystem(BaseModel):
    name: str
    owner: str = ""
    purpose: str = ""
    vendor_or_model: str = ""
    data_used: str = ""
    users_affected: str = ""
    status: str = Field("production", description="idea | pilot | production | retired")
    affects_individuals_rights: bool = False
    uses_biometrics_or_surveillance: bool = False
    safety_critical: bool = False
    interacts_with_public: bool = False
    generates_content: bool = False
    processes_personal_data: bool = False
    fully_automated_decisions: bool = False
    manipulative_or_social_scoring: bool = False
    controls_in_place: list[str] = Field(default_factory=list, description="control ids already evidenced, e.g. ['C01','C03']")

class GovernanceRequest(BaseModel):
    organisation: str
    industry: str = "General"
    size: str = "medium"
    policy_owner: str = "Head of Compliance"
    reviewers: str = "Compliance, Security, Engineering lead"
    jurisdictions: list[str] = Field(default_factory=lambda: ["India (DPDP)", "EU (GDPR, AI Act)"])
    gap_answers: dict[str, int] = Field(default_factory=dict, description="gap question id -> 0..4")
    systems: list[AISystem]

def classify(s: AISystem) -> str:
    env = s.model_dump()
    for r in library()["classification_rules"]:
        if eval(r["when"], {}, env): return r["tier"]
    return "minimal"

def analyse(req: GovernanceRequest) -> dict:
    lib = library(); controls = lib["controls"]
    inventory, all_gaps = [], []
    for s in req.systems:
        tier = classify(s)
        required = [c for c in controls if tier in c["tiers"]] if tier != "prohibited" else []
        missing = [c for c in required if c["id"] not in s.controls_in_place]
        if s.processes_personal_data and tier != "prohibited" and "C14" not in [c["id"] for c in required]:
            c14 = next(c for c in controls if c["id"] == "C14"); required.append(c14)
            if "C14" not in s.controls_in_place: missing.append(c14)
        cov = round(100 * (len(required) - len(missing)) / len(required)) if required else 0
        inventory.append({**s.model_dump(), "risk_tier": tier, "required_controls": [c["id"] for c in required],
                          "missing_controls": [{"id": c["id"], "title": c["title"], "evidence": c["evidence"]} for c in missing], "control_coverage_pct": cov})
        for c in missing: all_gaps.append((tier, s.name, c))
    # organisation gap assessment by NIST function
    by_fn: dict[str, list[int]] = {}
    for q in lib["gap_questions"]:
        if q["id"] in req.gap_answers: by_fn.setdefault(q["nist"], []).append(req.gap_answers[q["id"]])
    fn_scores = {k: round(100 * sum(v) / (4 * len(v))) for k, v in by_fn.items()}
    overall = round(sum(fn_scores.values()) / len(fn_scores)) if fn_scores else None
    tiers_count = {t: sum(1 for i in inventory if i["risk_tier"] == t) for t in lib["risk_tiers"]}
    # remediation: prohibited first, then high-risk missing controls, then org gaps <2, then limited
    order = {"prohibited": 0, "high": 1, "limited": 2, "minimal": 3}
    roadmap = {"30 days": [], "60 days": [], "90 days": [], "6 months": []}
    for i in inventory:
        if i["risk_tier"] == "prohibited": roadmap["30 days"].append(f"Stop / redesign '{i['name']}' — prohibited practice")
    for q in lib["gap_questions"]:
        a = req.gap_answers.get(q["id"])
        if a is not None and a <= 1: roadmap["30 days" if q["id"] in {"policy", "inventory", "classification"} else "60 days"].append(f"Organisation: {q['text'].rstrip('?')}")
    for tier, name, c in sorted(all_gaps, key=lambda x: order[x[0]]):
        h = "60 days" if tier == "high" else "90 days" if tier == "limited" else "6 months"
        roadmap[h].append(f"{name}: {c['title']} ({c['id']})")
    roadmap = {k: v for k, v in roadmap.items() if v}
    policy = lib["policy_template"].format(org=req.organisation, owner=req.policy_owner, date=date.today().isoformat(), reviewers=req.reviewers)
    return {"inventory": inventory, "tier_counts": tiers_count, "org_gap_scores": fn_scores, "org_gap_overall": overall,
            "control_library": [{"id": c["id"], "title": c["title"], "nist": c["nist"], "iso42001": c["iso42001"], "eu_ai_act": c["eu_ai_act"]} for c in controls],
            "roadmap": roadmap, "policy_markdown": policy}

def narrative(req: GovernanceRequest, a: dict) -> str:
    txt = llm.complete(f"Write a 170-word executive summary of this AI governance assessment for {req.organisation}. Tier counts: {a['tier_counts']}. "
                       f"Org gap scores by NIST function: {a['org_gap_scores']} (overall {a['org_gap_overall']}). Top 30-day actions: {a['roadmap'].get('30 days', [])[:4]}. Plain prose.")
    if txt: return txt.strip()
    hi = a["tier_counts"].get("high", 0); lim = a["tier_counts"].get("limited", 0); pro = a["tier_counts"].get("prohibited", 0)
    weakest = min(a["org_gap_scores"], key=a["org_gap_scores"].get) if a["org_gap_scores"] else "n/a"
    return (f"{req.organisation} operates {len(a['inventory'])} AI systems: {hi} high-risk, {lim} limited-risk, {a['tier_counts'].get('minimal', 0)} minimal"
            f"{f', and {pro} that must be stopped or redesigned' if pro else ''}. Governance maturity scores {a['org_gap_overall']}/100, weakest in the {weakest} function. "
            f"The first 30 days should establish the non-negotiables — policy, inventory and classification — and address any prohibited use; the following 60 days close the control gaps on high-risk systems, "
            f"where regulatory exposure is highest. The attached policy is ready for adoption, and the control library maps every gap to NIST AI RMF, ISO/IEC 42001 and the EU AI Act so audit evidence can be collected as work completes.")

def to_markdown(req: GovernanceRequest, a: dict, nar: str) -> str:
    lib = library()
    L = [f"# AI Governance, Safety & Compliance Assessment — {req.organisation}", f"*{req.industry} · {req.size} · Jurisdictions: {', '.join(req.jurisdictions)} · {date.today().isoformat()} · uniAIverse*", "",
         "## Executive summary", nar, "", "## AI inventory and risk classification", "",
         "| System | Owner | Purpose | Model / vendor | Status | Risk tier | Control coverage |", "|---|---|---|---|---|---|---|"]
    L += [f"| {i['name']} | {i['owner'] or '—'} | {i['purpose'] or '—'} | {i['vendor_or_model'] or '—'} | {i['status']} | **{lib['risk_tiers'][i['risk_tier']]['label']}** | {i['control_coverage_pct']}% |" for i in a["inventory"]]
    L += ["", "## Governance maturity (organisation level)", ""]
    if a["org_gap_scores"]:
        L += ["| NIST AI RMF function | Score |", "|---|---|"] + [f"| {k} | {v} |" for k, v in a["org_gap_scores"].items()] + [f"| **Overall** | **{a['org_gap_overall']}** |", ""]
    else: L += ["*Gap questionnaire not completed — organisation-level scores omitted.*", ""]
    L += ["## Control gaps by system"]
    for i in a["inventory"]:
        L += [f"### {i['name']} — {lib['risk_tiers'][i['risk_tier']]['label']}"]
        if i["risk_tier"] == "prohibited": L += ["> Prohibited practice. Do not deploy; redesign or retire.", ""]; continue
        L += ([f"- {c['id']} {c['title']} — *evidence: {c['evidence']}*" for c in i["missing_controls"]] or ["- All required controls evidenced."]) + [""]
    L += ["## Remediation roadmap"]
    for h, items in a["roadmap"].items(): L += [f"### {h}"] + [f"- {x}" for x in items] + [""]
    L += ["## Control library and framework mapping", "", "| ID | Control | NIST AI RMF | ISO/IEC 42001 | EU AI Act |", "|---|---|---|---|---|"]
    L += [f"| {c['id']} | {c['title']} | {c['nist']} | {c['iso42001']} | {c['eu_ai_act']} |" for c in a["control_library"]]
    L += ["", "---", "", a["policy_markdown"].replace("# Responsible AI Policy", "## Appendix — Responsible AI Policy (ready for adoption)"), "",
          "---", "*Framework-aligned guidance prepared by uniAIverse. Not legal advice; confirm obligations with counsel for your jurisdictions.*"]
    return "\n".join(L)

def run(req: GovernanceRequest) -> dict:
    a = analyse(req); nar = narrative(req, a); md = to_markdown(req, a, nar)
    rid = uuid.uuid4().hex[:10]; out = settings.outputs_dir / "governance"; out.mkdir(parents=True, exist_ok=True)
    (out / f"{rid}.md").write_text(md); (out / f"{rid}-policy.md").write_text(a["policy_markdown"]); markdown_to_pdf(md, out / f"{rid}.pdf")
    markdown_to_pdf(a["policy_markdown"], out / f"{rid}-policy.pdf")
    return {"report_id": rid, "organisation": req.organisation, "narrative": nar, **a,
            "report_markdown_url": f"/api/governance/report/{rid}.md", "report_pdf_url": f"/api/governance/report/{rid}.pdf",
            "policy_pdf_url": f"/api/governance/report/{rid}-policy.pdf"}
