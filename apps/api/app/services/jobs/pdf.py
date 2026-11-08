"""Render a cover letter to PDF following upstream's cover.cls layout (A4, 2.3 cm margins,
large light name header, grey contact line, right-aligned date) with upstream's Lato fonts.
ReportLab is used instead of XeLaTeX so the server needs no TeX installation."""
from __future__ import annotations
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape as _x
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer
from . import upstream
from .schemas import Letter, CandidateProfile

PRIMARY, HEADINGS, DATE = colors.HexColor("#2b2b2b"), colors.HexColor("#6A6A6A"), colors.HexColor("#666666")


def _fonts() -> tuple[str, str]:
    if "Lato-Lig" not in pdfmetrics.getRegisteredFontNames():
        for name in ("Lato-Lig", "Lato-Reg", "Lato-Bol"):
            pdfmetrics.registerFont(TTFont(name, str(upstream.FONTS_DIR / f"{name}.ttf")))
    return "Lato-Lig", "Lato-Reg"


def render(profile: CandidateProfile, letter: Letter, path: Path) -> int:
    """Write the PDF and return its page count (the upstream rule is exactly one page)."""
    light, regular = _fonts()
    name = ParagraphStyle("name", fontName=light, fontSize=34, leading=40, textColor=PRIMARY)
    contact = ParagraphStyle("contact", fontName=regular, fontSize=10.5, leading=14, textColor=HEADINGS)
    body = ParagraphStyle("body", fontName=regular, fontSize=11, leading=14.5, textColor=PRIMARY, spaceAfter=10)
    dated = ParagraphStyle("date", parent=body, alignment=TA_RIGHT, textColor=DATE)

    contact_bits = [_x(b) for b in (profile.email, profile.phone, profile.link, profile.city) if b]
    story = [Paragraph(_x(profile.name), name)]
    if contact_bits:
        story.append(Paragraph(" &nbsp;|&nbsp; ".join(contact_bits), contact))
    story += [Spacer(1, 18), Paragraph(date.today().strftime("%d %B %Y"), dated), Spacer(1, 6),
              Paragraph(_x(letter.salutation), body)]
    story += [Paragraph(_x(p), body) for p in letter.paragraphs_before_bullets]
    if letter.bullets:
        story.append(ListFlowable(
            [ListItem(Paragraph(_x(b), ParagraphStyle("li", parent=body, spaceAfter=4)), leftIndent=14) for b in letter.bullets],
            bulletType="bullet", start="•", leftIndent=14, bulletFontName=regular, bulletColor=PRIMARY))
        story.append(Spacer(1, 8))
    story += [Paragraph(_x(p), body) for p in letter.paragraphs_after_bullets]
    story += [Spacer(1, 6), Paragraph(_x(letter.sign_off), body), Paragraph(_x(profile.name), body)]

    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm,
                            topMargin=2.3 * cm, bottomMargin=2.3 * cm,
                            title=f"Cover letter - {profile.name}", author=profile.name)
    doc.build(story)
    return doc.page
