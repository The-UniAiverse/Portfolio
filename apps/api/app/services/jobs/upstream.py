"""Adapter over the vendored ai-job-search project (apps/api/vendor/ai-job-search).

Everything this service borrows from upstream goes through this module: its freehire
job connector (a Bun CLI, run as a subprocess), its Python tools (posting_guard,
rank_state, imported as modules) and its prompt files (read as text). Upstream files
are never edited; see vendor/README.md.
"""
from __future__ import annotations
import functools
import importlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from fastapi import HTTPException

log = logging.getLogger("uniaiverse.jobs")

VENDOR = Path(__file__).resolve().parents[3] / "vendor" / "ai-job-search"
FREEHIRE_CLI = VENDOR / ".agents" / "skills" / "freehire-search" / "cli" / "src" / "cli.ts"
SKILL_DIR = VENDOR / ".claude" / "skills" / "job-application-assistant"
FONTS_DIR = VENDOR / "cover_letters" / "OpenFonts" / "fonts" / "lato"
CLI_TIMEOUT = 40  # seconds; the CLI's own retry budget is 30 s


def _tools():
    tools_dir = str(VENDOR / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)  # posting_guard imports its sibling page_decode
    return importlib.import_module("posting_guard"), importlib.import_module("rank_state")


posting_guard, rank_state = _tools()

WEIGHTS: dict[str, float] = rank_state.WEIGHTS  # technical / experience / behavioral / career


def overall_score(scores: dict) -> int:
    return rank_state.overall_score(scores)


def band(score: int) -> str:
    return rank_state.band(score)


def guard(text: str) -> tuple[str, dict]:
    """Clean a posting and report hidden or injected content. Returns (clean_text, findings)."""
    return posting_guard.guard(text, "text")


# ─── Job connector ───────────────────────────────────────────────────────────

def bun_bin() -> str | None:
    return os.getenv("BUN_BIN") or shutil.which("bun")


def _run_cli(args: list[str]) -> dict:
    bun = bun_bin()
    if not bun:
        raise HTTPException(503, {"code": "jobs_unavailable",
                                  "message": "Job search is not available on this server right now."})
    env = {k: v for k, v in os.environ.items() if k in {"PATH", "HOME", "FREEHIRE_API_URL", "TMPDIR", "LANG"}}
    try:
        proc = subprocess.run([bun, "run", str(FREEHIRE_CLI), *args], cwd=VENDOR, env=env,
                              capture_output=True, text=True, timeout=CLI_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise HTTPException(504, {"code": "jobs_timeout", "message": "The job source took too long to respond. Please try again."})
    if proc.returncode != 0:
        try:
            err = json.loads(proc.stderr.strip().splitlines()[-1])
        except (ValueError, IndexError):
            err = {}
        if err.get("code") == "NOT_FOUND":
            raise HTTPException(404, {"code": "job_not_found", "message": "This job is no longer available."})
        log.warning("freehire CLI failed (%s): %s", err.get("code", proc.returncode), (err.get("error") or "")[:200])
        raise HTTPException(502, {"code": "jobs_source_error", "message": "The job source is unavailable right now. Please try again shortly."})
    return json.loads(proc.stdout)


def _arg(value: str) -> str:
    # Values are passed as argv (no shell). Strip leading dashes so user text can never be read as a flag.
    return re.sub(r"^-+", "", value.strip())


def search(*, query: str = "", city: str = "", country: str = "IN", seniority: list[str] | None = None,
           work_mode: str = "", posted_within_days: int = 0, page: int = 1, limit: int = 20) -> dict:
    args = ["search", "--format", "json", "--no-description", "--page", str(page), "--limit", str(limit)]
    if query.strip():
        args += ["-q", _arg(query)]
    # Upstream: --country and --city form one OR group, so a city search must not also pass a country.
    if city.strip():
        args += ["--city", _arg(city)]
    elif country:
        args += ["--country", _arg(country)]
    if seniority:
        args += ["--seniority", ",".join(_arg(s) for s in seniority)]
    if work_mode:
        args += ["--remote", _arg(work_mode)]
    if posted_within_days:
        args += ["--jobage", str(posted_within_days)]
    return _run_cli(args)


def detail(slug: str) -> dict:
    return _run_cli(["detail", _arg(slug), "--format", "json"])


# ─── Prompt files ────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=None)
def prompt_file(relative: str) -> str:
    """Read an upstream markdown file, without its YAML front matter."""
    text = (VENDOR / relative).read_text(encoding="utf-8")
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S).strip()


def section(markdown: str, heading: str) -> str:
    """Return one `## heading` section (up to the next `## `) from an upstream markdown file."""
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", markdown, flags=re.S | re.M)
    if not m:
        raise RuntimeError(f"upstream section '{heading}' not found; vendor/ai-job-search may have changed")
    return f"## {heading}\n{m.group(1).strip()}"
