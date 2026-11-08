"""Sign-in enforcement for AI tool endpoints.

The website (apps/web, Better Auth) signs users in with Google or GitHub and issues short-lived
JWTs (Ed25519). This module verifies them against the website's public keys (JWKS), so the API
does not trust the browser: no valid token, no AI tool. Attach with `Depends(require_user)`.
"""
from __future__ import annotations
import logging
from dataclasses import dataclass
import jwt
from fastapi import Header, HTTPException
from .config import settings

log = logging.getLogger("uniaiverse.auth")

ALGORITHMS = ["EdDSA", "ES256", "RS256"]  # Better Auth defaults to EdDSA; others if its key config changes
_jwks: jwt.PyJWKClient | None = None


@dataclass(frozen=True)
class User:
    id: str
    email: str
    name: str


def _client() -> jwt.PyJWKClient:
    global _jwks
    if _jwks is None:
        # Keys are cached; an unknown `kid` (key rotation) triggers one refetch.
        _jwks = jwt.PyJWKClient(settings.auth_jwks_url, cache_keys=True, lifespan=3600, timeout=10)
    return _jwks


def _unauthorized(message: str = "Please sign in to use this tool.") -> HTTPException:
    return HTTPException(401, {"code": "auth_required", "message": message}, headers={"WWW-Authenticate": "Bearer"})


def verify(token: str) -> User:
    try:
        key = _client().get_signing_key_from_jwt(token)
    except jwt.PyJWKClientConnectionError:
        log.warning("Could not fetch sign-in keys from %s", settings.auth_jwks_url)
        raise HTTPException(503, {"code": "auth_unavailable", "message": "Sign-in is temporarily unavailable. Please try again."})
    except jwt.PyJWTError:
        raise _unauthorized()
    try:
        claims = jwt.decode(token, key.key, algorithms=ALGORITHMS, audience=settings.auth_audience,
                            issuer=settings.auth_issuer, options={"require": ["exp", "iat", "sub"]}, leeway=30)
    except jwt.ExpiredSignatureError:
        raise _unauthorized("Your session expired. Please sign in again.")
    except jwt.PyJWTError:
        raise _unauthorized()
    return User(id=claims["sub"], email=claims.get("email", ""), name=claims.get("name", ""))


def require_user(authorization: str | None = Header(default=None)) -> User | None:
    """FastAPI dependency. Returns the signed-in user, or None when AUTH_REQUIRED=false (local dev)."""
    if not settings.auth_required:
        return None
    if not authorization or not authorization.lower().startswith("bearer "):
        raise _unauthorized()
    return verify(authorization[7:].strip())
