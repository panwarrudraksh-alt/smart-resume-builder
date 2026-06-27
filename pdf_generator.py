"""
pdf_generator.py – ResumeForge
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "Classic Green": {"primary": "#1D9E75", "light": "#E1F5EE", "dark": "#085041"},
    "Corporate Blue": {"primary": "#185FA5", "light": "#E6F1FB", "dark": "#042C53"},
    "Creative Purple": {"primary": "#533AB7", "light": "#EEEDFE", "dark": "#26215C"},
}

def _hex(h):
    h = h.lstrip("#")
    return colors.Color(int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255)

PAGE_W, PAGE_H = A4
LM, RM, TM, BM = 15*mm, 15*mm, 10*mm, 15*mm
BODY_W = PAGE_W - LM - RM

def _style(name, font="Helvetica", size=10, color="#111111", leading=None, align=TA_LEFT, sb=0, sa=0):
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

# ── Resume Generator ─────────────────────────────────────────────────────────
def generate_resume_pdf(data):
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM)
    story = []
    
    # Header
    name = data.get("name", "Your Name")
    title = data.get("title", "")
    contact = " · ".join(filter(None, [data.get("email", ""), data.get("phone", ""), data.get("location", "")]))
    
    hdr_data = [[Paragraph(name, _style("Name", font="Helvetica-Bold", size=20, color=colors.white, leading=26))]]
    if title:
        hdr_data.append([Paragraph(title, _style("Title", size=11, color=colors.white, leading=14))])
    if contact:
        hdr_data.append([Paragraph(contact, _style("Contact", size=9, color=colors.white, leading=12))])
    
    hdr = Table(hdr_data, colWidths=[BODY_W])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 5*mm))
    
    # Skills
    skills = data.get("skills", [])
    if skills:
        story.append(Paragraph("SKILLS", _style("Sec", font="Helvetica-Bold", size=9, color=PRIMARY, leading=12, sb=6)))
        for sk in skills:
            story.append(Paragraph(f"• {sk.title()}", _style("Body", size=9.5, color="#222222", leading=13)))
        story.append(Spacer(1, 5*mm))
    
    # Experience
    if data.get("role") or data.get("company"):
        story.append(Paragraph("EXPERIENCE", _style("Sec", font="Helvetica-Bold", size=9, color=PRIMARY, leading=12, sb=6)))
        if data.get("role"):
            story.append(Paragraph(data["role"], _style("Bold", font="Helvetica-Bold", size=10, color="#0f0f0f", leading=13)))
        co_line = " · ".join(filter(None, [data.get("company", ""), data.get("duration", "")]))
        if co_line:
            story.append(Paragraph(co_line, _style("Muted", size=8.5, color="#555555", leading=11)))
        if data.get("exp_desc"):
            for line in data["exp_desc"].split('\n'):
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", _style("Body", size=9.5, color="#222222", leading=13)))
        story.append(Spacer(1, 5*mm))
    
    # Education
    if data.get("degree") or data.get("institution"):
        story.append(Paragraph("EDUCATION", _style("Sec", font="Helvetica-Bold", size=9, color=PRIMARY, leading=12, sb=6)))
        if data.get("degree"):
            story.append(Paragraph(data["degree"], _style("Bold", font="Helvetica-Bold", size=10, color="#0f0f0f", leading=13)))
        inst_line = " · ".join(filter(None, [data.get("institution", ""), data.get("year", "")]))
        if inst_line:
            story.append(Paragraph(inst_line, _style("Muted", size=8.5, color="#555555", leading=11)))
    
    # Projects
    if data.get("projects"):
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph("PROJECTS", _style("Sec", font="Helvetica-Bold", size=9, color=PRIMARY, leading=12, sb=6)))
        for line in data["projects"].split('\n'):
            if line.strip():
                story.append(Paragraph(f"• {line.strip()}", _style("Body", size=9.5, color="#222222", leading=13)))
    
    doc.build(story)
    return buf.getvalue()

# ── CV Generator ─────────────────────────────────────────────────────────────
def generate_cv_pdf(data):
    # Same as resume but with more sections
    return generate_resume_pdf(data)

# ── Cover Letter Generator ──────────────────────────────────────────────────
def generate_cover_letter_pdf(data):
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM)
    story = []
    
    name = data.get("name", "Your Name")
    email = data.get("email", "")
    phone = data.get("phone", "")
    
    # Header
    story.append(Paragraph(name, _style("Name", font="Helvetica-Bold", size=16, color="#085041", leading=20)))
    story.append(Paragraph(f"{email} | {phone}" if email and phone else email or phone, 
                          _style("Contact", size=9, color="#555555", leading=12)))
    story.append(Spacer(1, 8*mm))
    
    # Date
    story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), 
                          _style("Date", size=9.5, color="#333333", align=TA_RIGHT, sa=6)))
    story.append(Spacer(1, 3*mm))
    
    # Recipient
    company = data.get("cover_company", "Company Name")
    position = data.get("cover_position", "Position")
    story.append(Paragraph(f"<b>{company}</b>", _style("Recipient", font="Helvetica-Bold", size=10, color="#333333", leading=14)))
    story.append(Paragraph(f"Re: Application for {position}", 
                          _style("Subject", size=10, color="#333333", leading=14, sa=6)))
    story.append(Spacer(1, 3*mm))
    
    # Body
    story.append(Paragraph("Dear Hiring Manager,", _style("Body", size=10, color="#333333", leading=16, sa=4)))
    
    opening = f"I am writing to express my strong interest in the {position} position at {company}. " \
              f"With experience in {', '.join(data.get('skills', ['my field']))}, " \
              f"I am confident that my skills and qualifications make me an ideal candidate."
    story.append(Paragraph(opening, _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    if data.get("cover_custom"):
        story.append(Paragraph(data["cover_custom"], _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    closing = "I would welcome the opportunity to discuss how my experience can contribute to your team. Thank you for your consideration."
    story.append(Paragraph(closing, _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Sincerely,", _style("Closing", size=10, color="#333333", leading=16, sa=4)))
    story.append(Paragraph(name, _style("Name", font="Helvetica-Bold", size=11, color="#085041", leading=16)))
    
    doc.build(story)
    return buf.getvalue()

# ── Proposal Generator ──────────────────────────────────────────────────────
def generate_proposal_pdf(data):
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM)
    story = []
    
    # Title
    story.append(Paragraph(data.get("proposal_title", "Project Proposal"), 
                          _style("Title", font="Helvetica-Bold", size=20, color=PRIMARY, leading=28, align=TA_CENTER)))
    story.append(Spacer(1, 3*mm))
    
    # Meta
    story.append(Paragraph(f"Prepared for: <b>{data.get('proposal_client', 'Client')}</b>", 
                          _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    story.append(Paragraph(f"Prepared by: <b>{data.get('name', 'Your Name')}</b>", 
                          _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    story.append(Paragraph(f"Date: <b>{datetime.now().strftime('%B %d, %Y')}</b>", 
                          _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    if data.get("proposal_budget"):
        story.append(Paragraph(f"Budget: <b>{data['proposal_budget']}</b>", 
                              _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
    story.append(Spacer(1, 8*mm))
    
    # Summary
    if data.get("proposal_summary"):
        story.append(Paragraph("<b>Executive Summary</b>", 
                              _style("Section", font="Helvetica-Bold", size=12, color=PRIMARY, leading=16, sb=6)))
        story.append(Paragraph(data["proposal_summary"], 
                              _style("Body", size=10, color="#333333", leading=16, sa=6)))
    
    doc.build(story)
    return buf.getvalue()

# ── Experience Letter Generator ─────────────────────────────────────────────
def generate_experience_letter_pdf(data):
    buf = io.BytesIO()
    theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
    PRIMARY = _hex(theme["primary"])
    
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM)
    story = []
    
    company = data.get("exp_company", "Company Name")
    story.append(Paragraph(company.upper(), _style("Company", font="Helvetica-Bold", size=18, color=PRIMARY, leading=24, align=TA_CENTER)))
    story.append(Paragraph("─" * 50, _style("Separator", size=10, color="#cccccc", leading=12, align=TA_CENTER)))
    story.append(Spacer(1, 8*mm))
    
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", 
                          _style("Date", size=10, color="#333333", leading=14, align=TA_RIGHT, sa=6)))
    story.append(Spacer(1, 4*mm))
    
    story.append(Paragraph("<b>TO WHOM IT MAY CONCERN</b>", 
                          _style("Subject", font="Helvetica-Bold", size=11, color="#085041", leading=16, align=TA_CENTER, sa=6)))
    story.append(Spacer(1, 6*mm))
    
    employee = data.get("exp_employee", "Employee Name")
    position = data.get("exp_position", "Position Held")
    period = data.get("exp_period", "Employment Period")
    
    story.append(Paragraph(f"This is to certify that <b>{employee}</b> was employed with us as <b>{position}</b> "
                          f"from <b>{period}</b>.",
                          _style("Body", size=10.5, color="#333333", leading=18, sa=8)))
    
    if data.get("exp_remarks"):
        story.append(Paragraph("<b>Performance:</b>", 
                              _style("Section", font="Helvetica-Bold", size=10.5, color="#085041", leading=16, sb=4)))
        story.append(Paragraph(data["exp_remarks"], 
                              _style("Body", size=10, color="#333333", leading=17, sa=8)))
    
    story.append(Paragraph("We wish the employee all the best in future endeavors.",
                          _style("Body", size=10, color="#333333", leading=17, sa=8)))
    
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("<b>Issued By:</b>", _style("Issuer", font="Helvetica-Bold", size=10, color="#333333", leading=16)))
    
    doc.build(story)
    return buf.getvalue()
