"""v2.7: integrated monitoring, founder hours, Platinum plan, operator console, design assets, Quest free tier."""
from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app
c = TestClient(app); H = {"X-Admin-Token": settings.admin_token}

def test_monitor_needs_admin_and_returns_every_section():
    assert c.get("/api/platform/monitor").status_code == 401
    m = c.get("/api/platform/monitor", headers=H).json()
    for k in ("services", "tenants", "gateway", "usage", "free_pool", "bot", "hours", "audit", "cost_model", "entitlements_mode"): assert k in m
    assert len(m["services"]) == 13 and all(s["id"] == "platform" and s["enabled"] for s in m["services"] if s["id"] == "platform")
    assert m["gateway"]["global_cap_inr"] > 0 and "queries_used" in m["free_pool"]

def test_hours_sheet_and_ceiling():
    assert c.post("/api/platform/hours", json={"person": "Sarfi", "day": "2026-09-26", "activity": "cohort delivery", "hours": 3.5, "note": "cohort 1 weekend 1"}, headers=H).json()["ok"]
    assert c.post("/api/platform/hours", json={"person": "Sarfi", "day": "2026-09-26", "activity": "sales", "hours": 30}, headers=H).status_code == 422
    h = c.get("/api/platform/hours?month=2026-09", headers=H).json(); p = next(x for x in h["by_person"] if x["person"] == "Sarfi")
    assert p["hours"] >= 3.5 and p["ceiling"] == 120 and p["opportunity_cost_inr"] >= 8750 and h["by_activity"][0]["hours"] > 0

def test_logs_endpoint():
    for k in ("audit", "gateway", "usage", "provisioning", "bot", "hours"): assert isinstance(c.get(f"/api/platform/monitor/logs?kind={k}", headers=H).json(), list)
    assert c.get("/api/platform/monitor/logs?kind=nope", headers=H).status_code == 404

def test_platinum_plan_is_applicable_and_costed():
    p = c.get("/api/platform/plans").json()["plans"]; assert list(p) == ["bronze", "silver", "gold", "platinum"] and p["platinum"]["platform_fee_inr"] > p["gold"]["platform_fee_inr"]
    r = c.post("/api/platform/register", json={"organisation": "Big Group", "contact_name": "CIO", "contact_email": "cio@biggroup-example.com", "requested_plan": "platinum", "purpose": "group programme"}).json(); tid = r["tenant_id"]
    a = c.post(f"/api/platform/approve/{tid}", json={"decided_by": "Sarfi"}, headers=H).json(); assert a["state"] == "PAYMENT_PENDING" and a["pay_product"] == "platform.platinum"
    assert "platform.platinum" in c.get("/api/payments/catalog").json()["items"]
    m = c.get("/api/platform/cost-model", headers=H).json(); assert m["plans"]["platinum"]["gross_margin_inr"] > 0

def test_console_monitor_pages_and_assets():
    for path in ("/console", "/monitor", "/platform", "/register", "/delivery", "/demos", "/tools", "/discovery", "/"): assert c.get(path).status_code == 200
    assert c.get("/assets/uav.css").status_code == 200 and c.get("/assets/nav.js").status_code == 200
    assert "/assets/uav.css" in c.get("/tools").text and "/assets/nav.js" in c.get("/quest").text

def test_quest_free_tier_has_more_questionnaires():
    t = c.get("/api/quest/topics?user_id=free-user-x").json(); unlocked = [x for x in t["topics"] if not x["locked"]] if isinstance(t, dict) else [x for x in t if not x["locked"]]
    assert len(unlocked) >= 4 and {"ai-basics", "genai", "rag", "prompt-engineering"} <= {x["id"] for x in unlocked}
