"""
pdf_generator.py  –  ResumeForge
Generates A4 resume PDFs with 3 colour themes using ReportLab.

Root cause of the original LayoutError:
  - KeepInFrame overflowing its fixed height
  - ROUNDEDCORNERS (not supported in all ReportLab versions)
  - Nested Tables inside KeepInFrame inside Table

Fix: replaced with a flat row-by-row two-column Table.
No KeepInFrame, no ROUNDEDCORNERS, no nested Table-in-KeepInFrame.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "Classic Green":   {"primary": "#1D9E75", "light": "#E1F5EE", "dark": "#085041"},
    "Corporate Blue":  {"primary": "#185FA5", "light": "#E6F1FB", "dark": "#042C53"},
    "Creative Purple": {"primary": "#533AB7", "light": "#EEEDFE", "dark": "#26215C"},
}

def _hex(h: str) -> colors.Color:
    h = h.lstrip("#")
    return colors.Color(int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255)

# ── Constants ─────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
LM, RM, TM, BM = 15*mm, 15*mm, 10*mm, 15*mm
BODY_W  = PAGE_W - LM - RM          # usable width  (~165 mm)
LEFT_W  = 58 * mm                   # left sidebar
GAP_W   = 6  * mm                   # column gap
RIGHT_W = BODY_W - LEFT_W - GAP_W   # right column

def _style(name, font="Helvetica", size=10, color="#111111",
           leading=None, align=TA_LEFT, sb=0, sa=0):
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        textColor=_hex(color) if isinstance(color, str) else color,
        leading=leading or size * 1.4,
        alignment=align,
        spaceBefore=sb,
        spaceAfter=sa,
    )


def generate_resume_pdf(data: dict) -> bytes:
    """Build resume PDF and return raw bytes."""

    buf = io.BytesIO()

    theme   = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    LIGHT   = _hex(theme["light"])
    DARK    = _hex(theme["dark"])
    BORDER  = _hex("#e0e0e0")

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM,  bottomMargin=BM,
    )

    # ── Styles ────────────────────────────────────────────────────────────────
    ST = {
        "name":    _style("N",  "Helvetica-Bold", 21, colors.white, 26),
        "title":   _style("Ti", "Helvetica",      11, colors.white, 14),
        "contact": _style("Co", "Helvetica",       9, colors.white, 12),
        "sec":     _style("S",  "Helvetica-Bold",  9, PRIMARY,      12, sb=6, sa=1),
        "bold":    _style("B",  "Helvetica-Bold", 10, "#0f0f0f",    13),
        "body":    _style("Bd", "Helvetica",      9.5,"#222222",    13),
        "muted":   _style("M",  "Helvetica",      8.5,"#555555",    11),
        "skill":   _style("Sk", "Helvetica",      8.5, DARK,        11, TA_CENTER),
    }

    story = []

    # ── HEADER ────────────────────────────────────────────────────────────────
    name    = (data.get("name") or "").strip() or "Your Name"
    title   = (data.get("title") or "").strip()
    contact = "   ·   ".join(filter(None, [
        data.get("email","").strip(),
        data.get("phone","").strip(),
        data.get("location","").strip(),
        data.get("linkedin","").strip(),
    ]))

    hdr_data = [[Paragraph(name, ST["name"])]]
    if title:
        hdr_data.append([Paragraph(title, ST["title"])])
    if contact:
        hdr_data.append([Paragraph(contact, ST["contact"])])

    hdr = Table(hdr_data, colWidths=[BODY_W])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), PRIMARY),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 5*mm))

    # ── Build column item lists ───────────────────────────────────────────────
    # Each item is a tuple: ("TYPE", value)
    # Types: SEC | BOLD | BODY | MUTED | SKILL | SPACER

    left_items:  list = []
    right_items: list = []

    # LEFT — Skills
    skills = [s.strip() for s in (data.get("skills") or []) if s and s.strip()]
    if skills:
        left_items.append(("SEC",   "SKILLS"))
        for sk in skills:
            left_items.append(("SKILL", sk.title()))
            left_items.append(("SPACER", 2))

    # LEFT — Education
    deg  = (data.get("degree","")      or "").strip()
    inst = (data.get("institution","") or "").strip()
    yr   = (data.get("year","")        or "").strip()
    left_items.append(("SPACER", 8))
    left_items.append(("SEC", "EDUCATION"))
    if deg:
        left_items.append(("BOLD", deg))
    inst_line = " · ".join(filter(None, [inst, yr]))
    if inst_line:
        left_items.append(("MUTED", inst_line))

    # RIGHT — Experience
    role     = (data.get("role","")     or "").strip()
    company  = (data.get("company","")  or "").strip()
    duration = (data.get("duration","") or "").strip()
    exp_desc = (data.get("exp_desc","") or "").strip()

    right_items.append(("SEC", "EXPERIENCE"))
    if role:
        right_items.append(("BOLD", role))
    co_line = " · ".join(filter(None, [company, duration]))
    if co_line:
        right_items.append(("MUTED", co_line))
    if exp_desc:
        right_items.append(("SPACER", 3))
        for line in exp_desc.splitlines():
            if line.strip():
                right_items.append(("BODY", line.strip()))

    # RIGHT — Projects
    projects = (data.get("projects","") or "").strip()
    if projects:
        right_items.append(("SPACER", 8))
        right_items.append(("SEC", "PROJECTS"))
        for line in projects.splitlines():
            if line.strip():
                right_items.append(("BODY", line.strip()))

    # ── Convert items → flowables ─────────────────────────────────────────────
    def to_flowable(kind: str, val, col_w: float, is_left: bool):
        """Return a single flowable for one item."""
        if kind == "SPACER":
            return Spacer(1, float(val))
        if kind == "SEC":
            return Paragraph(val.upper(), ST["sec"])
        if kind == "BOLD":
            return Paragraph(val, ST["bold"])
        if kind == "MUTED":
            return Paragraph(val, ST["muted"])
        if kind == "BODY":
            return Paragraph(val, ST["body"])
        if kind == "SKILL":
            # Simple background pill — plain 1×1 Table, NO ROUNDEDCORNERS
            inner_w = col_w - 16   # 8pt padding each side
            pill = Table([[Paragraph(val, ST["skill"])]], colWidths=[inner_w])
            pill.setStyle(TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), LIGHT),
                ("TOPPADDING",    (0,0), (-1,-1), 4),
                ("BOTTOMPADDING", (0,0), (-1,-1), 4),
                ("LEFTPADDING",   (0,0), (-1,-1), 8),
                ("RIGHTPADDING",  (0,0), (-1,-1), 8),
            ]))
            return pill
        return Spacer(1, 1)

    left_flows  = [to_flowable(k, v, LEFT_W,  True)  for k, v in left_items]
    right_flows = [to_flowable(k, v, RIGHT_W, False) for k, v in right_items]

    # Pad to equal length
    n = max(len(left_flows), len(right_flows), 1)
    left_flows  += [Spacer(1, 1)] * (n - len(left_flows))
    right_flows += [Spacer(1, 1)] * (n - len(right_flows))

    # ── Two-column Table (row-per-flowable, no KeepInFrame) ───────────────────
    rows = [[l, r] for l, r in zip(left_flows, right_flows)]

    body = Table(rows, colWidths=[LEFT_W, RIGHT_W + GAP_W], hAlign="LEFT")
    body.setStyle(TableStyle([
        ("VALIGN",          (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",      (0,0), (-1,-1), 1),
        ("BOTTOMPADDING",   (0,0), (-1,-1), 1),
        ("LEFTPADDING",     (0,0), (-1,-1), 2),
        ("RIGHTPADDING",    (0,0), (-1,-1), 2),
        ("LEFTPADDING",     (1,0), (1,-1),  10),
        # Thin vertical rule between columns
        ("LINEAFTER",       (0,0), (0,-1),  0.5, BORDER),
    ]))
    story.append(body)

    doc.build(story)
    return buf.getvalue()
