from __future__ import annotations
from pathlib import Path
from app.core.pdf import Doc

def policy_markdown(p: dict) -> str:
    L = [f"# {p['title']}", ""]
    for s in p["sections"]:
        L += [f"## {s['title']}"] + ([s["text"]] if s["text"] else []) + [f"- {b}" for b in s["bullets"]] + [""]
    return "\n".join(L)

def to_markdown(r: dict) -> str:
    L = [f"# AI Governance, Safety & Compliance Assessment — {r['organisation']}", f"*{r['industry']} · uniAIverse*", "",
         f"## Overall control implementation: {r['overall_compliance']}%", r["narrative"], "",
         "## AI inventory and risk classification", "", "| System | Owner | Vendor | Users affected | Risk tier | Controls implemented | Gaps |", "|---|---|---|---|---|---|---|"]
    L += [f"| {s['name']} | {s['owner']} | {s['vendor']} | {s['users_affected']} | {s['tier_title']} | {s['compliance_score']}% | {s['gap_count']} |" for s in r["systems"]]
    for s in r["systems"]:
        L += ["", f"### {s['name']} — {s['tier_title']}", s["purpose"], "", "| Control | Status |", "|---|---|"] + [f"| {c['id']} {c['title']} | {c['label']} |" for c in s["controls"]]
    L += ["", "## Framework gap assessment"]
    for k, a in r["assessment"].items():
        L += [f"### {a['title']} — {a['overall']}%", "", "| Element | Coverage |", "|---|---|"] + [f"| {e['id']} {e['title']} | {e['coverage'] if e['coverage'] is not None else 'n/a'}% |" for e in a["elements"]] + [""]
    L += ["## Remediation roadmap", "", "| # | Horizon | Control | Systems |", "|---|---|---|---|"] + [f"| {x['rank']} | {x['horizon']} | {x['control']} {x['title']} | {', '.join(x['systems'])} |" for x in r["remediation"]]
    L += ["", "## Review process"] + [f"{i}. {s}" for i, s in enumerate(r["review_process"], 1)]
    L += ["", "---", "", policy_markdown(r["policy"]), "", "*Framework-aligned guidance (EU AI Act structure, NIST AI RMF, ISO/IEC 42001). Not legal advice.*"]
    return "\n".join(L)

def to_pdf(r: dict, path: Path) -> Path:
    d = Doc(f"AI Governance, Safety & Compliance — {r['organisation']}", r["industry"])
    d.p(f"<b>Overall control implementation: {r['overall_compliance']}%</b>").h2("Executive summary").p(r["narrative"])
    d.h2("AI inventory and risk classification").table([["System", "Owner", "Vendor", "Users", "Risk tier", "Controls", "Gaps"]] +
        [[s["name"], s["owner"], s["vendor"], s["users_affected"], s["tier_title"], f"{s['compliance_score']}", str(s["gap_count"])] for s in r["systems"]], [42, 24, 22, 22, 22, 18, 14], heat_col=5)
    for s in r["systems"]:
        d.h3(f"{s['name']} — {s['tier_title']}").p(s["purpose"] or "", small=True)
        d.table([["Control", "Status"]] + [[f"{c['id']} — {c['title']}", c["label"]] for c in s["controls"]], [140, 30])
    d.page().h2("Framework gap assessment")
    for a in r["assessment"].values():
        d.h3(f"{a['title']} — {a['overall']}%").table([["Element", "Coverage"]] + [[f"{e['id']} {e['title']}", f"{e['coverage']}" if e["coverage"] is not None else "n/a"] for e in a["elements"]], [140, 30], heat_col=1)
    d.h2("Remediation roadmap").table([["#", "Horizon", "Control", "Systems"]] + [[str(x["rank"]), x["horizon"], f"{x['control']} — {x['title']}", ", ".join(x["systems"])] for x in r["remediation"]], [8, 18, 90, 54])
    d.h2("Review process").bullets([f"{i}. {s}" for i, s in enumerate(r["review_process"], 1)])
    d.page().h2(r["policy"]["title"])
    for s in r["policy"]["sections"]:
        d.h3(s["title"])
        if s["text"]: d.p(s["text"])
        if s["bullets"]: d.bullets(s["bullets"])
    d.p("Framework-aligned guidance (EU AI Act structure, NIST AI RMF, ISO/IEC 42001). Not legal advice.", small=True)
    return d.build(path)
