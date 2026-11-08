from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)

def test_health_lists_services():
    r = c.get("/api/health"); assert r.status_code == 200
    ids = {s["id"] for s in r.json()["services"]}
    assert {"readiness_audit", "training", "pricing"} <= ids

def test_readiness_audit_end_to_end():
    sample = c.get("/api/readiness_audit/sample").json()
    r = c.post("/api/readiness_audit/run", json=sample); assert r.status_code == 200, r.text
    body = r.json()
    assert 0 <= body["overall_score"] <= 100
    assert body["maturity_level"] in {"Nascent", "Emerging", "Developing", "Established", "Leading"}
    assert len(body["dimensions"]) == 6 and body["recommendations"]
    assert c.get(body["report_pdf_url"]).status_code == 200
    assert c.get(body["report_markdown_url"]).status_code == 200

def test_readiness_rejects_bad_answers():
    sample = c.get("/api/readiness_audit/sample").json()
    sample["answers"]["zzz"] = 9
    assert c.post("/api/readiness_audit/run", json=sample).status_code == 400

def test_perfect_score_is_leading():
    sample = c.get("/api/readiness_audit/sample").json()
    sample["answers"] = {k: 4 for k in sample["answers"]}
    assert c.post("/api/readiness_audit/run", json=sample).json()["maturity_level"] == "Leading"

def test_training_catalog_and_paths():
    cat = c.get("/api/training/catalog").json()
    assert len(cat["courses"]) == 9
    assert c.get("/api/training/course/genai-engineer").json()["outline_markdown"]
    assert c.post("/api/training/recommend?audience=engineer").status_code == 200

def test_pricing_quote():
    q = c.get("/api/pricing/quote?service=readiness_audit&tier=silver&company_size=medium").json()
    assert q["quoted_price_usd"] == 8400

def test_strategy_roadmap():
    r = c.post("/api/strategy/roadmap", json={"organisation": "Acme", "readiness_score": 32, "use_cases": [
        {"name": "Invoice extraction", "value": 4, "feasibility": 5, "risk": 2, "effort_weeks": 3},
        {"name": "Churn model", "value": 5, "feasibility": 2, "risk": 3, "effort_weeks": 10}]})
    assert r.status_code == 200 and r.json()["backlog"][0]["name"] == "Invoice extraction"

def test_governance_classify():
    r = c.post("/api/governance/classify", json={"use_case": "CV screening", "affects_individuals_rights": True, "processes_personal_data": True})
    assert r.json()["risk_tier"] == "high"

def test_automation_roi():
    r = c.post("/api/automation/roi", json={"build_cost": 10000, "monthly_run_cost": 200, "workflows": [
        {"name": "Invoice processing", "volume_per_month": 2000, "minutes_per_item": 6, "hourly_cost": 30}]})
    assert r.json()["payback_months"] and r.json()["payback_months"] > 0
