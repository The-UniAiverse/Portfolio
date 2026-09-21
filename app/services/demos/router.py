"""Demo Hub — runs the workshop demos server-side (sandboxed: fixed script list, timeout, no shell) and serves a live RAG demo."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.core.config import ROOT

router = APIRouter()
REG = Path(__file__).with_name("demos.yaml")
DEMOS_DIR = ROOT / "training-materials/agentic-ai-workshop/demos"
sys.path.insert(0, str(DEMOS_DIR))

def registry() -> dict: return yaml.safe_load(REG.read_text())

@router.get("")
def list_demos(audience: str | None = None):
    d = registry()["demos"]
    return [x for x in d if not audience or audience in x["audience"] or "everyone" in x["audience"]]

class RunReq(BaseModel):
    variant: str | None = None
    docs_text: str | None = Field(None, description="optional: replace sample documents with this text for RAG demos")

@router.post("/run/{demo_id}")
def run(demo_id: str, req: RunReq | None = None):
    d = next((x for x in registry()["demos"] if x["id"] == demo_id and x["kind"] == "script"), None)
    if not d: raise HTTPException(404, "not a runnable script demo")
    args = list(d.get("args", []))
    if req and req.variant:
        v = d.get("variants", {})
        if req.variant not in v: raise HTTPException(400, f"variant must be one of {list(v)}")
        args += v[req.variant]
    script = ROOT / d["script"]
    try:
        r = subprocess.run([sys.executable, script.name, *args], cwd=script.parent, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "demo timed out")
    return {"id": demo_id, "title": d["title"], "command": f"python {script.name} {' '.join(args)}".strip(),
            "ok": r.returncode == 0, "output": r.stdout[-12000:], "stderr": r.stderr[-2000:] if r.returncode else ""}

# ── Course labs: every training course's demos, discovered from disk (no registry to maintain) ─────────────────────────
import re
MAT = ROOT / "training-materials"
_NAME = re.compile(r"^[0-9]{2}_[a-z0-9_]+\.py$")

def _course_index() -> dict:
    cur = yaml.safe_load((MAT / "curriculum.yaml").read_text()); out = {}
    for c in cur["courses"]:
        d = MAT / c["folder"] / "demos"
        if c["folder"] == "agentic-ai-workshop" or not d.is_dir(): continue
        demos = []
        for p in sorted(d.glob("[0-9][0-9]_*.py")):
            if not _NAME.match(p.name): continue
            m = re.match(r'\s*"""(.*?)"""', p.read_text(), re.S); doc = (m.group(1) if m else p.stem).strip(); first = doc.splitlines()[0]
            t = re.search(r"Demo\s+\d+\s+—\s+(.*?)(?:\s+\((\d+)\s*min\))?(?:\s+·\s+Module\s+([\w+]+))?\s*$", first)
            shows = re.search(r"^Shows:\s*(.+)$", doc, re.M)
            demos.append({"id": p.stem, "file": p.name, "title": t.group(1) if t else first, "minutes": int(t.group(2)) if t and t.group(2) else None,
                          "module": t.group(3) if t else None, "shows": shows.group(1) if shows else ""})
        if demos: out[c["id"]] = {"id": c["id"], "folder": c["folder"], "title": c["title"], "audience": c["audience"], "hours": c["hours"], "level": c["level"], "demos": demos}
    return out

@router.get("/courses")
def course_labs():
    """Every course with runnable demos. The website can render this as a catalogue; each demo runs via POST /run-course/{course}/{demo}."""
    return list(_course_index().values())

@router.post("/run-course/{course_id}/{demo_id}")
def run_course_demo(course_id: str, demo_id: str):
    """Runs one course demo server-side. Safe by construction: the script must be one that discovery found on disk
    (NN_name.py inside that course's demos folder) — no paths, arguments or shell from the caller."""
    c = _course_index().get(course_id)
    d = next((x for x in (c or {}).get("demos", []) if x["id"] == demo_id), None)
    if not d: raise HTTPException(404, "unknown course or demo")
    folder = MAT / c["folder"] / "demos"
    try:
        r = subprocess.run([sys.executable, d["file"]], cwd=folder, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "demo timed out")
    return {"course": course_id, "id": demo_id, "title": d["title"], "command": f"python demos/{d['file']}", "ok": r.returncode == 0,
            "output": r.stdout[-16000:], "stderr": r.stderr[-2000:] if r.returncode else ""}

class Ask(BaseModel):
    question: str = Field(..., min_length=3, max_length=300)
    docs_text: str | None = Field(None, description="paste your own document text (use ## headings) instead of the sample docs")

@router.post("/rag/ask")
def rag_ask(a: Ask):
    """Basic (fixed chunks, dense-only) vs advanced (heading-aware + contextual prefix, hybrid + RRF + rerank) — side by side."""
    import common as C
    if a.docs_text:
        docs = [{"id": "yours", "title": "Your document", "text": a.docs_text}]
    else:
        docs = C.load_docs()
    basic_chunks = [c for d in docs for c in C.chunk_fixed(d)]
    adv_chunks = [c for d in docs for c in C.chunk_by_heading(d, contextual=True)]
    basic_hits = [c for _, c in C.semantic(a.question, basic_chunks)[:3]]
    fused = C.rrf(C.bm25(a.question, adv_chunks), C.semantic(a.question, adv_chunks))
    adv_hits = C.rerank(a.question, [c for _, c in fused[:10]], top=3)
    b_ans, b_in, b_out = C.answer(a.question, basic_hits)
    a_ans, a_in, a_out = C.answer(a.question, adv_hits)
    return {"question": a.question, "source": "your text" if a.docs_text else f"{len(docs)} sample documents",
            "basic": {"method": "fixed 400-char chunks · dense-only · top 3", "answer": b_ans, "passages": [{"source": f"{c.get('doc','')} › {c.get('heading','')}", "text": c["text"][:400]} for c in basic_hits], "tokens_in": b_in, "tokens_out": b_out},
            "advanced": {"method": "heading-aware chunks + contextual prefix · BM25 + dense fused (RRF) · reranked top 3", "answer": a_ans, "passages": [{"source": f"{c.get('doc','')} › {c.get('heading','')}", "text": c["text"][:400]} for c in adv_hits], "tokens_in": a_in, "tokens_out": a_out},
            "note": "Offline stand-in generator; with an LLM key in .env the same pipeline calls a real model."}

@router.get("/sample-docs")
def sample_docs():
    import common as C
    return [{"title": d["title"], "chars": len(d["text"]), "preview": d["text"][:300]} for d in C.load_docs()]
