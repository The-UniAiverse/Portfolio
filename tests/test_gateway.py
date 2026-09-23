"""LLM gateway + cohorts: identity → entitlement → per-user and cohort quotas → budget → rate limit → provider → metering → audit."""
import pytest
from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app
from app.services.platform import engine, gateway
c = TestClient(app); H = {"X-Admin-Token": settings.admin_token}
def cohort(seats=3, **over):
    r = c.post("/api/platform/cohorts", json={"name": "AI at Work — test", "track": "ai", "contact_email": "sarfi@uniaiverse-example.com", "starts": "2026-10-04", "ends": "2026-10-26", "seats": seats}, headers=H); assert r.status_code == 200, r.text
    j = r.json(); assert j["state"] == "ACTIVE" and j["api_key"]
    if over: c.patch(f"/api/platform/tenants/{j['cohort_id']}/limits", json={**over, "reason": "test override"}, headers=H)
    return j["cohort_id"], j["api_key"]

def test_cohort_is_admin_only_and_not_on_price_page():
    assert c.post("/api/platform/cohorts", json={"name": "Test cohort", "contact_email": "a@b.co", "starts": "2026-10-01", "ends": "2026-10-30"}).status_code == 401
    assert "platform.cohort" not in c.get("/api/payments/catalog").json()["items"] and "cohort" not in c.get("/api/platform/plans").json()["plans"]

def test_identity_chain_and_metering():
    cid, key = cohort(); T = {"X-Tenant-Key": key}
    assert c.post("/api/platform/llm/complete", json={"prompt": "hi"}).status_code == 401
    assert c.post("/api/platform/llm/complete", json={"prompt": "hi"}, headers=T).status_code == 403                                     # classroom needs a learner email
    assert c.post("/api/platform/llm/complete", json={"prompt": "hi"}, headers={**T, "X-User-Email": "nobody@x.co"}).status_code == 403
    a = c.post(f"/api/platform/cohorts/{cid}/learners", json={"emails": ["asha@x.co", "ravi@x.co", "meena@x.co", "extra@x.co"]}, headers=H).json(); assert len(a["added"]) == 3 and "extra@x.co" in a["skipped"]
    r = c.post("/api/platform/llm/complete", json={"prompt": "Explain RAG in one line", "purpose": "lab-03"}, headers={**T, "X-User-Email": "asha@x.co"}); assert r.status_code == 200, r.text; b = r.json()
    assert b["model_class"] == "cheap" and b["cost_inr"] > 0 and b["your_calls_left_today"] == 39 and b["tokens_in"] > 0
    assert c.post("/api/platform/llm/complete", json={"prompt": "x", "model_class": "flagship"}, headers={**T, "X-User-Email": "asha@x.co"}).status_code == 402
    u = c.get("/api/platform/llm/usage", headers=T).json(); assert u["calls"] == 1 and u["users"][0]["user_email"] == "asha@x.co"
    adm = c.get(f"/api/platform/tenants/{cid}/llm", headers=H).json(); assert adm["cost_inr"] == u["cost_inr"] and adm["denied"] >= 1

def test_per_user_daily_cap_does_not_hit_other_users():
    cid, key = cohort(per_user_daily_queries=2); c.post(f"/api/platform/cohorts/{cid}/learners", json={"emails": ["a@x.co", "b@x.co"]}, headers=H)
    A = {"X-Tenant-Key": key, "X-User-Email": "a@x.co"}; B = {"X-Tenant-Key": key, "X-User-Email": "b@x.co"}
    codes = [c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=A).status_code for _ in range(3)]; assert codes == [200, 200, 402]
    assert "daily limit" in c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=A).json()["detail"]
    assert c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=B).status_code == 200

def test_cohort_budget_hard_stop_and_override():
    cid, key = cohort(monthly_spend_limit_inr=0.001); c.post(f"/api/platform/cohorts/{cid}/learners", json={"emails": ["a@x.co"]}, headers=H); A = {"X-Tenant-Key": key, "X-User-Email": "a@x.co"}
    assert c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=A).status_code == 200
    r = c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=A); assert r.status_code == 402 and "HARD STOP" in r.json()["detail"]
    c.patch(f"/api/platform/tenants/{cid}/limits", json={"monthly_spend_limit_inr": 1000, "reason": "override for the last session"}, headers=H)
    assert c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=A).status_code == 200
    d = c.get(f"/api/platform/tenants/{cid}", headers=H).json(); assert any(a["action"] == "llm_denied" for a in d["audit"]) and any(a["action"] == "limits_changed" for a in d["audit"])

def test_rate_limit_and_global_cap(monkeypatch):
    cid, key = cohort(); c.post(f"/api/platform/cohorts/{cid}/learners", json={"emails": ["a@x.co"]}, headers=H); A = {"X-Tenant-Key": key, "X-User-Email": "a@x.co"}
    gateway._rate.clear(); codes = [c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=A).status_code for _ in range(7)]; assert codes[:6] == [200] * 6 and codes[6] == 429
    gateway._rate.clear(); c.post("/api/platform/llm/global-cap?cap_inr=0.0001", headers=H); assert "platform-wide" in c.post("/api/platform/llm/complete", json={"prompt": "q"}, headers=A).json()["detail"]
    c.post("/api/platform/llm/global-cap?cap_inr=60000", headers=H)

def test_registries_and_prerequisites_are_served_and_consistent():
    r = c.get("/api/platform/registries").json(); assert r["tracks"]["tracks"]["development"]["status"] == "draft" and r["tracks"]["public_positioning"]["standalone_public_offerings"] == ["ai"]
    assert set(r["models"]["classes"]) == {"cheap", "mid", "flagship"} and all(t["status"] in r["tools"]["statuses"] for t in r["tools"]["tools"])
    pol = r["token_policy"]; plan = engine.plan_profile("cohort"); assert pol["allocation"]["pool_per_cohort_inr"] == plan["monthly_spend_limit_inr"] and pol["allocation"]["per_learner_daily_queries"] == plan["per_user_daily_queries"]
    assert c.get("/api/platform/corporate-prerequisites").status_code == 401 and "azure_openai" in c.get("/api/platform/corporate-prerequisites", headers=H).json()["stacks"]
