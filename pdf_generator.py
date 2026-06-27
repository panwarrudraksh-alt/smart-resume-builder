"""
pdf_generator.py – ResumeForge Pro
Complete PDF generator for all document types
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
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

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

# ── RESUME GENERATOR ─────────────────────────────────────────────────────────
def generate_resume_pdf(data):
    """Generate a professional resume."""
    buf = io.BytesIO()
    
    try:
        theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
        PRIMARY = _hex(theme["primary"])
        LIGHT = _hex(theme["light"])
        DARK = _hex(theme["dark"])
        
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=BM,
        )
        
        story = []
        
        # Header
        name = data.get("name", "Your Name").strip() or "Your Name"
        title = data.get("title", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        location = data.get("location", "").strip()
        linkedin = data.get("linkedin", "").strip()
        
        contact_parts = [p for p in [email, phone, location, linkedin] if p]
        contact = " · ".join(contact_parts)
        
        hdr_data = [[Paragraph(name, _style("Name", "Helvetica-Bold", 22, colors.white, 28))]]
        if title:
            hdr_data.append([Paragraph(title, _style("Title", size=12, color=colors.white, leading=16))])
        if contact:
            hdr_data.append([Paragraph(contact, _style("Contact", size=8.5, color=colors.white, leading=12))])
        
        hdr = Table(hdr_data, colWidths=[BODY_W])
        hdr.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING", (0,0), (-1,-1), 16),
            ("RIGHTPADDING", (0,0), (-1,-1), 16),
        ]))
        story.append(hdr)
        story.append(Spacer(1, 6*mm))
        
        # Summary
        summary = data.get("summary", "").strip()
        if summary:
            story.append(Paragraph(summary, _style("Summary", size=9.5, color="#333333", leading=14, sa=8)))
            story.append(Spacer(1, 3*mm))
        
        # Skills
        skills = [s.strip() for s in (data.get("skills") or []) if s and s.strip()]
        if skills:
            story.append(Paragraph("SKILLS", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            for sk in skills:
                story.append(Paragraph(f"• {sk.title()}", _style("Body", size=9.5, color="#333333", leading=13)))
            story.append(Spacer(1, 5*mm))
        
        # Experience
        role = (data.get("role", "") or "").strip()
        company = (data.get("company", "") or "").strip()
        duration = (data.get("duration", "") or "").strip()
        exp_desc = (data.get("exp_desc", "") or "").strip()
        
        if role or company or duration or exp_desc:
            story.append(Paragraph("EXPERIENCE", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            if role:
                story.append(Paragraph(role, _style("Bold", "Helvetica-Bold", 10, "#0f0f0f", 13)))
            co_line = " · ".join(filter(None, [company, duration]))
            if co_line:
                story.append(Paragraph(co_line, _style("Muted", size=8.5, color="#666666", leading=11)))
            if exp_desc:
                for line in exp_desc.split('\n'):
                    if line.strip():
                        story.append(Paragraph(f"• {line.strip()}", _style("Body", size=9.5, color="#333333", leading=13)))
            story.append(Spacer(1, 5*mm))
        
        # Education
        degree = (data.get("degree", "") or "").strip()
        institution = (data.get("institution", "") or "").strip()
        year = (data.get("year", "") or "").strip()
        
        if degree or institution or year:
            story.append(Paragraph("EDUCATION", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            if degree:
                story.append(Paragraph(degree, _style("Bold", "Helvetica-Bold", 10, "#0f0f0f", 13)))
            inst_line = " · ".join(filter(None, [institution, year]))
            if inst_line:
                story.append(Paragraph(inst_line, _style("Muted", size=8.5, color="#666666", leading=11)))
            story.append(Spacer(1, 5*mm))
        
        # Projects
        projects = (data.get("projects", "") or "").strip()
        if projects:
            story.append(Paragraph("PROJECTS", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            for line in projects.split('\n'):
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", _style("Body", size=9.5, color="#333333", leading=13)))
        
        doc.build(story)
        
    except Exception as e:
        error_buf = io.BytesIO()
        c = canvas.Canvas(error_buf, pagesize=A4)
        c.drawString(50, 750, f"Error: {str(e)}")
        c.save()
        return error_buf.getvalue()
    
    return buf.getvalue()

# ── CV GENERATOR ─────────────────────────────────────────────────────────────
def generate_cv_pdf(data):
    """Generate a comprehensive CV."""
    buf = io.BytesIO()
    
    try:
        theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
        PRIMARY = _hex(theme["primary"])
        
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=BM,
        )
        
        story = []
        
        # Header
        name = data.get("name", "Your Name").strip() or "Your Name"
        title = data.get("title", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        location = data.get("location", "").strip()
        linkedin = data.get("linkedin", "").strip()
        
        contact_parts = [p for p in [email, phone, location, linkedin] if p]
        contact = " · ".join(contact_parts)
        
        hdr_data = [[Paragraph(name, _style("Name", "Helvetica-Bold", 22, colors.white, 28))]]
        if title:
            hdr_data.append([Paragraph(title, _style("Title", size=12, color=colors.white, leading=16))])
        if contact:
            hdr_data.append([Paragraph(contact, _style("Contact", size=8.5, color=colors.white, leading=12))])
        
        hdr = Table(hdr_data, colWidths=[BODY_W])
        hdr.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
            ("TOPPADDING", (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING", (0,0), (-1,-1), 16),
            ("RIGHTPADDING", (0,0), (-1,-1), 16),
        ]))
        story.append(hdr)
        story.append(Spacer(1, 6*mm))
        
        # Summary
        summary = data.get("summary", "").strip()
        if summary:
            story.append(Paragraph(summary, _style("Summary", size=9.5, color="#333333", leading=14, sa=8)))
            story.append(Spacer(1, 3*mm))
        
        # Skills
        skills = [s.strip() for s in (data.get("skills") or []) if s and s.strip()]
        if skills:
            story.append(Paragraph("SKILLS", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            for sk in skills:
                story.append(Paragraph(f"• {sk.title()}", _style("Body", size=9.5, color="#333333", leading=13)))
            story.append(Spacer(1, 5*mm))
        
        # Experience
        role = (data.get("role", "") or "").strip()
        company = (data.get("company", "") or "").strip()
        duration = (data.get("duration", "") or "").strip()
        exp_desc = (data.get("exp_desc", "") or "").strip()
        
        if role or company or duration or exp_desc:
            story.append(Paragraph("EXPERIENCE", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            if role:
                story.append(Paragraph(role, _style("Bold", "Helvetica-Bold", 10, "#0f0f0f", 13)))
            co_line = " · ".join(filter(None, [company, duration]))
            if co_line:
                story.append(Paragraph(co_line, _style("Muted", size=8.5, color="#666666", leading=11)))
            if exp_desc:
                for line in exp_desc.split('\n'):
                    if line.strip():
                        story.append(Paragraph(f"• {line.strip()}", _style("Body", size=9.5, color="#333333", leading=13)))
            story.append(Spacer(1, 5*mm))
        
        # Education
        degree = (data.get("degree", "") or "").strip()
        institution = (data.get("institution", "") or "").strip()
        year = (data.get("year", "") or "").strip()
        
        if degree or institution or year:
            story.append(Paragraph("EDUCATION", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            if degree:
                story.append(Paragraph(degree, _style("Bold", "Helvetica-Bold", 10, "#0f0f0f", 13)))
            inst_line = " · ".join(filter(None, [institution, year]))
            if inst_line:
                story.append(Paragraph(inst_line, _style("Muted", size=8.5, color="#666666", leading=11)))
            story.append(Spacer(1, 5*mm))
        
        # Publications
        publications = (data.get("publications", "") or "").strip()
        if publications:
            story.append(Paragraph("PUBLICATIONS", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            for pub in publications.split('\n'):
                if pub.strip():
                    story.append(Paragraph(f"• {pub.strip()}", _style("Body", size=9.5, color="#333333", leading=13)))
            story.append(Spacer(1, 5*mm))
        
        # Projects
        projects = (data.get("projects", "") or "").strip()
        if projects:
            story.append(Paragraph("PROJECTS", _style("Sec", "Helvetica-Bold", 9, PRIMARY, 12, sb=6, sa=1)))
            for line in projects.split('\n'):
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", _style("Body", size=9.5, color="#333333", leading=13)))
        
        doc.build(story)
        
    except Exception as e:
        error_buf = io.BytesIO()
        c = canvas.Canvas(error_buf, pagesize=A4)
        c.drawString(50, 750, f"Error: {str(e)}")
        c.save()
        return error_buf.getvalue()
    
    return buf.getvalue()

# ── COVER LETTER GENERATOR ──────────────────────────────────────────────────
def generate_cover_letter_pdf(data):
    """Generate a professional cover letter."""
    buf = io.BytesIO()
    
    try:
        theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
        PRIMARY = _hex(theme["primary"])
        DARK = _hex(theme["dark"])
        
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=BM,
        )
        
        story = []
        
        name = data.get("name", "Your Name").strip() or "Your Name"
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        location = data.get("location", "").strip()
        
        # Sender info
        story.append(Paragraph(name, _style("Name", "Helvetica-Bold", 16, DARK, 20)))
        if email or phone:
            contact = " | ".join(filter(None, [email, phone]))
            story.append(Paragraph(contact, _style("Contact", size=9, color="#666666", leading=12)))
        if location:
            story.append(Paragraph(location, _style("Contact", size=9, color="#666666", leading=12)))
        story.append(Spacer(1, 8*mm))
        
        # Date
        story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), 
                              _style("Date", size=9.5, color="#333333", align=TA_RIGHT, sa=6)))
        story.append(Spacer(1, 3*mm))
        
        # Recipient
        company = data.get("cover_company", "Company Name").strip()
        position = data.get("cover_position", "Position").strip()
        recruiter = data.get("cover_recruiter", "").strip()
        
        if recruiter:
            story.append(Paragraph(recruiter, _style("Recipient", "Helvetica-Bold", 10, "#333333", leading=14)))
        story.append(Paragraph(company, _style("Recipient", "Helvetica-Bold", 10, "#333333", leading=14)))
        if position:
            story.append(Paragraph(f"Re: Application for {position}", 
                                  _style("Subject", size=10, color="#333333", leading=14, sa=6)))
        story.append(Spacer(1, 3*mm))
        
        # Body
        salutation = f"Dear {recruiter if recruiter else 'Hiring Manager'}," if recruiter else "Dear Hiring Manager,"
        story.append(Paragraph(salutation, _style("Body", size=10, color="#333333", leading=16, sa=4)))
        
        # Opening
        opening = data.get("cover_custom", "").strip()
        if opening:
            story.append(Paragraph(opening, _style("Body", size=10, color="#333333", leading=16, sa=6)))
        else:
            opening_text = f"I am writing to express my strong interest in the {position} position at {company}. " \
                          f"With my experience in {', '.join(data.get('skills', ['my field']))}, " \
                          f"I am confident I would be a valuable addition to your team."
            story.append(Paragraph(opening_text, _style("Body", size=10, color="#333333", leading=16, sa=6)))
        
        # Closing
        closing = "I would welcome the opportunity to discuss how my experience can contribute to your success. " \
                  "Thank you for your time and consideration."
        story.append(Paragraph(closing, _style("Body", size=10, color="#333333", leading=16, sa=6)))
        
        story.append(Spacer(1, 8*mm))
        story.append(Paragraph("Sincerely,", _style("Closing", size=10, color="#333333", leading=16, sa=4)))
        story.append(Paragraph(name, _style("Name", "Helvetica-Bold", 11, DARK, 16)))
        
        doc.build(story)
        
    except Exception as e:
        error_buf = io.BytesIO()
        c = canvas.Canvas(error_buf, pagesize=A4)
        c.drawString(50, 750, f"Error: {str(e)}")
        c.save()
        return error_buf.getvalue()
    
    return buf.getvalue()

# ── PROPOSAL GENERATOR ──────────────────────────────────────────────────────
def generate_proposal_pdf(data):
    """Generate a professional project proposal."""
    buf = io.BytesIO()
    
    try:
        theme = THEMES.get(data.get("theme", "Classic Green"), THEMES["Classic Green"])
        PRIMARY = _hex(theme["primary"])
        
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=BM,
        )
        
        story = []
        
        # Title
        title_text = data.get("proposal_title", "Project Proposal")
        story.append(Paragraph(title_text, _style("Title", "Helvetica-Bold", 20, PRIMARY, 28, align=TA_CENTER)))
        story.append(Spacer(1, 3*mm))
        
        # Meta info
        client = data.get("proposal_client", "Client")
        name = data.get("name", "Your Name")
        
        story.append(Paragraph(f"Prepared for: <b>{client}</b>", 
                              _style("Meta", size=10, color="#333333", leading=16, align=TA_CENTER)))
        story.append(Paragraph(f"Prepared by: <b>{name}</b>", 
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
        story.append(Paragraph("─" * 50, _style("Separator", size=8, color="#cccccc", leading=10, align=TA_CENTER)))
        story.append(Spacer(1, 6*mm))
        
        # Executive Summary
        if data.get("proposal_summary"):
            story.append(Paragraph("<b>Executive Summary</b>", 
                                  _style("Section", "Helvetica-Bold", 12, PRIMARY, 16, sb=6)))
            story.append(Paragraph(data["proposal_summary"], 
                                  _style("Body", size=10, color="#333333", leading=16, sa=6)))
            story.append(Spacer(1, 3*mm))
        
        # Approach
        if data.get("proposal_approach"):
            story.append(Paragraph("<b>Approach & Methodology</b>", 
                                  _style("Section", "Helvetica-Bold", 12, PRIMARY, 16, sb=6)))
            for line in data["proposal_approach"].split('\n'):
                if line.strip():
                    story.append(Paragraph(f"• {line.strip()}", 
                                          _style("Body", size=10, color="#333333", leading=16)))
            story.append(Spacer(1, 3*mm))
        
        # About Us
        story.append(Paragraph("<b>About Us</b>", 
                              _style("Section", "Helvetica-Bold", 12, PRIMARY, 16, sb=6)))
        skills_text = ", ".join(data.get("skills", ["professional services"]))
        about_text = f"{name} brings extensive experience in the field, with expertise in {skills_text}. " \
                     f"We are committed to delivering exceptional results."
        story.append(Paragraph(about_text, _style("Body", size=10, color="#333333", leading=16, sa=6)))
        
        doc.build(story)
        
    except Exception as e:
        error_buf = io.BytesIO()
        c = canvas.Canvas(error_buf, pagesize=A4)
        c.drawString(50, 750, f"Error: {str(e)}")
        c.save()
        return error_buf.getvalue()
    
    return buf.getvalue()

# ── EXPERIENCE LETTER GENERATOR ─────────────────────────────────────────────
def generate_experience_letter_pdf(data):
    """Generate a professional experience letter."""
    buf = io.BytesIO()
    
    try:
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
        story.append(Paragraph(company.upper(), _style("Company", "Helvetica-Bold", 18, PRIMARY, 24, align=TA_CENTER)))
        story.append(Paragraph("─" * 50, _style("Separator", size=10, color="#cccccc", leading=12, align=TA_CENTER)))
        story.append(Spacer(1, 8*mm))
        
        # Date
        story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", 
                              _style("Date", size=10, color="#333333", leading=14, align=TA_RIGHT, sa=6)))
        story.append(Spacer(1, 4*mm))
        
        # Subject
        story.append(Paragraph("<b>TO WHOM IT MAY CONCERN</b>", 
                              _style("Subject", "Helvetica-Bold", 11, DARK, 16, align=TA_CENTER, sa=6)))
        story.append(Spacer(1, 6*mm))
        
        # Employee info
        employee = data.get("exp_employee", "Employee Name")
        position = data.get("exp_position", "Position Held")
        period = data.get("exp_period", "Employment Period")
        
        story.append(Paragraph(f"This is to certify that <b>{employee}</b> was employed with us as <b>{position}</b> "
                              f"from <b>{period}</b>.",
                              _style("Body", size=10.5, color="#333333", leading=18, sa=8)))
        
        # Remarks
        if data.get("exp_remarks"):
            story.append(Paragraph("<b>Performance & Conduct:</b>", 
                                  _style("Section", "Helvetica-Bold", 10.5, DARK, 16, sb=4)))
            story.append(Paragraph(data["exp_remarks"], 
                                  _style("Body", size=10, color="#333333", leading=17, sa=8)))
        
        # Closing
        story.append(Paragraph(f"We wish {employee} all the very best in future endeavors.",
                              _style("Body", size=10, color="#333333", leading=17, sa=8)))
        
        story.append(Spacer(1, 12*mm))
        
        # Issuer
        issuer = data.get("exp_issuer", "Issuer Name")
        issuer_title = data.get("exp_issuer_title", "Issuer Title")
        story.append(Paragraph(f"<b>{issuer}</b>", _style("Issuer", "Helvetica-Bold", 11, DARK, 16)))
        story.append(Paragraph(issuer_title, _style("IssuerTitle", size=10, color="#555555", leading=14)))
        
        doc.build(story)
        
    except Exception as e:
        error_buf = io.BytesIO()
        c = canvas.Canvas(error_buf, pagesize=A4)
        c.drawString(50, 750, f"Error: {str(e)}")
        c.save()
        return error_buf.getvalue()
    
    return buf.getvalue()
