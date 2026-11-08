"""Map a candidate's missing skills to uniAIverse courses (training-materials/catalog.yaml)."""
from __future__ import annotations
import yaml
from app.core.config import settings

# Skill keyword (normalised, as freehire spells skills) -> course ids, most relevant first.
SKILL_COURSES: dict[str, list[str]] = {
    "python": ["ai-engineer"], "machine-learning": ["ai-engineer"], "ml": ["ai-engineer"],
    "deep-learning": ["ai-engineer"], "pytorch": ["ai-engineer"], "tensorflow": ["ai-engineer"],
    "scikit-learn": ["ai-engineer"], "data-science": ["ai-engineer"], "sql": ["ai-engineer"],
    "pandas": ["ai-engineer"], "statistics": ["ai-engineer"], "analytics": ["ai-engineer"],
    "llm": ["genai-engineer"], "genai": ["genai-engineer"], "generative-ai": ["genai-engineer"],
    "rag": ["genai-engineer", "rag-nontechnical"], "langchain": ["genai-engineer"], "openai": ["genai-engineer"],
    "prompt-engineering": ["genai-engineer", "ai-for-all"], "nlp": ["genai-engineer"], "ai": ["ai-for-all", "genai-engineer"],
    "vector-databases": ["genai-engineer"], "agents": ["genai-engineer"],
    "mlops": ["ai-lifecycle"], "docker": ["ai-lifecycle"], "kubernetes": ["ai-lifecycle"], "ci-cd": ["ai-lifecycle"],
    "devops": ["ai-lifecycle"], "aws": ["ai-lifecycle"], "azure": ["ai-lifecycle"], "gcp": ["ai-lifecycle"], "cloud": ["ai-lifecycle"],
    "automation": ["ai-for-business", "ai-for-all"], "chatgpt": ["ai-for-all"],
    "marketing": ["ai-for-marketing"], "seo": ["ai-for-marketing"], "content": ["ai-for-marketing"],
    "sales": ["ai-for-sales"], "crm": ["ai-for-sales"], "salesforce": ["ai-for-sales"],
    "stakeholder-management": ["ai-for-business"], "product-management": ["ai-for-business", "llm-cost"],
}


def for_skills(missing: list[str], limit: int = 3) -> list[dict]:
    """Courses that cover the missing skills, deduplicated, with the skills each one addresses."""
    catalog = {c["id"]: c for c in yaml.safe_load((settings.materials_dir / "catalog.yaml").read_text())["courses"]}
    picked: dict[str, list[str]] = {}
    for skill in missing:
        for cid in SKILL_COURSES.get(skill, []):
            if cid in catalog:
                picked.setdefault(cid, []).append(skill)
    ranked = sorted(picked.items(), key=lambda kv: -len(kv[1]))[:limit]
    return [{"id": cid, "title": catalog[cid]["title"], "hours": catalog[cid]["hours"], "covers": skills}
            for cid, skills in ranked]
