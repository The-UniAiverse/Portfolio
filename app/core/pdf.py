"""Shared PDF builder (reportlab) so every service report looks like one firm's work."""
from __future__ import annotations
from datetime import date
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

NAVY = colors.HexColor("#1f2a44")
_ss = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=_ss["Title"], fontSize=19, spaceAfter=4, alignment=0)
H2 = ParagraphStyle("h2", parent=_ss["Heading2"], spaceBefore=10, textColor=NAVY)
H3 = ParagraphStyle("h3", parent=_ss["Heading3"], spaceBefore=6, textColor=NAVY)
BODY = ParagraphStyle("b", parent=_ss["BodyText"], fontSize=9.5, leading=13)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)

def heat(score: float) -> colors.Color:
    return colors.HexColor("#c2410c") if score < 40 else colors.HexColor("#ca8a04") if score <= 70 else colors.HexColor("#15803d")

class Doc:
    def __init__(self, title: str, subtitle: str):
        self.S = [Paragraph(title, H1), Paragraph(f"{subtitle} · {date.today().isoformat()} · uniAIverse", SMALL), Spacer(1, 8)]
    def h2(self, t): self.S.append(Paragraph(t, H2)); return self
    def h3(self, t): self.S.append(Paragraph(t, H3)); return self
    def p(self, t, small=False): self.S.append(Paragraph(t, SMALL if small else BODY)); return self
    def bullets(self, items, small=True):
        for i in items: self.S.append(Paragraph(f"• {i}", SMALL if small else BODY))
        return self
    def table(self, rows, widths_mm, heat_col: int | None = None, wrap=True):
        body = [[Paragraph(str(c), SMALL) if wrap and isinstance(c, str) else c for c in r] for r in rows[1:]]
        t = Table([rows[0]] + body, colWidths=[w * mm for w in widths_mm], repeatRows=1)
        st = TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
                         ("GRID", (0,0), (-1,-1), 0.3, colors.grey), ("VALIGN", (0,0), (-1,-1), "TOP"), ("FONTSIZE", (0,0), (-1,-1), 8)])
        if heat_col is not None:
            for i, r in enumerate(rows[1:], 1):
                try: v = float(str(r[heat_col]).split("/")[0]); st.add("BACKGROUND", (heat_col,i), (heat_col,i), heat(v)); st.add("TEXTCOLOR", (heat_col,i), (heat_col,i), colors.white)
                except ValueError: pass
        t.setStyle(st); self.S.append(t); return self
    def page(self): self.S.append(PageBreak()); return self
    def build(self, path: Path) -> Path:
        SimpleDocTemplate(str(path), pagesize=A4, leftMargin=16*mm, rightMargin=16*mm, topMargin=14*mm, bottomMargin=14*mm).build(self.S); return path
