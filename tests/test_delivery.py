"""AI Delivery Framework — golden tests. If a number here changes, a content file or a rule changed: update the test ON PURPOSE, never by reflex."""
import os
os.environ["ADMIN_TOKEN"] = os.environ.get("ADMIN_TOKEN") or "test-token"
import pytest
from fastapi.testclient import TestClient
from app.core.config import settings
settings.admin_token = settings.admin_token or "test-token"
from app.main import app
c = TestClient(app); H = {"X-Admin-Token": settings.admin_token}
def sample(t): return c.get(f"/api/delivery/sample?tier={t}").json()
def run(i): r = c.post("/api/delivery/run", json=i); assert r.status_code == 200, r.text; return r.json()

@pytest.mark.parametrize("tier,docs,gates", [("bronze", 13, ["G0", "G1"]), ("silver", 21, ["G0", "G1", "G2", "G3"]), ("gold", 26, ["G0", "G1", "G2", "G3", "G4"])])
def test_golden_tier_documents_and_gates(tier, docs, gates):
    R = run(sample(tier)); assert R["tier"] == tier and not R["stop"]
    assert sum(d["included"] for d in R["deliverables"]) == docs and len(R["deliverables"]) == 26
    assert list(R["gates"])[:len(gates)] == gates or set(gates) <= set(R["gates"])

def test_score_bands_and_contingency_bands():
    for t, (lo, hi), band in (("bronze", (8, 12), (10, 15)), ("silver", (13, 18), (15, 25)), ("gold", (19, 24), (25, 40))):
        R = run(sample(t)); assert lo <= R["sizing"]["score"] <= hi; assert band[0] <= R["estimate"]["contingency_pct"] <= band[1]
        e = R["estimate"]; assert abs(e["expected_days"] + e["contingency_days"] - e["total_days"]) < 0.2

def test_totals_are_internally_consistent():
    R = run(sample("silver")); P = R["project_cost"]; E = R["estimate"]
    assert abs(sum(w["expected"] for w in E["workstreams"]) - E["expected_days"]) < 1.0
    assert P["build_range"][0] < P["build_expected"] < P["build_range"][1]
    assert abs(sum(l["amount"] for l in P["build_lines"]) - P["build_expected"]) <= 2
    rm = P["run_monthly"]; assert abs(rm["llm"] + rm["infrastructure"] + rm["support"] - rm["total"]) <= 2
    assert abs(sum(m["amount"] for m in P["milestones"]) - P["build_expected"]) <= len(P["milestones"]) and sum(m["pct"] for m in P["milestones"]) == 100

def test_deterministic():
    a, b = run(sample("silver")), run(sample("silver")); assert a["estimate"] == b["estimate"] and a["project_cost"] == b["project_cost"] and a["stamp"]["content_hash"] == b["stamp"]["content_hash"]

def test_llm_cost_scales_with_volume_and_router_saves():
    s = sample("silver"); base = run(s)["llm_cost"]["monthly_expected"]; s2 = dict(s, requests_per_day=s["requests_per_day"] * 2); assert run(s2)["llm_cost"]["monthly_expected"] > base * 1.7
    s3 = dict(s, cheap_route_share=0.6); assert run(s3)["llm_cost"]["monthly_expected"] < base

def test_risk_floors():
    s = sample("bronze"); assert run(s)["tier"] == "bronze"
    assert run(dict(s, writes_to_production_systems=True, needs_actions_in_systems=True))["tier"] in ("silver", "gold")
    hi = run(dict(s, affects_individuals_rights=True, processes_personal_data=True)); assert hi["governance"]["risk_tier"] == "high" and hi["sizing"]["depth"]["governance"] == "gold" and hi["sizing"]["floors_applied"]

def test_prohibited_stops_and_produces_no_pack():
    s = dict(sample("silver"), manipulative_or_social_scoring=True); R = run(s); assert R["stop"] and "decline_note" in R and "estimate" not in R
    p = c.post("/api/delivery/pack", json=s).json(); assert p["stop"] and "pdf_url" not in p

