"""Course labs: every course has a complete, runnable kit, and the Demo Hub only runs scripts it discovered itself."""
import ast, re
from pathlib import Path
import yaml, pytest
from fastapi.testclient import TestClient
from app.main import app
ROOT = Path(__file__).resolve().parents[1]; MAT = ROOT / "training-materials"; c = TestClient(app)
COURSES = yaml.safe_load((MAT / "curriculum.yaml").read_text())["courses"]

@pytest.mark.parametrize("course", COURSES, ids=lambda x: x["id"])
def test_every_course_has_a_full_kit(course):
    d = MAT / course["folder"]; demos = sorted((d / "demos").glob("[0-9][0-9]_*.py")); assert len(demos) >= 2, "needs working demos, not just slides"
    for f in ("README.md", "facilitator-guide.md", "exercises.md", "demos/run_all.py"): assert (d / f).exists(), f
    assert list((d / "handouts").glob("*.md"))
    for p in demos:
        src = p.read_text(); ast.parse(src); assert ast.get_docstring(ast.parse(src)), f"{p.name}: docstring header missing"
        if course["folder"] != "agentic-ai-workshop": assert re.search(r"Say it|say\(", src), f"{p.name}: no closing say-line"

def test_labkit_is_pure_python_and_offline():
    for p in (MAT / "labkit").glob("*.py"):
        mods = {n.names[0].name.split(".")[0] for n in ast.walk(ast.parse(p.read_text())) if isinstance(n, ast.Import)} | {n.module.split(".")[0] for n in ast.walk(ast.parse(p.read_text())) if isinstance(n, ast.ImportFrom) and n.module and n.level == 0}
        assert not mods & {"numpy", "pandas", "sklearn", "torch", "requests"}, f"{p.name} imports a heavy or network package: {mods}"

def test_course_catalogue_endpoint():
    r = c.get("/api/demos/courses").json(); assert len(r) == len(COURSES) - 1            # the workshop is served by the classic /api/demos list
    assert sum(len(x["demos"]) for x in r) >= 100 and all(d["title"] and d["shows"] for x in r for d in x["demos"])

def test_run_one_demo_and_refuse_everything_else():
    r = c.post("/api/demos/run-course/llm-cost/01_billing_unit_and_formula").json(); assert r["ok"] and "Say it" in r["output"]
    for bad in ("/api/demos/run-course/llm-cost/run_all", "/api/demos/run-course/labkit/core", "/api/demos/run-course/llm-cost/..%2Fcost_calculator", "/api/demos/run-course/nope/01_x"): assert c.post(bad).status_code == 404
