"""Sign-in enforcement on AI tool endpoints, with real Ed25519-signed tokens (as Better Auth issues)."""
import time
import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient
from app.core import auth
from app.core.config import settings
from app.main import app

c = TestClient(app)
ISS = AUD = "http://localhost:3000"
KEY = Ed25519PrivateKey.generate()
OTHER_KEY = Ed25519PrivateKey.generate()
ROI = {"workflows": [{"name": "Invoices", "volume_per_month": 100, "minutes_per_item": 5}]}


class FakeJWKS:
    """Stands in for the website's /api/auth/jwks: serves the public half of KEY."""
    def get_signing_key_from_jwt(self, token):
        return type("K", (), {"key": KEY.public_key()})()


@pytest.fixture(autouse=True)
def enforce(monkeypatch):
    monkeypatch.setattr(settings, "auth_required", True)
    monkeypatch.setattr(auth, "_jwks", FakeJWKS())


def token(key=KEY, **over):
    now = int(time.time())
    claims = {"sub": "user-1", "email": "a@example.com", "name": "A", "iss": ISS, "aud": AUD, "iat": now, "exp": now + 900}
    claims.update(over)
    return jwt.encode({k: v for k, v in claims.items() if v is not None}, key, algorithm="EdDSA")


def roi(tok=None):
    return c.post("/api/automation/roi", json=ROI, headers={"Authorization": f"Bearer {tok}"} if tok else {})


def test_ai_tools_reject_anonymous_requests():
    for path, body in [("/api/automation/roi", ROI), ("/api/governance/classify", {"use_case": "x"}),
                       ("/api/strategy/roadmap", {}), ("/api/readiness_audit/run", {}), ("/api/jobs/match", {}),
                       ("/api/jobs/cover-letter", {}), ("/api/jobs/cover-letter/pdf", {})]:
        r = c.post(path, json=body)
        assert r.status_code == 401, path
        assert r.json()["detail"]["code"] == "auth_required"


def test_valid_token_is_accepted():
    assert roi(token()).status_code == 200


@pytest.mark.parametrize("bad", [
    token(key=OTHER_KEY),                       # signed by someone else
    token(exp=int(time.time()) - 120),          # expired
    token(aud="https://evil.example"),          # wrong audience
    token(iss="https://evil.example"),          # wrong issuer
    token(sub=None),                            # no subject
    "not-a-jwt",
])
def test_bad_tokens_are_rejected(bad):
    assert roi(bad).status_code == 401


def test_unsigned_token_is_rejected():
    forged = jwt.encode({"sub": "x", "iss": ISS, "aud": AUD, "iat": int(time.time()), "exp": int(time.time()) + 900}, None, algorithm="none")
    assert roi(forged).status_code == 401


def test_public_endpoints_stay_open():
    for path in ["/api/health", "/api/pricing/tiers", "/api/training/catalog", "/api/readiness_audit/questionnaire",
                 "/api/governance/policy-template"]:
        assert c.get(path).status_code == 200, path


def test_jwks_outage_is_503_not_401(monkeypatch):
    class Down:
        def get_signing_key_from_jwt(self, t):
            raise jwt.PyJWKClientConnectionError("down")
    monkeypatch.setattr(auth, "_jwks", Down())
    r = roi(token())
    assert r.status_code == 503 and r.json()["detail"]["code"] == "auth_unavailable"
