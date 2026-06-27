import streamlit as st
import io
from datetime import datetime

# Try importing with error handling
try:
    from pdf_generator import (
        generate_resume_pdf, 
        generate_cover_letter_pdf, 
        generate_proposal_pdf, 
        generate_experience_letter_pdf, 
        generate_cv_pdf
    )
    from job_scraper import get_jobs, match_skills
except Exception as e:
    st.error(f"⚠️ Error loading modules: {str(e)}")
    st.stop()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeForge – Smart Document Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.main-header {
    background: linear-gradient(135deg, #1D9E75 0%, #085041 100%);
    color: white; padding: 2rem 2.5rem; border-radius: 16px;
    margin-bottom: 2rem;
}
.main-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem; margin: 0; font-weight: 400;
}
.main-header p { margin: 0.5rem 0 0; opacity: 0.85; font-size: 1.05rem; }

.document-card {
    background: white;
    border: 2px solid #e8e8e8;
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    height: 100%;
}
.document-card:hover {
    border-color: #1D9E75;
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(29, 158, 117, 0.1);
}
.document-card .icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}
.document-card .title {
    font-weight: 600;
    font-size: 1.1rem;
    color: #1D9E75;
}
.document-card .desc {
    font-size: 0.85rem;
    color: #666;
    margin-top: 0.5rem;
}

.section-card {
    background: white; border: 1px solid #e8e8e8;
    border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
}

