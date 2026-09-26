"""v2.8: services and stories, showcase, playground gate, news top-5, newsletter (dry-run), chat widget on every page, bot fallback flag."""
from fastapi.testclient import TestClient
from app.core.config import settings
from app.main import app
c = TestClient(app); H = {"X-Admin-Token": settings.admin_token}

def test_services_and_stories_from_content_with_live_prices():
    s = c.get("/api/site/services").json()["services"]; assert {x["id"] for x in s} >= {"readiness", "consulting", "delivery", "workshops", "training", "platform"}
    d = c.get("/api/site/services/delivery").json(); assert d["tiers"] and d["stories"] and d["stories"][0]["status"] == "illustrative"
    assert c.get("/api/site/services/nope").status_code == 404 and len(c.get("/api/site/stories").json()["stories"]) >= 4 and len(c.get("/api/site/showcase").json()["items"]) >= 5
    t = c.get("/api/site/services/training").json(); assert "not separate services" in t["note"]

def test_playground_trial_gate():
    P = {"X-Playground-Id": "pg_test_1"}; s = c.get("/api/site/playground/status", headers=P).json(); assert s["remaining_today"] == 5
    r = c.post("/api/site/playground/ask", json={"question": "How many days of annual leave do permanent employees get?"}, headers=P); assert r.status_code == 200, r.text; j = r.json(); assert j["answer"] and j["remaining_today"] == 4
    for _ in range(4): c.post("/api/site/playground/ask", json={"question": "What is the refund for a late delivery?"}, headers=P)
    r = c.post("/api/site/playground/ask", json={"question": "and claims?"}, headers=P); assert r.status_code == 402 and "Request access" in r.json()["detail"]
    assert c.get("/api/site/playground/status", headers={"X-Playground-Id": "pg_test_2"}).json()["remaining_today"] == 5

def test_news_top5_and_newsletter_dry_run():
    n = c.get("/api/site/news").json(); assert "items" in n and len(n["items"]) <= 5
    r = c.post("/api/site/newsletter/subscribe", json={"email": "reader@example-news.com", "name": "R"}).json(); assert r["status"] == "pending" and "confirm?token=" in r["confirm_url"]
    tok = r["confirm_url"].split("token=")[1]; assert c.get(f"/api/site/newsletter/confirm?token={tok}").json()["status"] == "confirmed"
    assert c.post("/api/site/newsletter/compose").status_code == 401
    iss = c.post("/api/site/newsletter/compose", headers=H).json(); assert iss["status"] == "draft" and iss["subject"] and iss["script"].startswith("Good morning")
    s = c.post("/api/site/newsletter/send", headers=H).json(); assert s["provider"].startswith("none") and s["dry_run"] >= 1 and s["sent"] == 0
    v = c.get("/api/site/newsletter/voice", headers=H).json(); assert v["audio"] is None and "dry-run" in v["status"]
    assert c.get(f"/api/site/newsletter/unsubscribe?token={tok}").json()["status"] == "unsubscribed" and c.get("/api/site/newsletter/subscribers", headers=H).json()["by_status"].get("unsubscribed", 0) >= 1

def test_widget_on_every_page_and_bot_fallback_flag():
    for path in ("/", "/services", "/showcase", "/news", "/delivery", "/platform", "/register", "/console", "/monitor", "/quest"):
        r = c.get(path); assert r.status_code == 200 and "/assets/widget.js" in r.text, path
    assert c.get("/assets/widget.js").status_code == 200
    j = c.post("/api/bot/chat", json={"message": "weather on mars"}).json(); assert j["intent"] is None and j["fallback_llm"] is False      # offline: honest fallback, nothing spent
    assert any(s["id"] == "site" for s in c.get("/api/health").json()["services"])
