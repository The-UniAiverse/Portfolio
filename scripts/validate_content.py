#!/usr/bin/env python3
"""One command to check everything editable is still consistent. Run before every commit / delivery:
    python scripts/validate_content.py
Checks: every YAML parses · readiness question bank line format & tiers · curriculum integrity (tracks, prerequisites, folders)
· quest question bank (answers in range, ids unique) · bot knowledge intents · pricing ↔ blueprint tiers · workshop demos run."""
from __future__ import annotations
import glob, re, subprocess, sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]; errs: list[str] = []
def err(m): errs.append(m); print("  ✗", m)

print("YAML files")
for f in glob.glob(str(ROOT / "**/*.yaml"), recursive=True):
    try: yaml.safe_load(open(f))
    except Exception as e: err(f"{f}: {e}")

print("Readiness question bank")
qb = yaml.safe_load(open(ROOT / "app/services/readiness_audit/question_bank.yaml")); n = 0
for d in qb["domains"]:
    if not d.get("weight"): err(f"domain {d['id']} has no weight")
    for c in d["capabilities"]:
        for k in ("low_action", "mid_action"):
            if not c.get(k): err(f"{d['id']}.{c['id']} missing {k}")
        for q in c["questions"]:
            n += 1
            if not re.match(r"^[FBSGP][*!]*\s+\S", q): err(f"bad question line in {d['id']}.{c['id']}: {q[:60]}")
if abs(sum(d["weight"] for d in qb["domains"]) - 1) > 1e-6: err("domain weights do not sum to 1.0")
print(f"  {n} questions, {len(qb['domains'])} domains")

print("Curriculum")
cur = yaml.safe_load(open(ROOT / "training-materials/curriculum.yaml")); ids = {c["id"] for c in cur["courses"]}
for t in cur["tracks"]:
    for cid in t["courses"]:
        if cid not in ids: err(f"track {t['id']} references unknown course {cid}")
for c in cur["courses"]:
    for p in c.get("prerequisites", []):
        if p not in ids: err(f"course {c['id']} prerequisite {p} unknown")
    if not (ROOT / "training-materials" / c["folder"]).exists(): err(f"course {c['id']} folder missing: {c['folder']}")
    for f in c.get("files", []):
        if not (ROOT / "training-materials" / c["folder"] / f).exists(): err(f"course {c['id']} file missing: {f}")
    if not c.get("modules") or not c.get("outcomes"): err(f"course {c['id']} needs modules and outcomes")
print(f"  {len(cur['courses'])} courses, {len(cur['tracks'])} tracks")

print("uniAI Quest question bank")
q = yaml.safe_load(open(ROOT / "app/services/quest/question_bank.yaml")); seen = set(); n = 0
for t in q["topics"]:
    for x in t["questions"]:
        n += 1
        if not 0 <= x["answer"] < len(x["options"]): err(f"{t['id']}: answer index out of range: {x['q'][:50]}")
        if x["d"] not in (1, 2, 3): err(f"{t['id']}: difficulty must be 1-3: {x['q'][:50]}")
        key = (t["id"], x["q"])
        if key in seen: err(f"duplicate question in {t['id']}: {x['q'][:50]}")
        seen.add(key)
for ch in q.get("interview_challenges", []):
    for k in ("id", "topic", "prompt", "listen_for", "model_answer"):
        if k not in ch: err(f"challenge missing {k}")
print(f"  {n} questions, {len(q.get('interview_challenges', []))} challenges")

print("uniAI bot knowledge")
kb = yaml.safe_load(open(ROOT / "app/services/bot/knowledge.yaml")); iids = set()
for it in kb["intents"]:
    if it["id"] in iids: err(f"duplicate intent {it['id']}")
    iids.add(it["id"])
    if not it.get("triggers") or not it.get("answer"): err(f"intent {it['id']} needs triggers and answer")
print(f"  {len(kb['intents'])} intents")

print("Pricing ↔ blueprints")
tiers = yaml.safe_load(open(ROOT / "pricing/tiers.yaml")); bp = yaml.safe_load(open(ROOT / "pricing/blueprints.yaml"))
for svc, spec in bp["services"].items():
    for t in spec["tiers"]:
        if t not in tiers["services"].get(svc, {}).get("tiers", {}): err(f"blueprint {svc}/{t} has no price in tiers.yaml")

if "--no-demos" not in sys.argv:
    print("Workshop demos")
    r = subprocess.run([sys.executable, "run_all.py"], cwd=ROOT / "training-materials/agentic-ai-workshop/demos", capture_output=True, text=True)
    if "ALL DEMOS OK" not in r.stdout: err("workshop demos failed: " + r.stdout[-300:] + r.stderr[-300:])
    else: print("  all demos ran")

print("\n" + ("ALL CONTENT VALID" if not errs else f"{len(errs)} problem(s) — fix before shipping")); sys.exit(1 if errs else 0)
