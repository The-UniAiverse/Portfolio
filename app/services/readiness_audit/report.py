"""Render the audit as Markdown and PDF (reportlab, no external binaries)."""
from __future__ import annotations
from datetime import date
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak)
from .schemas import AuditResult

def to_markdown(r: AuditResult) -> str:
    L = [f"# AI Readiness Audit — {r.organisation.name}",
         f"*{r.organisation.industry} · {r.organisation.size} · {date.today().isoformat()} · uniAIverse*", "",
         f"## Overall: {r.overall_score}/100 — {r.maturity_level}", r.maturity_summary, "",
         "## Executive summary", r.narrative, "",
         "## Dimension scores", "", "| Dimension | Weight | Score |", "|---|---|---|"]
    for d in r.dimensions:
        L.append(f"| {d.title} | {int(d.weight*100)}% | {d.score} |")
    L += ["", "## Strengths and gaps"]
    for d in r.dimensions:
        L += [f"### {d.title} ({d.score})"]
        L += [f"- ✅ {s}" for s in d.strengths] or ["- (no strong areas yet)"]
        L += [f"- ⚠️ {g}" for g in d.gaps]
        L.append("")
    L += ["## Prioritised recommendations", "", "| # | Horizon | Dimension | Action | Why | Suggested owner |", "|---|---|---|---|---|---|"]
    for x in r.recommendations:
        L.append(f"| {x.priority} | {x.horizon} | {x.dimension} | {x.action} | {x.why} | {x.owner_hint} |")
    L += ["", "## Roadmap"]
    for h, items in r.roadmap.items():
        L += [f"### {h}"] + [f"- {i}" for i in items] + [""]
    L += ["---", "*Prepared by uniAIverse — AI Strategy, Consulting, Data & MLOps.*"]
    return "\n".join(L)

def to_pdf(r: AuditResult, path: Path) -> Path:
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=20, spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], spaceBefore=10)
    body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=10, leading=14)
    small = ParagraphStyle("s", parent=body, fontSize=8.5, leading=11)
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    S = [Paragraph(f"AI Readiness Audit — {r.organisation.name}", h1),
         Paragraph(f"{r.organisation.industry} · {r.organisation.size} · {date.today().isoformat()} · uniAIverse", small),
         Spacer(1, 8),
         Paragraph(f"<b>Overall score: {r.overall_score}/100 — {r.maturity_level}</b>", body),
         Paragraph(r.maturity_summary, body), Spacer(1, 6),
         Paragraph("Executive summary", h2), Paragraph(r.narrative, body),
         Paragraph("Dimension scores", h2)]
    rows = [["Dimension", "Weight", "Score"]] + [[d.title, f"{int(d.weight*100)}%", f"{d.score}"] for d in r.dimensions]
    t = Table(rows, colWidths=[90*mm, 30*mm, 30*mm])
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1f2a44")),
                           ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                           ("GRID", (0,0), (-1,-1), 0.4, colors.grey), ("FONTSIZE", (0,0), (-1,-1), 9)]))
    S += [t, Paragraph("Strengths and gaps", h2)]
    for d in r.dimensions:
        S.append(Paragraph(f"<b>{d.title} — {d.score}</b>", body))
        for s in d.strengths: S.append(Paragraph(f"+ {s}", small))
        for g in d.gaps: S.append(Paragraph(f"– {g}", small))
        S.append(Spacer(1, 4))
    S += [PageBreak(), Paragraph("Prioritised recommendations", h2)]
    rows = [["#", "Horizon", "Action", "Why", "Owner"]]
    for x in r.recommendations:
        rows.append([str(x.priority), x.horizon, Paragraph(x.action, small), Paragraph(x.why, small), Paragraph(x.owner_hint, small)])
    t = Table(rows, colWidths=[8*mm, 18*mm, 68*mm, 55*mm, 30*mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1f2a44")), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                           ("GRID", (0,0), (-1,-1), 0.3, colors.grey), ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 8.5)]))
    S += [t, Paragraph("Roadmap", h2)]
    for h, items in r.roadmap.items():
        S.append(Paragraph(f"<b>{h}</b>", body))
        for i in items: S.append(Paragraph(f"• {i}", small))
    doc.build(S)
    return path
