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

# ── v2.2: Quest, bot, payments, workshop ─────────────────────────────────────
def test_quest_free_tier_flow():
    t = c.get("/api/quest/topics?user_id=q1").json()
    assert t["tier"] == "free" and any(x["locked"] for x in t["topics"]) and not next(x for x in t["topics"] if x["id"] == "ai-basics")["locked"]
    q = c.get("/api/quest/quiz?topic=ai-basics&user_id=q1&n=5").json(); assert len(q["questions"]) == 5
    r = c.post("/api/quest/quiz/submit", json={"user_id": "q1", "topic": "ai-basics", "answers": {x["id"]: 0 for x in q["questions"]}}).json()
    assert r["total"] == 5 and "level" in r
    assert c.get("/api/quest/quiz?topic=agents&user_id=q1").status_code == 402
    assert c.get("/api/quest/challenges?user_id=q1").json()["locked"]

def test_quest_daily_limit_and_upgrade():
    for _ in range(3):
        q = c.get("/api/quest/quiz?topic=genai&user_id=q2").json()
        c.post("/api/quest/quiz/submit", json={"user_id": "q2", "topic": "genai", "answers": {x["id"]: 1 for x in q["questions"]}})
    assert c.get("/api/quest/quiz?topic=genai&user_id=q2").status_code == 402
    o = c.post("/api/payments/order", json={"product_id": "quest.silver", "customer_name": "Q", "customer_email": "q@x.io", "user_id": "q2"}).json()
    assert o["test_mode"] and o["methods"]["upi"] is True
    c.post("/api/payments/verify", json={"payment_id": o["payment_id"], "razorpay_order_id": o["order_id"], "razorpay_payment_id": "pay_t", "razorpay_signature": "s"})
    assert c.get("/api/quest/progress?user_id=q2").json()["tier"] == "silver"
    assert not c.get("/api/quest/challenges?user_id=q2").json()["locked"]

def test_payment_method_rule_and_bank_transfer():
    o = c.post("/api/payments/order", json={"product_id": "quest.gold", "customer_name": "G", "customer_email": "g@x.io"}).json()
    assert o["methods"]["upi"] is False and o["methods"]["bank_transfer"] is True
    b = c.post("/api/payments/bank-transfer", json={"product_id": "readiness_audit.bronze", "customer_name": "B", "customer_email": "b@x.io"}).json()
    assert b["status"] == "awaiting_transfer" and set(b["methods"]) == {"NEFT", "RTGS", "IMPS"}
    assert c.get(f"/api/payments/status/{b['payment_id']}").json()["status"] == "awaiting_transfer"

def test_bot_answers_site_questions():
    for msg, intent in [("how do I book an appointment", "book"), ("what is uniaiverse", "about"), ("which course is right for me", "course_finder")]:
        r = c.post("/api/bot/chat", json={"message": msg}).json()
        assert r["intent"] == intent and r["bot"] == "uniAI", (msg, r)
    assert c.post("/api/bot/chat", json={"message": "weather on mars"}).json()["intent"] is None

def test_admin_requires_token():
    assert c.get("/api/quest/admin/news/queue").status_code == 401
    assert c.post("/api/payments/admin/mark-paid/x").status_code == 401

def test_workshop_in_curriculum():
    r = c.get("/api/training/course/agentic-ai-workshop").json()
    assert r["hours"] == 16 and "WORKSHOP.md" in r["materials"] and r["outline_markdown"].startswith("# Agentic")
