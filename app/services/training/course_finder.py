"""Course Finder — profile / CV → best track and courses, with why / what / how / when.

Free tier: track + one course + short 'why'. Paid tier: full path, gap analysis, week-by-week plan,
capstone, mentor plan. Works rule-based; LLM (if configured) adds a personalised narrative.
"""
from __future__ import annotations
import re
import yaml
from pydantic import BaseModel, Field
from app.core import llm
from app.core.config import settings

CUR = settings.materials_dir / "curriculum.yaml"

class Profile(BaseModel):
    name: str | None = None
    tier: str = Field("free", description="free | paid")
    current_role: str = Field("", examples=["Business analyst", "Student", "Backend developer"])
    education: str = Field("", examples=["B.Tech CS", "MBA", "BCom"])
    years_experience: float = 0
    programming: list[str] = Field(default_factory=list, description="languages you can actually write, e.g. python, javascript")
    tech_stack: list[str] = Field(default_factory=list, description="tools/frameworks: sql, react, aws, pandas, langchain ...")
    interests: list[str] = Field(default_factory=list, description="e.g. build chatbots, lead AI projects, sales, marketing, governance, data")
    goal: str = Field("", description="What do you want in 6-12 months?")
    hours_per_week: float = 5
    cv_text: str | None = Field(None, description="Paste your CV / LinkedIn summary (optional)")

KEYWORDS = {
    "coding":     ["python", "java", "javascript", "typescript", "c#", "go", "rust", "sql", "developer", "engineer", "software", "backend", "frontend", "api", "git"],
    "data":       ["data", "sql", "pandas", "spark", "warehouse", "analytics", "etl", "pipeline", "dbt", "snowflake", "bigquery", "excel", "power bi", "tableau"],
    "ml":         ["machine learning", "ml", "scikit", "sklearn", "tensorflow", "pytorch", "model", "regression", "classification", "mlops", "mlflow"],
    "genai":      ["llm", "gpt", "claude", "openai", "langchain", "llamaindex", "rag", "vector", "embedding", "prompt", "agent", "chatbot", "genai", "generative"],
    "leadership": ["manager", "head", "director", "founder", "ceo", "cto", "cxo", "lead", "strategy", "board", "vp", "owner"],
    "business":   ["analyst", "consultant", "operations", "process", "product", "project", "mba", "finance", "hr", "pmo"],
    "sales":      ["sales", "account", "sdr", "bdr", "revenue", "crm", "pipeline", "quota", "prospect"],
    "marketing":  ["marketing", "content", "seo", "campaign", "brand", "social media", "growth", "copy"],
    "governance": ["compliance", "risk", "legal", "audit", "privacy", "gdpr", "security", "governance", "policy", "regulat"],
    "student":    ["student", "fresher", "graduate", "intern", "bachelor", "b.tech", "bsc", "final year", "campus"],
}

def _signals(p: Profile) -> dict[str, float]:
    text = " ".join([p.current_role, p.education, p.goal, " ".join(p.programming), " ".join(p.tech_stack),
                     " ".join(p.interests), p.cv_text or ""]).lower()
    s = {k: 0.0 for k in KEYWORDS}
    for k, words in KEYWORDS.items():
        s[k] = sum(len(re.findall(r"\b" + re.escape(w), text)) for w in words)
    s["coding"] += 3 * len(p.programming)
    s["data"] += sum(1 for t in p.tech_stack if t.lower() in KEYWORDS["data"])
    if p.years_experience == 0 and p.cv_text:   # infer experience from CV if not given
        m = re.search(r"(\d{1,2})\+?\s*(?:years|yrs)", text)
        if m: p.years_experience = float(m.group(1))
    if p.years_experience >= 8: s["leadership"] += 2
    if p.years_experience == 0: s["student"] += 2
    return s

def _choose_track(s: dict[str, float], p: Profile) -> tuple[str, str]:
    codes = s["coding"] >= 3
    if s["governance"] >= 2 and not codes:
        return "governance", "your background is in risk, compliance or legal — governance is where that expertise becomes an AI role."
    if s["sales"] >= 2 and not codes:
        return "sales", "your profile is sales-led; the fastest value is AI applied to prospecting, calls and proposals."
    if s["marketing"] >= 2 and not codes:
        return "marketing", "your profile is marketing-led; AI content and campaign workflows give immediate results."
    if codes and (s["genai"] >= 2 or "chatbot" in p.goal.lower() or "llm" in p.goal.lower() or "genai" in p.goal.lower()):
        return "genai_engineer", "you can code and you're already circling LLMs, RAG or agents — this is the direct path."
    if s["student"] >= 2 and p.years_experience < 1:
        return "professional", "you're early-career; the professional track builds foundations, a portfolio project and a certificate employers can check."
    if codes and s["data"] >= 3 and s["ml"] >= 1:
        return "data_mlops", "you code and work with data — MLOps and AI-ready data are the highest-demand combination."
    if codes:
        return "engineer", "you can write code; the AI Engineer track turns that into shippable AI features first, GenAI next."
    if s["leadership"] >= 3:
        return "leadership", "you lead teams or budgets; you need to prioritise, fund and govern AI, not build it."
    if s["student"] >= 2:
        return "professional", "you're early-career; the professional track builds foundations, a portfolio project and a certificate."
    if s["business"] >= 2 or p.years_experience >= 2:
        return "business", "you work with processes and stakeholders — you'll own AI use cases rather than engineer them."
    return "everyone", "start with foundations; your profile doesn't yet point to a specialism, and that's fine."

