#!/usr/bin/env python3
"""Add a course in one command. Creates the folder pack and appends the curriculum entry.
Usage: python scripts/new_course.py <id> "<title>" --hours 8 --level 2 --audience "..." --track business [--tiers bronze,silver,gold,platinum]
Then: edit curriculum.yaml (modules, labs), slides/slides.md and demos/NN_*.py; run scripts/build_course_kits.py <id> to regenerate the guide, exercises, handout and run_all.py; commit."""
from __future__ import annotations
import argparse, datetime
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]; MAT = ROOT / "training-materials"
ap = argparse.ArgumentParser(); ap.add_argument("id"); ap.add_argument("title"); ap.add_argument("--hours", type=float, default=8); ap.add_argument("--level", type=int, default=2)
ap.add_argument("--audience", default="Business and technical teams"); ap.add_argument("--track", default=None); ap.add_argument("--tiers", default="silver,gold,platinum"); ap.add_argument("--owner", default="Sarfi")
a = ap.parse_args()
cur_p = MAT / "curriculum.yaml"; cur = yaml.safe_load(cur_p.read_text())
if any(c["id"] == a.id for c in cur["courses"]): raise SystemExit(f"course '{a.id}' already exists")
entry = {"id": a.id, "title": a.title, "version": "0.1", "status": "draft", "level": a.level, "owner": a.owner, "last_reviewed": datetime.date.today().isoformat(),
         "audience": a.audience, "hours": a.hours, "formats": ["workshop"], "tiers": a.tiers.split(","), "prerequisites": [], "certification": "aware",
         "outcomes": ["Outcome 1 — replace", "Outcome 2 — replace"],
         "modules": [{"title": "Module 1 — replace", "hours": round(a.hours / 2, 1), "topics": ["topic a", "topic b"], "lab": "Lab — replace"},
                     {"title": "Module 2 — replace", "hours": round(a.hours / 2, 1), "topics": ["topic c", "topic d"], "lab": "Lab — replace"}],
         "assessment": "Replace with the deliverable participants produce", "folder": a.id}
cur["courses"].append(entry)
if a.track:
    t = next((t for t in cur["tracks"] if t["id"] == a.track), None)
    if t: t["courses"].append(a.id)
cur_p.write_text(yaml.safe_dump(cur, sort_keys=False, allow_unicode=True, width=120))
d = MAT / a.id; (d / "slides").mkdir(parents=True, exist_ok=True); (d / "demos").mkdir(exist_ok=True)
(d / "COURSE.md").write_text(f"# {a.title}\n\nOne-paragraph pitch. Who it's for, what they leave with.\n\nSee `facilitator-guide.md`, `slides/slides.md`, `exercises.md`, `demos/`.\n")
(d / "facilitator-guide.md").write_text(f"# Facilitator Guide — {a.title}\n\n**Before:** logins, printouts, run demos.\n\n| Time | Slide | Segment | What you do and say |\n|---|---|---|---|\n| 00:00 | 1 | Welcome | |\n| 00:10 | 3 | Module 1 | |\n\n## If short on time\n\n## What can go wrong\n")
(d / "exercises.md").write_text(f"# {a.title} — Exercise Sheets\n\n## Lab 1\n\n## Lab 2\n")
(d / "demos" / "01_first_demo.py").write_text(f'''"""{a.title} · Demo 1 — Replace this title (10 min) · Module 1
Shows: one sentence — what the room will see
Lab: one or two sentences — what participants then do themselves
Run: python 01_first_demo.py
"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); from labkit import *
banner("{a.title} · Demo 1 — Replace this title")
table(["Thing", "Value"], [["replace", "me"]])
say("Replace with the one sentence the room should remember.")
''')
import subprocess, sys; subprocess.run([sys.executable, str(ROOT / "scripts/build_slides.py")])
for f in ("facilitator-guide.md", "exercises.md"): (d / f).unlink()          # let the kit generator own these until you take them over by hand
subprocess.run([sys.executable, str(ROOT / "scripts/build_course_kits.py"), a.id])
print(f"created training-materials/{a.id}/ and curriculum entry (status: draft). Edit, then set status: active.")
