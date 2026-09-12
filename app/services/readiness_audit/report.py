"""Markdown + PDF rendering (reportlab). Capability heatmap, red flags, evidence checklist, roadmap."""
from __future__ import annotations
from datetime import date
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from .schemas import AuditResult

def _heat(s: float) -> colors.Color:
    return colors.HexColor("#c2410c") if s < 40 else colors.HexColor("#ca8a04") if s <= 70 else colors.HexColor("#15803d")

def to_markdown(r: AuditResult) -> str:
    L = [f"# AI Readiness Audit — {r.organisation.name}",
         f"*{r.tier.title()} tier · Framework v{r.framework_version} · {r.organisation.industry} · {r.organisation.size} · {date.today().isoformat()} · uniAIverse*", "",
         f"## Overall: {r.overall_score}/100 — {r.maturity_level}", r.maturity_summary, ""]
    if r.benchmark:
        L += [f"**Benchmark ({r.organisation.size}):** {r.benchmark['overall']} — {r.benchmark['note']}", ""]
    if r.red_flags:
        L += ["## 🚩 Critical controls absent"] + [f"- {f}" for f in r.red_flags] + [""]
    L += ["## Executive summary", r.narrative, "", "## Domain scores", "", "| Domain | Weight | Score |", "|---|---|---|"]
    L += [f"| {d.title} | {int(d.weight*100)}% | {d.score} |" for d in r.dimensions]
    L += ["", "## Capability heatmap", "", "| Domain | Capability | Score | Answered |", "|---|---|---|---|"]
    for d in r.dimensions:
        for c in d.capabilities:
            L.append(f"| {d.title} | {c.title} | {c.score} | {c.answered}/{c.total} |")
    if r.industry_modules:
        L += ["", "## Industry modules"] + [f"- **{m['title']}**: {m['score']}" for m in r.industry_modules]
    L += ["", "## Prioritised recommendations", "", "| # | Horizon | Domain › Capability | Action |", "|---|---|---|---|"]
    L += [f"| {x.priority} | {x.horizon} | {x.domain} › {x.capability} | {x.action} |" for x in r.recommendations]
    L += ["", "## Roadmap"]
    for h, items in r.roadmap.items():
        L += [f"### {h}"] + [f"- {i}" for i in items] + [""]
    ev = [(d.title, c.title, e) for d in r.dimensions for c in d.capabilities for e in c.evidence_missing]
    if ev:
        L += ["## Evidence to validate (Gold/Platinum)", "", "| Domain | Capability | Claim to evidence |", "|---|---|---|"]
        L += [f"| {a} | {b} | {e} |" for a, b, e in ev]
    if r.upgrade_hint:
        L += ["", f"> {r.upgrade_hint}"]
    L += ["", "---", "*uniAIverse — AI Strategy, Consulting, Data & MLOps.*"]
    return "\n".join(L)

def to_pdf(r: AuditResult, path: Path) -> Path:
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=19, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], spaceBefore=10, textColor=colors.HexColor("#1f2a44"))
    body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=9.5, leading=13)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.5)
    navy = colors.HexColor("#1f2a44")
    hdr = [("BACKGROUND", (0,0), (-1,0), navy), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
           ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
           ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 8)]
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=14*mm, bottomMargin=14*mm)
    S = [Paragraph(f"AI Readiness Audit — {r.organisation.name}", h1),
         Paragraph(f"{r.tier.title()} tier · Framework v{r.framework_version} · {r.organisation.industry} · {r.organisation.size} · {date.today().isoformat()} · uniAIverse", small),
         Spacer(1, 8), Paragraph(f"<b>Overall score {r.overall_score}/100 — {r.maturity_level}</b>", body), Paragraph(r.maturity_summary, body)]
    if r.benchmark:
        S.append(Paragraph(f"<b>Benchmark ({r.organisation.size} companies): {r.benchmark['overall']}.</b> {r.benchmark['note']}", body))
    if r.red_flags:
        S.append(Paragraph("Critical controls absent", h2))
        S += [Paragraph(f"• {f}", small) for f in r.red_flags]
    S += [Paragraph("Executive summary", h2), Paragraph(r.narrative, body), Paragraph("Domain scores", h2)]
    t = Table([["Domain", "Weight", "Score"]] + [[d.title, f"{int(d.weight*100)}%", f"{d.score}"] for d in r.dimensions], colWidths=[110*mm, 25*mm, 25*mm])
    st = TableStyle(hdr)
    for i, d in enumerate(r.dimensions, 1):
        st.add("BACKGROUND", (2,i), (2,i), _heat(d.score)); st.add("TEXTCOLOR", (2,i), (2,i), colors.white)
    t.setStyle(st); S += [t, Paragraph("Capability heatmap", h2)]
    rows = [["Domain", "Capability", "Score", "Answered"]]
    for d in r.dimensions:
        for c in d.capabilities:
            rows.append([Paragraph(d.title, small), Paragraph(c.title, small), f"{c.score}", f"{c.answered}/{c.total}"])
    t = Table(rows, colWidths=[55*mm, 80*mm, 20*mm, 22*mm], repeatRows=1); st = TableStyle(hdr)
    i = 1
    for d in r.dimensions:
        for c in d.capabilities:
            st.add("BACKGROUND", (2,i), (2,i), _heat(c.score)); st.add("TEXTCOLOR", (2,i), (2,i), colors.white); i += 1
    t.setStyle(st); S.append(t)
    if r.industry_modules:
        S.append(Paragraph("Industry modules", h2))
        S += [Paragraph(f"<b>{m['title']}</b>: {m['score']}", body) for m in r.industry_modules]
    S += [PageBreak(), Paragraph("Prioritised recommendations", h2)]
    rows = [["#", "Horizon", "Domain › Capability", "Action"]] + [[str(x.priority), x.horizon, Paragraph(f"{x.domain} › {x.capability}", small), Paragraph(x.action, small)] for x in r.recommendations]
    t = Table(rows, colWidths=[8*mm, 18*mm, 50*mm, 101*mm], repeatRows=1); t.setStyle(TableStyle(hdr)); S.append(t)
    S.append(Paragraph("Roadmap", h2))
    for h, items in r.roadmap.items():
        S.append(Paragraph(f"<b>{h}</b>", body)); S += [Paragraph(f"• {i}", small) for i in items]
    ev = [(d.title, c.title, e) for d in r.dimensions for c in d.capabilities for e in c.evidence_missing]
    if ev:
        S += [PageBreak(), Paragraph("Evidence to validate", h2),
              Paragraph("Claims scored 3 or 4 on evidence-flagged questions. The audit team validates each against documents, screenshots or system references.", body)]
        t = Table([["Domain", "Capability", "Claim"]] + [[Paragraph(a, small), Paragraph(b, small), Paragraph(e, small)] for a, b, e in ev],
                  colWidths=[40*mm, 45*mm, 92*mm], repeatRows=1); t.setStyle(TableStyle(hdr)); S.append(t)
    if r.upgrade_hint:
        S += [Spacer(1, 10), Paragraph(r.upgrade_hint, body)]
    doc.build(S)
    return path