def _gaps(track: str, s: dict[str, float], p: Profile) -> list[str]:
    g = []
    if track in {"genai_engineer", "engineer", "data_mlops"}:
        if "python" not in [x.lower() for x in p.programming]: g.append("Python is required — add a 2-week Python refresher before module 1")
        if s["data"] < 2: g.append("SQL and basic data handling — cover before the data modules")
        if track == "genai_engineer" and s["genai"] < 1: g.append("No LLM exposure yet — do the non-technical RAG course first to build intuition")
    if track in {"business", "leadership", "professional"} and s["genai"] < 1:
        g.append("Build hands-on intuition with the no-code RAG course before strategy modules")
    if track == "governance" and s["genai"] < 1:
        g.append("Take AI for All first — you must understand how models fail to govern them")
    if p.hours_per_week < 3: g.append("Under 3h/week — choose the self-paced format and expect roughly double the calendar time")
    return g

def find(p: Profile) -> dict:
    cur = yaml.safe_load(CUR.read_text())
    by_id = {c["id"]: c for c in cur["courses"]}
    s = _signals(p)
    track_id, why = _choose_track(s, p)
    track = next(t for t in cur["tracks"] if t["id"] == track_id)
    path = [by_id[i] for i in track["courses"] if i in by_id]
    first = path[0]
    # skip ai-for-all if clearly experienced with genai
    if first["id"] == "ai-for-all" and s["genai"] >= 3 and len(path) > 1:
        first = path[1]
    total_hours = sum(c["hours"] for c in path)
    weeks = max(1, round(total_hours / max(1, p.hours_per_week)))
    base = {
        "tier": p.tier, "name": p.name,
        "track": {"id": track["id"], "title": track["title"], "audience": track["audience"]},
        "why": f"Recommended because {why}",
        "first_course": {"id": first["id"], "title": first["title"], "hours": first["hours"], "level": first["level"],
                         "what": first["outcomes"][:2]},
        "when": f"Start with {first['title']} ({first['hours']}h). At {p.hours_per_week}h/week the full {track['title']} track takes about {weeks} weeks.",
        "signals": {k: v for k, v in s.items() if v},
    }
    if p.tier != "paid":
        base["locked"] = ["Full learning path with all courses and modules", "Skills gap analysis and prerequisite plan",
                          "Week-by-week study plan", "Capstone project matched to your CV", "Mentor plan and certification route",
                          "Alternative tracks and why they scored lower"]
        base["upgrade"] = "Professional tier ($900): full personalised path, 8 mentor sessions, capstone review and certificate. Or a free 20-minute call to discuss."
        return base
    # paid detail
    gaps = _gaps(track_id, s, p)
    plan, week, budget = [], 1, 0.0
    for c in path:
        for m in c["modules"]:
            budget += m["hours"]
            plan.append({"week": week, "course": c["title"], "module": m["title"], "hours": m["hours"], "lab": m.get("lab")})
            if budget >= p.hours_per_week:
                week += 1; budget = 0
    alternatives = []
    for t in cur["tracks"]:
        if t["id"] != track_id and t["id"] in {"business", "engineer", "genai_engineer", "data_mlops", "governance", "professional"}:
            alternatives.append({"track": t["title"], "why_not_first": "scored lower on your current signals; revisit after the first course"})
    capstone = {
        "genai_engineer": "A grounded knowledge assistant over documents from your current/target industry, with a 50-question eval set.",
        "engineer": "An AI feature shipped as an API with tests, CI, monitoring and rollback — on a dataset from your domain.",
        "data_mlops": "A monitored data pipeline + model registry with drift alerts for one use case.",
        "business": "An AI use-case business case + no-code prototype for a real process from your workplace.",
        "leadership": "A 12-month AI roadmap and governance quick-start for your organisation.",
        "governance": "An AI inventory, risk classification and gap assessment for a real or simulated company.",
        "sales": "A personal AI sales playbook with measured research-time and reply-rate improvements.",
        "marketing": "An AI content SOP with brand-voice kit and pre-publish checklist.",
        "professional": "A portfolio project: a working RAG bot with test sheet and cost estimate, published on GitHub.",
        "everyone": "Five automated weekly workflows with verification notes.",
    }[track_id]
    narrative = llm.complete(
        f"Write 120 words of personalised guidance for this learner. Profile: {p.model_dump(exclude={'cv_text'})}. "
        f"Track: {track['title']}. Path: {[c['title'] for c in path]}. Gaps: {gaps}. Plain, encouraging, specific, no bullets.") or (
        f"{why[0].upper() + why[1:]} Follow the path in order, close the gaps listed before the technical modules, and treat the capstone as a portfolio piece.")
    base.update({
        "full_path": [{"id": c["id"], "title": c["title"], "hours": c["hours"], "level": c["level"], "certification": c["certification"],
                       "prerequisites": c["prerequisites"], "outcomes": c["outcomes"]} for c in path],
        "how": {"formats": sorted({f for c in path for f in c["formats"]}), "total_hours": total_hours, "estimated_weeks": weeks,
                "study_rhythm": f"{p.hours_per_week}h/week: one module per sitting, lab immediately after, review notes weekly"},
        "gap_analysis": gaps, "week_by_week": plan, "capstone": capstone,
        "mentor_plan": "Weekly 60-minute session: 20 min review of last lab, 30 min unblock, 10 min plan next week. Capstone reviewed against the Definition of Done.",
        "certification_route": [c["certification"] for c in path][-1],
        "alternatives": alternatives, "narrative": narrative,
    })
    return base
