#!/usr/bin/env python3
"""Build every audience variant of the workshop from variants.yaml + slides.yaml:
    python training-materials/agentic-ai-workshop/build_variants.py [variant_id]
Output per variant in variants/<id>/: slides.yaml, <deck>.pptx, facilitator-guide.md, exercises.md, README.md"""
from __future__ import annotations
import re, subprocess, sys, shutil
from pathlib import Path
import yaml
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]
master = yaml.safe_load((HERE / "slides.yaml").read_text()); V = yaml.safe_load((HERE / "variants.yaml").read_text())
exercises = (HERE / "exercises.md").read_text()

def hit(title: str, pat: str) -> bool: return pat.lower() in (title or "").lower()

def build(vid: str, v: dict):
    out = HERE / "variants" / vid; out.mkdir(parents=True, exist_ok=True)
    slides = list(master["slides"])
    if v["keep_slides"] != "all":
        slides = [s for s in slides if any(hit(s.get("title", ""), k) for k in v["keep_slides"]) or s.get("type") == "close"]
    slides = [s for s in slides if not any(hit(s.get("title", ""), d) for d in v.get("drop_slides", []))]
    added = 0
    for m in v.get("add_modules", []):
        idx = next((i for i, s in enumerate(slides) if hit(s.get("title", ""), m["after"])), None)
        new = {"type": "bullets", "title": m["title"], "bullets": [b.strip() for b in re.split(r"(?<=[.!?])\s+", m["talk"]) if b.strip()][:5], "notes": m["talk"]}
        if idx is None: slides.append(new)
        else: slides.insert(idx + 1, new)
        added += 1
    slides[0] = {**slides[0], "title": v["title"], "subtitle": v["audience"]}
    spec = {"deck": {**master["deck"], "title": v["title"], "file": f"deck-{vid}", "footer": f"uniAIverse · {v['title']} · v{V['version']}"}, "slides": slides}
    (out / "slides.yaml").write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=200))
    subprocess.run(["node", str(ROOT / "scripts/build_slides.js"), str(out / "slides.yaml")], check=True)
    labs = "\n".join(f"- **{k.upper()}** — {t}" for k, t in v["labs"].items())
    mods = "\n".join(f"### {m['title']} ({m['minutes']} min, after “{m['after']}”)\n{m['talk']}\n" for m in v.get("add_modules", []))
    guide = f"""# Facilitator guide — {v['title']}
**Audience:** {v['audience']}  ·  **Duration:** {v['duration_days']} day(s)  ·  **Deck:** `deck-{vid}.pptx` ({len(slides)} slides, speaker notes on every slide)

## Tone
{v['tone']}

## Platform
{v['platform']}

## Before the day
{chr(10).join('- ' + p for p in v['prerequisites'])}
- Run `python ../../demos/run_all.py` on the delivery laptop — it must print ALL DEMOS OK
- Replace `demos/sample_docs/` with the client's documents where allowed

## Run of show
Follow the master run sheet (`../../facilitator-guide.md`) for timing and demo cues, using only the slides in this deck. Variant-specific modules below are inserted where their heading says.

{mods if mods else '_No added modules._'}

## Labs in this variant
{labs}

{('## Assessment' + chr(10) + v['assessment'] + chr(10)) if v.get('assessment') else ''}
## Done when
{v['done_when']}

## Follow-up offers
{chr(10).join('- ' + f for f in v['follow_up'])}
"""
    (out / "facilitator-guide.md").write_text(guide)
    keep = set(v["labs"].keys())
    parts = re.split(r"(?=^## Lab )", exercises, flags=re.M)
    ex = parts[0] + "".join(p for p in parts[1:] if re.match(r"## Lab (\d)", p) and f"lab{re.match(r'## Lab (\d)', p).group(1)}" in keep)
    (out / "exercises.md").write_text(ex)
    (out / "README.md").write_text(f"# {v['title']}\n\n{v['audience']}. {v['duration_days']} day(s).\n\n- `deck-{vid}.pptx` — {len(slides)} slides ({added} audience-specific modules added)\n- `facilitator-guide.md` — tone, platform, prerequisites, added modules with talk tracks, labs, done-when, follow-ups\n- `exercises.md` — only the labs this variant uses\n- Demos: `../../demos/` (shared)\n\nRebuild after editing `../../variants.yaml` or `../../slides.yaml`: `python ../../build_variants.py {vid}`\n")
    print(f"{vid}: {len(slides)} slides, {added} modules added → {out}")

ids = sys.argv[1:] or list(V["variants"])
for vid in ids: build(vid, V["variants"][vid])
