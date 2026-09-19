#!/usr/bin/env python3
"""Generate a Marp slide deck for every course that doesn't have a hand-written one.
Reads training-materials/curriculum.yaml → writes training-materials/<folder>/slides/slides.md (skips if exists unless --force).
Then optional: --pdf renders every slides.md to slides.pdf (needs Marp CLI + Chrome; CHROME_PATH may be required)."""
from __future__ import annotations
import subprocess, sys, os
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]; MAT = ROOT / "training-materials"
HEADER = """---
marp: true
theme: default
paginate: true
style: |
  section { font-family: Georgia, "Iowan Old Style", serif; color: #14213d; background: #fbfaf7; }
  h1, h2 { color: #1f2a44; } strong { color: #0f766e; } table { font-size: 0.8em; }
  section.lead h1 { font-size: 2.2em; } footer { color: #5b6170; font-size: 0.6em; }
footer: "uniAIverse Academy · {title} · v{version}"
---
"""

def deck(c: dict) -> str:
    s = [HEADER.replace("{title}", c["title"]).replace("{version}", str(c["version"]))]
    s.append(f"<!-- _class: lead -->\n# {c['title']}\n## {c['audience']}\n**{c['hours']} hours · {', '.join(c['formats'])} · certification: {c['certification']}**\n\n---\n")
    s.append("# What you'll be able to do\n" + "\n".join(f"- {o}" for o in c["outcomes"]) + "\n\n---\n")
    s.append("# Agenda\n| # | Module | Hours |\n|---|---|---|\n" + "\n".join(f"| {i} | {m['title']} | {m['hours']} |" for i, m in enumerate(c["modules"], 1)) + "\n\n---\n")
    for i, m in enumerate(c["modules"], 1):
        s.append(f"<!-- _class: lead -->\n# Module {i}\n## {m['title']}\n*{m['hours']}h*\n\n---\n")
        s.append(f"# {m['title']} — key ideas\n" + "\n".join(f"- **{t}**" for t in m["topics"]) + "\n\n<!-- Trainer: one slide per topic below is the minimum; add a demo or story for each. -->\n\n---\n")
        for t in m["topics"]:
            s.append(f"# {t[0].upper() + t[1:]}\n- What it is\n- Why it matters for **{c['audience'].split(',')[0].lower()}**\n- One example from your organisation\n\n<!-- TODO: replace bullets with the actual teaching content / demo cue -->\n\n---\n")
        if m.get("lab"):
            s.append(f"# Lab · {m['lab']}\n1. Set-up (5 min)\n2. Do (bulk of the time)\n3. Share one result per table\n\n**Deliverable:** {m['lab']}\n\n---\n")
    s.append(f"# Assessment\n{c['assessment']}\n\n---\n")
    s.append("<!-- _class: lead -->\n# Thank you\n## Questions · next steps · uniaiverse.ai\n")
    return "\n".join(s)

def main():
    force = "--force" in sys.argv; cur = yaml.safe_load((MAT / "curriculum.yaml").read_text()); made = []
    for c in cur["courses"]:
        d = MAT / c["folder"] / "slides"; d.mkdir(parents=True, exist_ok=True); f = d / "slides.md"
        if f.exists() and not force: continue
        f.write_text(deck(c)); made.append(str(f.relative_to(ROOT)))
    print(f"generated {len(made)} decks" + (":\n  " + "\n  ".join(made) if made else ""))
    if "--pdf" in sys.argv:
        for f in MAT.glob("*/slides/slides.md"):
            r = subprocess.run(["npx", "-y", "@marp-team/marp-cli", str(f), "--pdf", "--allow-local-files", "--no-stdin", "-o", str(f.with_suffix(".pdf"))], capture_output=True, text=True, stdin=subprocess.DEVNULL)
            print(("ok   " if r.returncode == 0 else "FAIL ") + str(f.relative_to(ROOT)))

if __name__ == "__main__": main()
