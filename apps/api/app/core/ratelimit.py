"""Minimal in-memory, per-client sliding-window rate limiter for state-changing requests.

Public Playground tools are anonymous, so every POST under /api is limited per client IP.
This is process-local: with several workers/instances each keeps its own window. For
multi-instance production use a shared store (e.g. Redis) or the hosting platform's
edge rate limiting — see docs/architecture.md.
"""
from __future__ import annotations
import time
from collections import defaultdict, deque
from threading import Lock
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_seconds: float = 60.0):
        self.limit = limit
        self.window = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, now: float | None = None) -> float | None:
        """Record a hit. Return None if allowed, or seconds until retry if limited."""
        if self.limit <= 0:
            return None
        now = time.monotonic() if now is None else now
        with self._lock:
            q = self._hits[key]
            while q and now - q[0] >= self.window:
                q.popleft()
            if len(q) >= self.limit:
                return max(0.0, self.window - (now - q[0]))
            q.append(now)
            if len(self._hits) > 10_000:  # bound memory: drop idle clients
                for k in [k for k, v in self._hits.items() if not v]:
                    del self._hits[k]
            return None

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


def client_key(request: Request, trust_proxy: bool) -> str:
    if trust_proxy:
        fwd = request.headers.get("x-forwarded-for")
        if fwd:
            return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter: SlidingWindowLimiter, trust_proxy: bool = False):
        super().__init__(app)
        self.limiter = limiter
        self.trust_proxy = trust_proxy

    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.url.path.startswith("/api/"):
            retry = self.limiter.check(client_key(request, self.trust_proxy))
            if retry is not None:
                return JSONResponse(
                    status_code=429,
                    content={"detail": {"code": "rate_limited",
                                        "message": "Too many requests. Please wait a moment and try again."}},
                    headers={"Retry-After": str(int(retry) + 1)},
                )
        return await call_next(request)
