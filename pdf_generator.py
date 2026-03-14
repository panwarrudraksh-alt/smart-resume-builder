"""
pdf_generator.py
Generates professional resume PDFs using ReportLab.
Three themes: Classic Green, Corporate Blue, Creative Purple.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Theme definitions ─────────────────────────────────────────────────────────
THEMES = {
    "Classic Green":   {"primary": "#1D9E75", "light": "#E1F5EE", "dark": "#085041"},
    "Corporate Blue":  {"primary": "#185FA5", "light": "#E6F1FB", "dark": "#042C53"},
    "Creative Purple": {"primary": "#533AB7", "light": "#EEEDFE", "dark": "#26215C"},
}


def hex_to_color(h):
    h = h.lstrip("#")
    return colors.Color(*[int(h[i:i+2], 16)/255 for i in (0, 2, 4)])


def generate_resume_pdf(data: dict) -> bytes:
    """
    Build a PDF from resume data dict and return raw bytes.
    Called directly from Streamlit with st.download_button.
    """
    buf = io.BytesIO()

    theme_name = data.get("theme", "Classic Green")
    theme      = THEMES.get(theme_name, THEMES["Classic Green"])
    PRIMARY    = hex_to_color(theme["primary"])
    LIGHT      = hex_to_color(theme["light"])
    DARK       = hex_to_color(theme["dark"])

    # ── Document ──────────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=15*mm, leftMargin=15*mm,
        topMargin=10*mm,   bottomMargin=15*mm,
    )
    W, H = A4
    story = []

    # ── Styles ────────────────────────────────────────────────────────────────
    name_style = ParagraphStyle(
        "Name", fontName="Helvetica-Bold", fontSize=22,
        textColor=colors.white, leading=26, alignment=TA_LEFT,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", fontName="Helvetica", fontSize=11,
        textColor=colors.white, leading=14, alignment=TA_LEFT,
    )
    contact_style = ParagraphStyle(
        "Contact", fontName="Helvetica", fontSize=9,
        textColor=colors.white, leading=12, alignment=TA_LEFT,
    )
    section_head_style = ParagraphStyle(
        "SecHead", fontName="Helvetica-Bold", fontSize=9,
        textColor=PRIMARY, leading=11, spaceAfter=2,
        spaceBefore=6,
    )
    body_style = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=9.5,
        textColor=colors.HexColor("#222222"), leading=13,
    )
    bold_style = ParagraphStyle(
        "Bold", fontName="Helvetica-Bold", fontSize=10,
        textColor=colors.HexColor("#111111"), leading=13,
    )
    muted_style = ParagraphStyle(
        "Muted", fontName="Helvetica", fontSize=8.5,
        textColor=colors.HexColor("#666666"), leading=11,
    )
    skill_style = ParagraphStyle(
        "Skill", fontName="Helvetica", fontSize=8.5,
        textColor=DARK, leading=11, alignment=TA_CENTER,
    )

    # ── Helper: section divider ───────────────────────────────────────────────
    def section_title(text):
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph(text.upper(), section_head_style))
        story.append(HRFlowable(
            width="100%", thickness=1.5,
            color=PRIMARY, spaceAfter=3,
        ))

    # ── HEADER BLOCK ─────────────────────────────────────────────────────────
    contact_parts = [p for p in [
        data.get("email"), data.get("phone"),
        data.get("location"), data.get("linkedin"),
    ] if p]
    contact_line = "  ·  ".join(contact_parts)

    header_data = [
        [
            Paragraph(data.get("name") or "Your Name", name_style),
        ],
        [
            Paragraph(data.get("title") or "", subtitle_style),
        ],
        [
            Paragraph(contact_line, contact_style),
        ],
    ]
    header_table = Table(
        header_data,
        colWidths=[W - 30*mm],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PRIMARY]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4*mm))

    # ── TWO COLUMN LAYOUT ─────────────────────────────────────────────────────
    # Build left column content
    left_content  = []
    right_content = []

    # ── LEFT: Skills ──────────────────────────────────────────────────────────
    skills = data.get("skills", [])
    if skills:
        left_content.append(Paragraph("SKILLS", section_head_style))
        left_content.append(HRFlowable(
            width="100%", thickness=1.2, color=PRIMARY, spaceAfter=4))
        # Render skills as pill-style table rows
        for sk in skills:
            pill = Table(
                [[Paragraph(sk.title(), skill_style)]],
                colWidths=[45*mm],
            )
            pill.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, -1), LIGHT),
                ("TOPPADDING",    (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING",   (0, 0), (-1, -1), 6),
                ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
                ("ROUNDEDCORNERS", [4]),
            ]))
            left_content.append(pill)
            left_content.append(Spacer(1, 2))

    # ── LEFT: Education ───────────────────────────────────────────────────────
    left_content.append(Spacer(1, 6))
    left_content.append(Paragraph("EDUCATION", section_head_style))
    left_content.append(HRFlowable(
        width="100%", thickness=1.2, color=PRIMARY, spaceAfter=4))
    if data.get("degree"):
        left_content.append(Paragraph(data["degree"], bold_style))
    if data.get("institution"):
        inst_yr = data["institution"]
        if data.get("year"): inst_yr += f" · {data['year']}"
        left_content.append(Paragraph(inst_yr, muted_style))

    # ── RIGHT: Experience ─────────────────────────────────────────────────────
    right_content.append(Paragraph("EXPERIENCE", section_head_style))
    right_content.append(HRFlowable(
        width="100%", thickness=1.2, color=PRIMARY, spaceAfter=4))
    if data.get("role"):
        right_content.append(Paragraph(data["role"], bold_style))
    company_dur = " · ".join(filter(None, [data.get("company"), data.get("duration")]))
    if company_dur:
        right_content.append(Paragraph(company_dur, muted_style))
    if data.get("exp_desc"):
        right_content.append(Spacer(1, 3))
        for line in data["exp_desc"].split("\n"):
            if line.strip():
                right_content.append(Paragraph(line.strip(), body_style))
                right_content.append(Spacer(1, 1))

    # ── RIGHT: Projects ───────────────────────────────────────────────────────
    if data.get("projects"):
        right_content.append(Spacer(1, 6))
        right_content.append(Paragraph("PROJECTS", section_head_style))
        right_content.append(HRFlowable(
            width="100%", thickness=1.2, color=PRIMARY, spaceAfter=4))
        for line in data["projects"].split("\n"):
            if line.strip():
                right_content.append(Paragraph(line.strip(), body_style))
                right_content.append(Spacer(1, 2))

    # ── Assemble two-column table ─────────────────────────────────────────────
    from reportlab.platypus import KeepInFrame
    left_frame  = KeepInFrame(55*mm,  400*mm, left_content,  mode="shrink")
    right_frame = KeepInFrame(105*mm, 400*mm, right_content, mode="shrink")

    two_col = Table(
        [[left_frame, right_frame]],
        colWidths=[58*mm, 107*mm],
        hAlign="LEFT",
    )
    two_col.setStyle(TableStyle([
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("LINEAFTER",    (0, 0), (0, -1), 0.5, colors.HexColor("#e0e0e0")),
        ("RIGHTPADDING", (0, 0), (0, -1), 10),
        ("LEFTPADDING",  (1, 0), (1, -1), 10),
    ]))
    story.append(two_col)

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story)
    return buf.getvalue()
