from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)

def test_health_lists_services():
    ids = {s["id"] for s in c.get("/api/health").json()["services"]}
    assert {"readiness_audit", "training", "pricing", "strategy", "governance", "automation"} <= ids

def test_framework_counts():
    f = c.get("/api/readiness_audit/framework").json()
    assert len(f["domains"]) == 10 and sum(len(d["capabilities"]) for d in f["domains"]) == 51
    t = f["tiers"]; assert t["free"] < t["bronze"] < t["silver"] < t["gold"] < t["platinum"] and t["platinum"] >= 300

def test_free_tier_no_pdf_and_upgrade_hint():
    s = c.get("/api/readiness_audit/sample?tier=free").json()
    r = c.post("/api/readiness_audit/run", json=s).json()
    assert r["report_pdf_url"] is None and r["upgrade_hint"] and len(r["recommendations"]) == 3

def test_bronze_to_platinum_end_to_end():
    for tier in ["bronze", "silver", "gold", "platinum"]:
        s = c.get(f"/api/readiness_audit/sample?tier={tier}&industries=financial_services").json()
        r = c.post("/api/readiness_audit/run", json=s); assert r.status_code == 200, r.text
        b = r.json()
        assert 0 <= b["overall_score"] <= 100 and len(b["dimensions"]) == 10
        assert c.get(b["report_pdf_url"]).status_code == 200
        if tier != "bronze":
            assert b["industry_modules"] and b["benchmark"]

def test_rejects_answer_outside_tier():
    s = c.get("/api/readiness_audit/sample?tier=free").json()
    s["answers"]["strategy.vision.7"] = 3          # a Platinum question
    assert c.post("/api/readiness_audit/run", json=s).status_code == 400

def test_perfect_score_is_leading_and_no_red_flags():
    s = c.get("/api/readiness_audit/sample?tier=bronze").json()
    s["answers"] = {k: 4 for k in s["answers"]}
    r = c.post("/api/readiness_audit/run", json=s).json()
    assert r["maturity_level"] == "Leading" and r["red_flags"] == []

def test_curriculum_integrity():
    cur = c.get("/api/training/curriculum").json()
    ids = {x["id"] for x in cur["courses"]}
    assert cur["summary"]["courses"] >= 20 and not cur["summary"]["stale_courses"]
    for t in cur["tracks"]:
        assert set(t["courses"]) <= ids, t
    for co in cur["courses"]:
        assert set(co["prerequisites"]) <= ids and co["modules"] and co["outcomes"]
    assert c.get("/api/training/course/agentic-engineer").json()["outline_markdown"].startswith("# Agentic")
    assert c.get("/api/training/by-tier/bronze").json()["total_hours"] > 0

def test_pricing_quote_and_proposal():
    assert c.get("/api/pricing/quote?service=readiness_audit&tier=silver&company_size=medium").json()["quoted_price_usd"] == 8400
    assert c.get("/api/pricing/quote?service=readiness_audit&tier=free").json()["quoted_price_usd"] == 0
    p = c.get("/api/pricing/proposal?service=strategy&tier=gold&company_size=large&client_name=Acme").json()
    assert p["deliverables"] and p["phases"] and p["price_usd"] == 80000

def test_blueprint_consistency():
    bp = c.get("/api/pricing/blueprint").json(); tiers = c.get("/api/pricing/tiers").json()
    for svc, spec in bp["services"].items():
        for t in spec["tiers"]:
            assert t in tiers["services"][svc]["tiers"], (svc, t)

def test_strategy_governance_automation():
    r = c.post("/api/strategy/roadmap", json={"organisation": "Acme", "readiness_score": 32, "use_cases": [
        {"name": "Invoice extraction", "value": 4, "feasibility": 5, "risk": 2, "effort_weeks": 3},
        {"name": "Churn model", "value": 5, "feasibility": 2, "risk": 3, "effort_weeks": 10}]})
    assert r.json()["backlog"][0]["name"] == "Invoice extraction"
    assert c.post("/api/governance/classify", json={"use_case": "CV screening", "affects_individuals_rights": True}).json()["risk_tier"] == "high"
    assert c.post("/api/automation/roi", json={"build_cost": 10000, "monthly_run_cost": 200, "workflows": [
        {"name": "Invoices", "volume_per_month": 2000, "minutes_per_item": 6, "hourly_cost": 30}]}).json()["payback_months"] > 0

def test_course_finder_free_and_paid():
    for kind, track in [("developer", "genai_engineer"), ("student", "professional"), ("analyst", "business"), ("leader", "leadership"), ("compliance", "governance")]:
        p = c.get(f"/api/training/course-finder/sample?kind={kind}").json()
        r = c.post("/api/training/course-finder", json=p).json()
        assert r["track"]["id"] == track, (kind, r["track"], r["signals"])
        assert r["locked"] and "full_path" not in r
        p["tier"] = "paid"; r = c.post("/api/training/course-finder", json=p).json()
        assert r["full_path"] and r["week_by_week"] and r["capstone"]

def test_course_finder_cv_text():
    r = c.post("/api/training/course-finder", json={"cv_text": "Data engineer, 4 years. Python, SQL, Spark, Airflow, ML models with scikit-learn, MLflow.", "hours_per_week": 5}).json()
    assert r["track"]["id"] == "data_mlops"
