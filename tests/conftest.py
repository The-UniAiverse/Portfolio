"""Test isolation: every test session gets a throwaway database and a known admin token.
Without this, tests write into outputs/uniaiverse.db and start failing once a test user reaches its daily free limit."""
import os, tempfile
from pathlib import Path
os.environ["ADMIN_TOKEN"] = "test-token"
from app.core.config import settings   # noqa: E402
settings.admin_token = "test-token"
from app.core import db                # noqa: E402
db.DB_PATH = Path(tempfile.mkdtemp(prefix="uniaiverse-test-")) / "test.db"
db.init()
