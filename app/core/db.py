"""Tiny SQLite store (stdlib) for users, quest progress, news queue, payments. Swap for Postgres later via the same functions."""
from __future__ import annotations
import json, sqlite3, threading, time
from contextlib import contextmanager
from .config import settings

DB_PATH = settings.outputs_dir / "uniaiverse.db"
_lock = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, email TEXT, name TEXT, tier TEXT DEFAULT 'free', xp INTEGER DEFAULT 0,
  created_at REAL, meta TEXT DEFAULT '{}');
CREATE TABLE IF NOT EXISTS quiz_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, topic TEXT, difficulty INTEGER,
  score INTEGER, total INTEGER, xp INTEGER, kind TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS news (id TEXT PRIMARY KEY, source TEXT, title TEXT, url TEXT, summary TEXT, published TEXT,
  status TEXT DEFAULT 'pending', tags TEXT DEFAULT '[]', fetched_at REAL, approved_at REAL);
CREATE TABLE IF NOT EXISTS question_drafts (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, question TEXT, status TEXT DEFAULT 'pending',
  source_url TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS mentor_requests (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, tier TEXT, topic TEXT,
  preferred_slots TEXT, status TEXT DEFAULT 'requested', created_at REAL);
CREATE TABLE IF NOT EXISTS payments (id TEXT PRIMARY KEY, provider TEXT, order_id TEXT, product_id TEXT, amount INTEGER, currency TEXT,
  method_rule TEXT, status TEXT, customer TEXT, user_id TEXT, created_at REAL, paid_at REAL, raw TEXT);
CREATE TABLE IF NOT EXISTS delivery_engagements (id TEXT PRIMARY KEY, client TEXT, project TEXT, tier TEXT, version INTEGER DEFAULT 1,
  content_hash TEXT, intake TEXT, result TEXT, created_at REAL, updated_at REAL);
CREATE TABLE IF NOT EXISTS delivery_versions (id INTEGER PRIMARY KEY AUTOINCREMENT, engagement_id TEXT, version INTEGER, content_hash TEXT, intake TEXT, summary TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS delivery_gate_records (id INTEGER PRIMARY KEY AUTOINCREMENT, engagement_id TEXT, gate TEXT, decision TEXT, recommendation TEXT,
  met TEXT, missing TEXT, evidence TEXT, attendees TEXT, decided_by TEXT, conditions TEXT, risks_carried TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS tenants (id TEXT PRIMARY KEY, name TEXT, contact_email TEXT, contact_name TEXT, plan TEXT, state TEXT, requested_plan TEXT, purpose TEXT,
  key_hash TEXT, limits TEXT, environment TEXT, created_at REAL, updated_at REAL, activated_at REAL, expires_at REAL);
CREATE TABLE IF NOT EXISTS tenant_users (id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT, email TEXT, role TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS tenant_usage (id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT, month TEXT, day TEXT, capability TEXT, units INTEGER, cost_inr REAL, allowed INTEGER, reason TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS provisioning_jobs (id TEXT PRIMARY KEY, tenant_id TEXT, status TEXT, steps TEXT, error TEXT, created_at REAL, finished_at REAL);
CREATE TABLE IF NOT EXISTS platform_audit (id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT, actor TEXT, action TEXT, detail TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS platform_settings (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS llm_calls (id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT, user_email TEXT, month TEXT, day TEXT, provider TEXT, model TEXT, model_class TEXT, tokens_in INTEGER, tokens_out INTEGER, cost_inr REAL, latency_ms INTEGER, status TEXT, reason TEXT, purpose TEXT, created_at REAL);
CREATE TABLE IF NOT EXISTS bot_log (id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT, question TEXT, intent TEXT, answered INTEGER, created_at REAL);
"""

@contextmanager
def conn():
    with _lock:
        c = sqlite3.connect(DB_PATH, check_same_thread=False)
        c.row_factory = sqlite3.Row
        try:
            yield c; c.commit()
        finally:
            c.close()

def init():
    with conn() as c:
        c.executescript(SCHEMA)

def now() -> float:
    return time.time()

def get_user(user_id: str, create: bool = True) -> dict | None:
    with conn() as c:
        r = c.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if r is None and create:
            c.execute("INSERT INTO users (id, created_at) VALUES (?, ?)", (user_id, now()))
            r = c.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        return dict(r) if r else None

def set_tier(user_id: str, tier: str, email: str | None = None):
    get_user(user_id)
    with conn() as c:
        c.execute("UPDATE users SET tier=?, email=COALESCE(?, email) WHERE id=?", (tier, email, user_id))

init()