.skill-badge {
    display: inline-block; padding: 3px 10px;
    background: #E1F5EE; color: #085041;
    border-radius: 20px; font-size: 0.78rem;
    font-weight: 500; margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "skills": [],
    "jobs": [],
    "template": "Classic Green",
    "resume_built": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📄 ResumeForge")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📝 Document Builder", "🔍 Job Scraper", "📄 Document Generator"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Quick stats**")
    col1, col2 = st.columns(2)
    col1.metric("Skills", len(st.session_state.skills))
    col2.metric("Jobs", len(st.session_state.jobs))
    st.markdown("---")
    st.caption("Built with Streamlit · ReportLab · BeautifulSoup")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>ResumeForge</h1>
        <p>Create professional documents: Resumes, CVs, Cover Letters, Proposals, and Experience Letters</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    documents = [
        ("📄", "Resume", "ATS-friendly resume with skills & experience"),
        ("📋", "CV", "Comprehensive curriculum vitae"),
        ("✉️", "Cover Letter", "Customizable cover letter for job applications"),
        ("📊", "Proposal", "Professional project proposal"),
    ]
    
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], documents):
        with col:
            st.markdown(f"""
            <div class="document-card">
                <div class="icon">{icon}</div>
                <div class="title">{title}</div>
                <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-card" style="margin-top: 2rem;">
        <h3>🚀 How it works</h3>
        <ol style="font-size: 1rem; line-height: 1.8;">
            <li><strong>Fill your information</strong> once in the Document Builder</li>
            <li><strong>Choose a document type</strong> from the Document Generator</li>
            <li><strong>Customize</strong> the document with additional details</li>
            <li><strong>Download</strong> your professional PDF instantly</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DOCUMENT BUILDER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Document Builder":
    st.markdown("## 📝 Document Builder")
    st.markdown("Fill in your details once. All documents will use this information.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Personal Info", "💼 Experience", "🎓 Education", "🛠️ Skills & Projects"
    ])

    with tab1:
        st.markdown("#### Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", key="f_name", placeholder="Jane Doe")
            email = st.text_input("Email *", key="f_email", placeholder="jane@email.com")
            phone = st.text_input("Phone", key="f_phone", placeholder="+91 9876543210")
        with col2:
            title = st.text_input("Professional Title", key="f_title", placeholder="Software Engineer")
            loc = st.text_input("Location", key="f_loc", placeholder="New Delhi, India")
            linkedin = st.text_input("LinkedIn URL", key="f_linkedin", placeholder="linkedin.com/in/jane")

    with tab2:
        st.markdown("#### Work Experience")
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company", key="f_company", placeholder="TechCorp Inc.")
            exp_role = st.text_input("Role/Position", key="f_exp_role", placeholder="Senior Developer")
        with col2:
            duration = st.text_input("Duration", key="f_duration", placeholder="Jan 2022 – Present")
        exp_desc = st.text_area("Job Description", key="f_exp_desc",
            placeholder="• Built REST APIs serving 10k users/day\n• Reduced latency by 40%", height=100)

    with tab3:
        st.markdown("#### Education")
        col1, col2, col3 = st.columns(3)
        with col1: 
            degree = st.text_input("Degree", key="f_degree", placeholder="B.Tech in Computer Science")
        with col2:   
            inst = st.text_input("Institution", key="f_inst", placeholder="IIT Delhi")
        with col3:   
            year = st.text_input("Year", key="f_year", placeholder="2018–2022")

    with tab4:
        st.markdown("#### Skills")
        col1, col2 = st.columns([3, 1])
        with col1:
            new_skill = st.text_input("Add a skill", key="skill_input", placeholder="Python, React, SQL...")
        with col2:
            if st.button("➕ Add", use_container_width=True) and new_skill.strip():
                s = new_skill.strip().lower()
                if s not in st.session_state.skills:
                    st.session_state.skills.append(s)
                st.rerun()

        if st.session_state.skills:
            st.markdown("**Your skills:**")
            cols = st.columns(5)
            for i, sk in enumerate(st.session_state.skills):
                with cols[i % 5]:
                    if st.button(f"✕ {sk.title()}", key=f"rm_{sk}"):
                        st.session_state.skills.remove(sk)
                        st.rerun()
        else:
            st.caption("No skills added yet.")

        st.markdown("#### Projects")
        projects = st.text_area("Projects (one per line)", key="f_projects",
            placeholder="ResumeForge — AI resume builder\nTaskBot — Slack automation", height=100)

    if st.button("💾 Save Information", type="primary", use_container_width=True):
        st.session_state.resume_built = True
        st.success("✅ Information saved! Go to Document Generator to create your documents.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB SCRAPER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Job Scraper":
    st.markdown("## 🔍 Job Scraper + Skill Matching")

    col_cfg, col_gap = st.columns([1, 1], gap="large")

    with col_cfg:
        st.markdown("#### Scraper Config")
        role = st.text_input("Job role to search", value="Python Developer")
        source = st.selectbox("Source", ["RemoteOK (live)", "Indeed (simulated)"])
        if st.button("🔍 Scrape Jobs", type="primary", use_container_width=True):
            with st.spinner("Scraping jobs…"):
                jobs = get_jobs(role, source, st.session_state.skills)
                st.session_state.jobs = jobs
            st.success(f"Found {len(jobs)} listings!")

    with col_gap:
        st.markdown("#### Skill Gap Analysis")
        if not st.session_state.skills:
            st.info("Add skills in the Document Builder.")
        else:
            for sk in st.session_state.skills[:5]:
                st.markdown(f"✅ {sk.title()}")

    st.markdown("---")
    st.markdown("#### Job Listings")

    if not st.session_state.jobs:
        st.info("Click **Scrape Jobs** above to load listings.")
    else:
        for j in st.session_state.jobs[:5]:
            st.markdown(f"""
            **{j['emoji']} {j['title']}**  
            {j['company']} · {j['loc']} · {j['type']}  
            Match: **{j['match']}%**
            ---
            """)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DOCUMENT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Document Generator":
    st.markdown("## 📄 Document Generator")
    
    doc_type = st.radio(
        "Select Document Type",
        ["📄 Resume", "📋 CV", "✉️ Cover Letter", "📊 Proposal", "🏆 Experience Letter"],
        horizontal=True,
    )
    
    st.markdown("---")
    
    # Additional fields based on document type
    if doc_type == "✉️ Cover Letter":
        st.markdown("#### Cover Letter Details")
        col1, col2 = st.columns(2)
        with col1:
            cover_company = st.text_input("Company Name *", key="cover_company", placeholder="Google")
        with col2:
            cover_position = st.text_input("Position *", key="cover_position", placeholder="Senior Software Engineer")
        cover_custom = st.text_area("Additional Information", key="cover_custom", 
            placeholder="Why you're interested in this role, specific achievements...", height=100)
    
    elif doc_type == "📊 Proposal":
        st.markdown("#### Proposal Details")
        proposal_title = st.text_input("Proposal Title *", key="prop_title", placeholder="AI-Powered Customer Support System")
        proposal_client = st.text_input("Client/Organization *", key="prop_client", placeholder="ABC Corporation")
        col1, col2 = st.columns(2)
        with col1:
            proposal_budget = st.text_input("Budget", key="prop_budget", placeholder="$50,000")
        with col2:
            proposal_timeline = st.text_input("Timeline", key="prop_timeline", placeholder="3 months")
        proposal_summary = st.text_area("Executive Summary *", key="prop_summary", 
            placeholder="This proposal outlines the development and implementation...", height=80)
    
    elif doc_type == "🏆 Experience Letter":
        st.markdown("#### Experience Letter Details")
        col1, col2 = st.columns(2)
        with col1:
            exp_company = st.text_input("Company Name *", key="exp_company", placeholder="TechCorp Inc.")
            exp_employee = st.text_input("Employee Name *", key="exp_employee", placeholder="John Doe")
        with col2:
            exp_position = st.text_input("Position *", key="exp_position", placeholder="Senior Developer")
            exp_period = st.text_input("Employment Period *", key="exp_period", placeholder="Jan 2020 - Dec 2023")
        exp_remarks = st.text_area("Remarks *", key="exp_remarks", 
            placeholder="John was an exceptional employee who consistently exceeded expectations...", height=80)
    
    # ── Download section ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Download Document")
    
    # Collect data
    resume_data = {
        "name": st.session_state.get("f_name", ""),
        "title": st.session_state.get("f_title", ""),
        "email": st.session_state.get("f_email", ""),
        "phone": st.session_state.get("f_phone", ""),
        "location": st.session_state.get("f_loc", ""),
        "linkedin": st.session_state.get("f_linkedin", ""),
        "skills": st.session_state.skills,
        "company": st.session_state.get("f_company", ""),
        "role": st.session_state.get("f_exp_role", ""),
        "duration": st.session_state.get("f_duration", ""),
        "exp_desc": st.session_state.get("f_exp_desc", ""),
        "degree": st.session_state.get("f_degree", ""),
        "institution": st.session_state.get("f_inst", ""),
        "year": st.session_state.get("f_year", ""),
        "projects": st.session_state.get("f_projects", ""),
        "theme": st.session_state.template,
    }
    
    # Add document-specific data
    if doc_type == "✉️ Cover Letter":
        resume_data.update({
            "cover_company": st.session_state.get("cover_company", ""),
            "cover_position": st.session_state.get("cover_position", ""),
            "cover_custom": st.session_state.get("cover_custom", ""),
        })
    elif doc_type == "📊 Proposal":
        resume_data.update({
            "proposal_title": st.session_state.get("prop_title", ""),
            "proposal_client": st.session_state.get("prop_client", ""),
            "proposal_budget": st.session_state.get("prop_budget", ""),
            "proposal_timeline": st.session_state.get("prop_timeline", ""),
            "proposal_summary": st.session_state.get("prop_summary", ""),
        })
    elif doc_type == "🏆 Experience Letter":
        resume_data.update({
            "exp_company": st.session_state.get("exp_company", ""),
            "exp_employee": st.session_state.get("exp_employee", ""),
            "exp_position": st.session_state.get("exp_position", ""),
            "exp_period": st.session_state.get("exp_period", ""),
            "exp_remarks": st.session_state.get("exp_remarks", ""),
        })
    
    if not resume_data.get("name"):
        st.warning("⚠️ Please fill in your name in the Document Builder first.")
    else:
        doc_funcs = {
            "📄 Resume": generate_resume_pdf,
            "📋 CV": generate_cv_pdf,
            "✉️ Cover Letter": generate_cover_letter_pdf,
            "📊 Proposal": generate_proposal_pdf,
            "🏆 Experience Letter": generate_experience_letter_pdf,
        }
        
        doc_func = doc_funcs.get(doc_type)
        if doc_func:
            try:
                pdf_bytes = doc_func(resume_data)
                doc_name = doc_type.split(" ")[-1].lower()
                fname = f"{resume_data['name'].replace(' ', '_')}_{doc_name}.pdf"
                
                st.download_button(
                    label=f"📥 Download {doc_type}",
                    data=pdf_bytes,
                    file_name=fname,
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.success(f"✅ {doc_type} ready for download!")
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
