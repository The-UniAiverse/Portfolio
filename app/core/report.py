"""Shared report renderer: a list of sections (heading, paragraphs, tables, bullets) → Markdown + PDF.
Every service builds its deliverable as data and hands it here, so all reports look the same and PDF code lives once."""
from __future__ import annotations
from datetime import date
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

NAVY = colors.HexColor("#1f2a44")

def section(heading: str, *blocks) -> dict:
    return {"heading": heading, "blocks": list(blocks)}
def para(text: str) -> dict: return {"type": "p", "text": text}
def bullets(items: list[str]) -> dict: return {"type": "ul", "items": items}
def table(headers: list[str], rows: list[list], widths: list[float] | None = None) -> dict:
    return {"type": "table", "headers": headers, "rows": rows, "widths": widths}
def page_break() -> dict: return {"type": "pb"}

def to_markdown(title: str, subtitle: str, sections: list[dict]) -> str:
    L = [f"# {title}", f"*{subtitle} · {date.today().isoformat()} · uniAIverse*", ""]
    for s in sections:
        L += [f"## {s['heading']}", ""]
        for b in s["blocks"]:
            if b["type"] == "p": L += [b["text"], ""]
            elif b["type"] == "ul": L += [f"- {i}" for i in b["items"]] + [""]
            elif b["type"] == "table":
                L += ["| " + " | ".join(b["headers"]) + " |", "|" + "---|" * len(b["headers"])]
                L += ["| " + " | ".join(str(c) for c in r) + " |" for r in b["rows"]] + [""]
    L += ["---", "*uniAIverse — AI Strategy, Consulting, Data & MLOps.*"]
    return "\n".join(L)

def to_pdf(title: str, subtitle: str, sections: list[dict], path: Path) -> Path:
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=19, spaceAfter=4, alignment=0)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], spaceBefore=10, textColor=NAVY)
    body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=9.5, leading=13)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.5)
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=14*mm, bottomMargin=14*mm)
    S = [Paragraph(title, h1), Paragraph(f"{subtitle} · {date.today().isoformat()} · uniAIverse", small), Spacer(1, 8)]
    usable = 178
    for s in sections:
        S.append(Paragraph(s["heading"], h2))
        for b in s["blocks"]:
            if b["type"] == "p": S.append(Paragraph(b["text"], body))
            elif b["type"] == "ul": S += [Paragraph(f"• {i}", body) for i in b["items"]]
            elif b["type"] == "pb": S.append(PageBreak())
            elif b["type"] == "table":
                n = len(b["headers"]); w = b["widths"] or [usable / n] * n
                rows = [b["headers"]] + [[Paragraph(str(c), small) for c in r] for r in b["rows"]]
                t = Table(rows, colWidths=[x * mm for x in w], repeatRows=1)
                t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                                       ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8),
                                       ("GRID", (0,0), (-1,-1), 0.3, colors.grey), ("VALIGN", (0,0), (-1,-1), "TOP")]))
                S += [t, Spacer(1, 6)]
    doc.build(S)
    return path

def write_both(out_dir: Path, stem: str, title: str, subtitle: str, sections: list[dict]) -> tuple[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{stem}.md").write_text(to_markdown(title, subtitle, sections))
    to_pdf(title, subtitle, sections, out_dir / f"{stem}.pdf")
    return f"{stem}.md", f"{stem}.pdf"

def markdown_to_pdf(md: str, path: Path) -> Path:
    """Render simple Markdown (# / ## headings, | tables |, - bullets, paragraphs) with the same house style."""
    title, subtitle, sections, cur, blocks, tbl = "Report", "", [], None, [], None
    def flush_tbl():
        nonlocal tbl
        if tbl: blocks.append(table(tbl[0], tbl[1:])); tbl = None
    def flush_sec():
        nonlocal cur, blocks
        flush_tbl()
        if cur is not None: sections.append(section(cur, *blocks))
        cur, blocks = None, []
    for raw in md.splitlines():
        line = raw.strip()
        if line.startswith("# ") and title == "Report": title = line[2:]; continue
        if line.startswith("*") and line.endswith("*") and not subtitle and cur is None: subtitle = line.strip("*"); continue
        if line.startswith("## "): flush_sec(); cur = line[3:]; continue
        if line.startswith("### "): flush_tbl(); blocks.append(para(f"<b>{line[4:]}</b>")); continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells): continue
            tbl = (tbl or []) + [cells]; continue
        flush_tbl()
        if line.startswith("- ") or line.startswith("• "):
            if blocks and blocks[-1]["type"] == "ul": blocks[-1]["items"].append(line[2:])
            else: blocks.append(bullets([line[2:]]))
        elif line and line != "---": blocks.append(para(line.replace("**", "<b>", 1).replace("**", "</b>", 1) if line.count("**") >= 2 else line))
    if cur is None and blocks: cur = "Summary"
    flush_sec()
    return to_pdf(title, subtitle, sections, path)
