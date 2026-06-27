"""
pdf_generator.py – ResumeForge
Generates various professional documents: Resume, CV, Cover Letter, Proposal, Experience Letter
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

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
BODY_W  = PAGE_W - LM - RM

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

# ── Helper function for bullet points ────────────────────────────────────────
def _bullet_points(text: str) -> list:
    """Convert text with bullet points to list of paragraphs."""
    result = []
    for line in text.split('\n'):
        line = line.strip()
        if line:
            if line.startswith('•') or line.startswith('-'):
                result.append(Paragraph(line, _style("Bullet", size=9.5, color="#333333", leading=13)))
            else:
                result.append(Paragraph(f"• {line}", _style("Bullet", size=9.5, color="#333333", leading=13)))
    return result

# ── DOCUMENT GENERATORS ──────────────────────────────────────────────────────

def generate_resume_pdf(data: dict) -> bytes:
    """Generate a professional resume."""
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    LIGHT = _hex(theme["light"])
    
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )
    
    story = []
    
    # Header
    story.extend(_create_header(data, PRIMARY))
    story.append(Spacer(1, 5*mm))
    
    # Two-column layout
    left_items, right_items = _prepare_resume_sections(data)
    story.append(_create_two_column_table(left_items, right_items, PRIMARY))
    
    doc.build(story)
    return buf.getvalue()

def generate_cv_pdf(data: dict) -> bytes:
    """Generate a comprehensive CV."""
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )
    
    story = []
    
    # Header
    story.extend(_create_header(data, PRIMARY))
    story.append(Spacer(1, 5*mm))
    
    # Professional Summary
    if data.get("summary"):
        story.append(Paragraph(data["summary"], _style("Summary", size=9.5, color="#333333", leading=14, sa=6)))
        story.append(Spacer(1, 3*mm))
    
    # Full layout with more sections
    story.append(_create_cv_full_layout(data, PRIMARY))
    
    doc.build(story)
    return buf.getvalue()

def generate_cover_letter_pdf(data: dict) -> bytes:
    """Generate a professional cover letter."""
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    DARK = _hex(theme["dark"])
    
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )
    
    story = []
    
    # Letter Header
    name = data.get("name", "Your Name")
    title = data.get("title", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    location = data.get("location", "")
    
    # Sender info
    story.append(Paragraph(name, _style("Name", font="Helvetica-Bold", size=16, color=DARK, leading=20)))
    if title:
        story.append(Paragraph(title, _style("Title", size=10, color="#555555", leading=14)))
    story.append(Paragraph(f"{email} | {phone}" if email and phone else email or phone, 
                          _style("Contact", size=9, color="#777777", leading=12)))
    if location:
        story.append(Paragraph(location, _style("Contact", size=9, color="#777777", leading=12)))
    story.append(Spacer(1, 8*mm))
    
    # Date
    date_str = data.get("cover_date", datetime.now().strftime("%B %d, %Y"))
    story.append(Paragraph(date_str, _style("Date", size=9.5, color="#333333", align=TA_RIGHT, sa=6)))
    story.append(Spacer(1, 3*mm))
    
    # Recipient
    company = data.get("cover_company", "Company Name")
    position = data.get("cover_position", "Position")
    story.append(Paragraph(f"<b>{company}</b>", _style("Recipient", font="Helvetica-Bold", size=10, color="#333333", leading=14)))
    story.append(Paragraph(f"Re: Application for {position}", 
                          _style("Subject", size=10, color="#333333", leading=14, sa=6)))
    story.append(Spacer(1, 3*mm))
    
    # Body
    salutation = f"Dear Hiring Manager,"
    story.append(Paragraph(salutation, _style("Body", size=10, color="#333333", leading=16, sa=4)))
    
    # Paragraph 1 - Opening
    opening = f"I am writing to express my strong interest in the {position} position at {company}. " \
              f"With {data.get('role', 'my experience')} experience in {data.get('title', 'my field')}, " \
              f"I am confident that my skills and qualifications make me an ideal candidate for this role."
    story.append(Paragraph(opening, _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    # Paragraph 2 - Skills & Experience
    skills_text = ", ".join(data.get("skills", ["technical skills"]))
    experience = f"In my current role as {data.get('role', 'professional')} at {data.get('company', 'my previous organization')}, " \
                 f"I have developed strong expertise in {skills_text}. " \
                 f"I am particularly drawn to this opportunity because of {company}'s reputation for innovation and excellence."
    story.append(Paragraph(experience, _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    # Custom paragraph
    if data.get("cover_custom"):
        story.append(Paragraph(data["cover_custom"], _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    # Closing
    closing = "I would welcome the opportunity to discuss how my experience and skills can contribute to the success of your team. " \
              "Thank you for your time and consideration."
    story.append(Paragraph(closing, _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Sincerely,", _style("Closing", size=10, color="#333333", leading=16, sa=4)))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(name, _style("Name", font="Helvetica-Bold", size=11, color=DARK, leading=16)))
    
    doc.build(story)
    return buf.getvalue()

def generate_proposal_pdf(data: dict) -> bytes:
    """Generate a professional project proposal."""
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    DARK = _hex(theme["dark"])
    
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )
    
    story = []
    
    # Title
    story.append(Paragraph(data.get("proposal_title", "Project Proposal"), 
                          _style("PropTitle", font="Helvetica-Bold", size=20, color=PRIMARY, leading=28, align=TA_CENTER)))
    story.append(Spacer(1, 3*mm))
    
    # Meta info
    story.append(Paragraph(f"Prepared for: <b>{data.get('proposal_client', 'Client')}</b>", 
                          _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    story.append(Paragraph(f"Prepared by: <b>{data.get('name', 'Your Name')}</b>", 
                          _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    story.append(Paragraph(f"Date: <b>{datetime.now().strftime('%B %d, %Y')}</b>", 
                          _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    if data.get("proposal_budget"):
        story.append(Paragraph(f"Budget: <b>{data['proposal_budget']}</b>", 
                              _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    if data.get("proposal_timeline"):
        story.append(Paragraph(f"Timeline: <b>{data['proposal_timeline']}</b>", 
                              _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    story.append(Spacer(1, 8*mm))
    
    # Separator
    story.append(Paragraph("─" * 50, _style("Separator", size=8, color="#cccccc", leading=10, align=TA_CENTER)))
    story.append(Spacer(1, 6*mm))
    
    # Executive Summary
    if data.get("proposal_summary"):
        story.append(Paragraph("<b>Executive Summary</b>", 
                              _style("Section", font="Helvetica-Bold", size=12, color=PRIMARY, leading=16, sb=6)))
        story.append(Paragraph(data["proposal_summary"], 
                              _style("Body", size=10, color="#333333", leading=16, sa=6)))
        story.append(Spacer(1, 3*mm))
    
    # Approach
    if data.get("proposal_approach"):
        story.append(Paragraph("<b>Approach & Methodology</b>", 
                              _style("Section", font="Helvetica-Bold", size=12, color=PRIMARY, leading=16, sb=6)))
        for line in data["proposal_approach"].split('\n'):
            if line.strip():
                story.append(Paragraph(f"• {line.strip()}", 
                                      _style("Body", size=10, color="#333333", leading=16)))
        story.append(Spacer(1, 3*mm))
    
    # Benefits
    if data.get("proposal_benefits"):
        story.append(Paragraph("<b>Value Proposition</b>", 
                              _style("Section", font="Helvetica-Bold", size=12, color=PRIMARY, leading=16, sb=6)))
        for line in data["proposal_benefits"].split('\n'):
            if line.strip():
                story.append(Paragraph(f"• {line.strip()}", 
                                      _style("Body", size=10, color="#333333", leading=16)))
        story.append(Spacer(1, 3*mm))
    
    # About Us
    story.append(Paragraph("<b>About Us</b>", 
                          _style("Section", font="Helvetica-Bold", size=12, color=PRIMARY, leading=16, sb=6)))
    story.append(Paragraph(f"{data.get('name', 'Our team')} brings extensive experience in the field, "
                          f"with expertise in {', '.join(data.get('skills', ['professional services']))}. "
                          f"We are committed to delivering exceptional results that align with "
                          f"client objectives and exceed expectations.",
                          _style("Body", size=10, color="#333333", leading=16, sa=6)))
    story.append(Spacer(1, 3*mm))
    
    # Contact
    story.append(Paragraph("<b>Contact Information</b>", 
                          _style("Section", font="Helvetica-Bold", size=12, color=PRIMARY, leading=16, sb=6)))
    contact_info = f"Email: {data.get('email', '')}" if data.get('email') else ""
    if data.get('phone'):
        contact_info += f" | Phone: {data['phone']}"
    if data.get('location'):
        contact_info += f" | Location: {data['location']}"
    story.append(Paragraph(contact_info, _style("Body", size=10, color="#333333", leading=16)))
    
    doc.build(story)
    return buf.getvalue()

def generate_experience_letter_pdf(data: dict) -> bytes:
    """Generate a professional experience/employment letter."""
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    DARK = _hex(theme["dark"])
    
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
    )
    
    story = []
    
    # Company Header
    company = data.get("exp_company", "Company Name")
    story.append(Paragraph(company.upper(), _style("Company", font="Helvetica-Bold", size=18, color=PRIMARY, leading=24, align=TA_CENTER)))
    story.append(Paragraph("─" * 50, _style("Separator", size=10, color="#cccccc", leading=12, align=TA_CENTER)))
    story.append(Spacer(1, 8*mm))
    
    # Date
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", 
                          _style("Date", size=10, color="#333333", leading=14, align=TA_RIGHT, sa=6)))
    story.append(Spacer(1, 4*mm))
    
    # Subject
    story.append(Paragraph("<b>TO WHOM IT MAY CONCERN</b>", 
                          _style("Subject", font="Helvetica-Bold", size=11, color=DARK, leading=16, align=TA_CENTER, sa=6)))
    story.append(Spacer(1, 6*mm))
    
    # Employee info
    employee = data.get("exp_employee", "Employee Name")
    position = data.get("exp_position", "Position Held")
    period = data.get("exp_period", "Employment Period")
    reason = data.get("exp_reason", "")
    
    story.append(Paragraph(f"This is to certify that <b>{employee}</b> was employed with us as <b>{position}</b> "
                          f"from <b>{period}</b>.",
                          _style("Body", size=10.5, color="#333333", leading=18, sa=8)))
    
    # Remarks
    if data.get("exp_remarks"):
        story.append(Paragraph("<b>Performance & Conduct:</b>", 
                              _style("Section", font="Helvetica-Bold", size=10.5, color=DARK, leading=16, sb=4)))
        story.append(Paragraph(data["exp_remarks"], 
                              _style("Body", size=10, color="#333333", leading=17, sa=8)))
    
    if reason:
        story.append(Paragraph(f"<b>Reason for Leaving:</b> {reason}", 
                              _style("Body", size=10, color="#333333", leading=17, sa=8)))
    
    # Closing
    closing_text = f"We wish {employee} all the very best in future endeavors and confirm "
    story.append(Paragraph(closing_text + "that the above information is true to the best of our knowledge.",
                          _style("Body", size=10, color="#333333", leading=17, sa=8)))
    
    story.append(Spacer(1, 8*mm))
    
    # Issuer
    issuer = data.get("exp_issuer", "Issuer Name")
    issuer_title = data.get("exp_issuer_title", "Issuer Title")
    story.append(Paragraph(f"<b>{issuer}</b>", _style("Issuer", font="Helvetica-Bold", size=11, color=DARK, leading=16)))
    story.append(Paragraph(issuer_title, _style("IssuerTitle", size=10, color="#555555", leading=14)))
    
    doc.build(story)
    return buf.getvalue()

# ── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

def _create_header(data: dict, primary_color) -> list:
    """Create the header section for resumes and CVs."""
    name = (data.get("name") or "").strip() or "Your Name"
    title = (data.get("title") or "").strip()
    contact = "   ·   ".join(filter(None, [
        data.get("email", "").strip(),
        data.get("phone", "").strip(),
        data.get("location", "").strip(),
        data.get("linkedin", "").strip(),
    ]))
    
    hdr_data = [[Paragraph(name, _style("Name", font="Helvetica-Bold", size=21, color=colors.white, leading=26))]]
    if title:
        hdr_data.append([Paragraph(title, _style("Title", size=11, color=colors.white, leading=14))])
    if contact:
        hdr_data.append([Paragraph(contact, _style("Contact", size=9, color=colors.white, leading=12))])
    
    hdr = Table(hdr_data, colWidths=[BODY_W])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), primary_color),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ]))
    return [hdr]

def _prepare_resume_sections(data: dict) -> tuple:
    """Prepare left and right sections for resume."""
    left_items = []
    right_items = []
    
    # Skills
    skills = [s.strip() for s in (data.get("skills") or []) if s and s.strip()]
    if skills:
        left_items.append(("SEC", "SKILLS"))
        for sk in skills:
            left_items.append(("SKILL", sk.title()))
            left_items.append(("SPACER", 2))
    
    # Education
    deg = (data.get("degree", "") or "").strip()
    inst = (data.get("institution", "") or "").strip()
    yr = (data.get("year", "") or "").strip()
    left_items.append(("SPACER", 8))
    left_items.append(("SEC", "EDUCATION"))
    if deg:
        left_items.append(("BOLD", deg))
    inst_line = " · ".join(filter(None, [inst, yr]))
    if inst_line:
        left_items.append(("MUTED", inst_line))
    
    # Certifications
    certs = (data.get("certifications", "") or "").strip()
    if certs:
        left_items.append(("SPACER", 8))
        left_items.append(("SEC", "CERTIFICATIONS"))
        for cert in certs.split('\n'):
            if cert.strip():
                left_items.append(("MUTED", cert.strip()))
    
    # Languages
    langs = (data.get("languages", "") or "").strip()
    if langs:
        left_items.append(("SPACER", 8))
        left_items.append(("SEC", "LANGUAGES"))
        left_items.append(("MUTED", langs))
    
    # ── Right Column ──
    # Experience
    role = (data.get("role", "") or "").strip()
    company = (data.get("company", "") or "").strip()
    duration = (data.get("duration", "") or "").strip()
    exp_desc = (data.get("exp_desc", "") or "").strip()
    
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
    
    # Additional Experience
    add_exp = (data.get("add_exp", "") or "").strip()
    if add_exp:
        right_items.append(("SPACER", 6))
        right_items.append(("MUTED", "Additional Experience:"))
        for line in add_exp.splitlines():
            if line.strip():
                right_items.append(("BODY", line.strip()))
    
    # Projects
    projects = (data.get("projects", "") or "").strip()
    if projects:
        right_items.append(("SPACER", 8))
        right_items.append(("SEC", "PROJECTS"))
        for line in projects.splitlines():
            if line.strip():
                right_items.append(("BODY", line.strip()))
    
    return left_items, right_items

def _create_cv_full_layout(data: dict, primary_color) -> Table:
    """Create full CV layout with all sections."""
    # This is a simplified version - for a full CV, we'd use a more complex layout
    # but we'll reuse the resume layout and add more sections
    left_items, right_items = _prepare_resume_sections(data)
    
    # Add more CV-specific sections
    # Publications
    pubs = (data.get("publications", "") or "").strip()
    if pubs:
        right_items.append(("SPACER", 8))
        right_items.append(("SEC", "PUBLICATIONS"))
        for pub in pubs.split('\n'):
            if pub.strip():
                right_items.append(("BODY", pub.strip()))
    
    # Affiliations
    aff = (data.get("affiliations", "") or "").strip()
    if aff:
        right_items.append(("SPACER", 6))
        right_items.append(("SEC", "PROFESSIONAL AFFILIATIONS"))
        right_items.append(("BODY", aff))
    
    # Interests
    interests = (data.get("interests", "") or "").strip()
    if interests:
        right_items.append(("SPACER", 6))
        right_items.append(("SEC", "INTERESTS"))
        right_items.append(("BODY", interests))
    
    return _create_two_column_table(left_items, right_items, primary_color)

def _create_two_column_table(left_items: list, right_items: list, primary_color) -> Table:
    """Create a two-column table layout."""
    LEFT_W = 58 * mm
    GAP_W = 6 * mm
    RIGHT_W = BODY_W - LEFT_W - GAP_W
    
    # Style definitions for column items
    styles = {
        "SPACER": lambda v: Spacer(1, float(v)),
        "SEC": lambda v: Paragraph(v.upper(), _style("Sec", font="Helvetica-Bold", size=9, color=primary_color, leading=12, sb=6, sa=1)),
        "BOLD": lambda v: Paragraph(v, _style("Bold", font="Helvetica-Bold", size=10, color="#0f0f0f", leading=13)),
        "MUTED": lambda v: Paragraph(v, _style("Muted", size=8.5, color="#555555", leading=11)),
        "BODY": lambda v: Paragraph(v, _style("Body", size=9.5, color="#222222", leading=13)),
        "SKILL": lambda v: _create_skill_pill(v, primary_color),
    }
    
    def to_flowable(kind: str, val, col_w: float):
        func = styles.get(kind, lambda v: Spacer(1, 1))
        return func(val)
    
    left_flows = [to_flowable(k, v, LEFT_W) for k, v in left_items]
    right_flows = [to_flowable(k, v, RIGHT_W) for k, v in right_items]
    
    # Pad to equal length
    n = max(len(left_flows), len(right_flows), 1)
    left_flows += [Spacer(1, 1)] * (n - len(left_flows))
    right_flows += [Spacer(1, 1)] * (n - len(right_flows))
    
    rows = [[l, r] for l, r in zip(left_flows, right_flows)]
    
    body = Table(rows, colWidths=[LEFT_W, RIGHT_W + GAP_W], hAlign="LEFT")
    body.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 1),
        ("BOTTOMPADDING", (0,0), (-1,-1), 1),
        ("LEFTPADDING", (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING", (1,0), (1,-1), 10),
        ("LINEAFTER", (0,0), (0,-1), 0.5, _hex("#e0e0e0")),
    ]))
    return body

def _create_skill_pill(text: str, primary_color) -> Table:
    """Create a skill badge/pill."""
    pill = Table([[Paragraph(text, _style("Skill", size=8.5, color=primary_color, leading=11, align=TA_CENTER))]], 
                 colWidths=[58*mm - 16])
    pill.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), _hex("#E1F5EE")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ]))
    return pill
