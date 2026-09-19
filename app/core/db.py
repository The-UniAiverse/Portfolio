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