def test_override_needs_reason_and_is_recorded():
    s = sample("bronze"); bad = dict(s, overrides=[{"field": "tier", "value": "silver", "reason": "x"}]); assert c.post("/api/delivery/run", json=bad).status_code == 422
    R = run(dict(s, overrides=[{"field": "tier", "value": "silver", "reason": "Client asked for full gate formality", "by": "Sarfi"}])); assert R["tier"] == "silver" and R["overrides"] and R["sizing"]["base_tier"] == "bronze"

def test_pack_files_in_all_formats():
    p = c.post("/api/delivery/pack", json=sample("silver")).json(); assert p["documents"] == 21
    for k, magic in (("pdf_url", b"%PDF"), ("docx_url", b"PK"), ("md_url", b"#"), ("json_url", b"{")):
        r = c.get(p[k]); assert r.status_code == 200 and r.content.startswith(magic), k
    assert c.get("/api/delivery/file/..%2F..%2F.env").status_code == 404 and c.get("/api/delivery/file/nope.pdf").status_code == 404

def test_partial_pack():
    R = run(sample("silver")); ids = [d["id"] for d in R["deliverables"] if d["included"]][:2]; p = c.post("/api/delivery/pack?only=" + ",".join(ids), json=sample("silver")).json(); assert p["documents"] == 2

def test_engagements_need_admin_and_keep_versions():
    s = sample("silver"); assert c.post("/api/delivery/intake", json=s).status_code == 401 and c.get("/api/delivery/engagements").status_code == 401
    e = c.post("/api/delivery/intake", json=s, headers=H).json(); eid = e["engagement_id"]; assert e["version"] == 1
    v2 = c.post(f"/api/delivery/intake?engagement_id={eid}", json=dict(s, integrations=s["integrations"] + 4), headers=H).json(); assert v2["version"] == 2 and v2["summary"]["total_days"] > e["summary"]["total_days"]
    d = c.get(f"/api/delivery/engagements/{eid}", headers=H).json(); assert len(d["versions"]) == 2 and d["stale"] is False
    assert any(x["id"] == eid for x in c.get("/api/delivery/engagements", headers=H).json()); assert c.post(f"/api/delivery/engagements/{eid}/pack", headers=H).json()["documents"] == 21

def test_gate_review_rules():
    eid = c.post("/api/delivery/intake", json=sample("silver"), headers=H).json()["engagement_id"]; g = c.get(f"/api/delivery/gates/{eid}", headers=H).json(); crit = g["checklists"]["G0"]["criteria"]
    r = c.post(f"/api/delivery/gates/{eid}/G0", json={"met": [], "decided_by": "Sponsor", "decision": "go"}, headers=H); assert r.status_code == 422          # 'go' with blocking items open needs written conditions
    r = c.post(f"/api/delivery/gates/{eid}/G0", json={"met": [], "decided_by": "Sponsor"}, headers=H).json(); assert r["decision"] == "no_go"
    r = c.post(f"/api/delivery/gates/{eid}/G0", json={"met": [x["id"] for x in crit], "decided_by": "Sponsor", "evidence": {crit[0]["id"]: "SOW v1"}}, headers=H).json(); assert r["decision"] == "go" and not r["missing"]
    assert len(c.get(f"/api/delivery/gates/{eid}", headers=H).json()["records"]) == 2 and c.post(f"/api/delivery/gates/{eid}/G9", json={"decided_by": "x"}, headers=H).status_code == 404

def test_config_and_page():
    cfg = c.get("/api/delivery/config").json(); assert len(cfg["dimensions"]) == 8 and cfg["bands"]["silver"] == [13, 18] and len(cfg["catalogue"]) == 26
    assert c.get("/delivery").status_code == 200 and any(s["id"] == "delivery" for s in c.get("/api/health").json()["services"])
