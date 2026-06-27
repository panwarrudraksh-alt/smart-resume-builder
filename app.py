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
    page_title="ResumeForge Pro – Smart Document Builder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 3rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
}

.main-header h1 {
    font-weight: 800;
    font-size: 2.8rem;
    margin: 0;
    color: white;
}
.main-header p {
    margin: 0.5rem 0 0;
    opacity: 0.9;
    font-size: 1.1rem;
    color: #e0e7ff;
}

.document-card {
    background: white;
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border: 2px solid transparent;
}
.document-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
    border-color: #667eea;
}
.document-card .icon {
    font-size: 3rem;
    margin-bottom: 0.75rem;
    display: block;
}
.document-card .title {
    font-weight: 700;
    font-size: 1.1rem;
    color: #1a1a2e;
}
.document-card .desc {
    font-size: 0.85rem;
    color: #6b7280;
}

.section-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.skill-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.2rem;
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
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">🚀</div>
        <div style="font-weight: 800; font-size: 1.3rem; color: white; margin-top: 0.5rem;">ResumeForge</div>
        <div style="color: #9ca3af; font-size: 0.8rem;">Pro Edition</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "📋 Navigation",
        ["🏠 Home", "📝 Builder", "📄 Resume", "📋 CV", "✉️ Cover Letter", "📊 Proposal", "🏆 Experience", "🔍 Job Scraper"],
        label_visibility="collapsed",
    )
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("📚 Skills", len(st.session_state.skills))
    col2.metric("💼 Jobs", len(st.session_state.jobs))
    st.markdown("---")
    st.caption("⚡ Built with Streamlit · ReportLab")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>✨ Create Professional Documents Instantly</h1>
        <p>One platform for all your professional document needs — Resumes, CVs, Cover Letters, Proposals & more</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    docs = [
        ("📄", "Resume", "ATS-optimized resume"),
        ("📋", "CV", "Comprehensive CV"),
        ("✉️", "Cover Letter", "Customizable cover letter"),
        ("📊", "Proposal", "Professional proposals"),
    ]
    
    for i, (icon, title, desc) in enumerate(docs):
        col = [col1, col2, col3, col4][i]
        with col:
            st.markdown(f"""
            <div class="document-card">
                <span class="icon">{icon}</span>
                <div class="title">{title}</div>
                <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-card" style="margin-top: 2rem;">
        <h3 style="color: #1a1a2e; font-weight: 700;">🚀 How It Works</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">1️⃣</div>
                <div style="font-weight: 600;">Fill Information</div>
                <div style="color: #6b7280; font-size: 0.9rem;">Enter your details once</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">2️⃣</div>
                <div style="font-weight: 600;">Choose Document</div>
                <div style="color: #6b7280; font-size: 0.9rem;">Select from 5 document types</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">3️⃣</div>
                <div style="font-weight: 600;">Customize</div>
                <div style="color: #6b7280; font-size: 0.9rem;">Add document-specific details</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">4️⃣</div>
                <div style="font-weight: 600;">Download PDF</div>
                <div style="color: #6b7280; font-size: 0.9rem;">Get professional PDF instantly</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: BUILDER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Builder":
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem 2rem;">
        <h1 style="font-size: 2rem;">📝 Document Builder</h1>
        <p>Fill your information once. All documents will use this data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Personal", "💼 Experience", "🎓 Education", "🛠️ Skills"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", key="f_name", placeholder="John Doe")
            email = st.text_input("Email *", key="f_email", placeholder="john@email.com")
            phone = st.text_input("Phone", key="f_phone", placeholder="+1 234 567 890")
        with col2:
            title = st.text_input("Professional Title", key="f_title", placeholder="Software Engineer")
            location = st.text_input("Location", key="f_loc", placeholder="San Francisco, CA")
            linkedin = st.text_input("LinkedIn URL", key="f_linkedin", placeholder="linkedin.com/in/john")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company", key="f_company", placeholder="Tech Corp")
            role = st.text_input("Role", key="f_exp_role", placeholder="Senior Developer")
        with col2:
            duration = st.text_input("Duration", key="f_duration", placeholder="Jan 2020 - Present")
        exp_desc = st.text_area("Job Description", key="f_exp_desc", 
            placeholder="• Built REST APIs serving 10k users/day\n• Led team of 5 developers",
            height=100)
    
    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            degree = st.text_input("Degree", key="f_degree", placeholder="B.Tech Computer Science")
        with col2:
            institution = st.text_input("Institution", key="f_inst", placeholder="Stanford University")
        with col3:
            year = st.text_input("Year", key="f_year", placeholder="2016 - 2020")
    
    with tab4:
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
            cols = st.columns(6)
            for i, sk in enumerate(st.session_state.skills):
                with cols[i % 6]:
                    if st.button(f"✕ {sk.title()}", key=f"rm_{sk}"):
                        st.session_state.skills.remove(sk)
                        st.rerun()
        else:
            st.info("No skills added yet.")
        
        projects = st.text_area("Projects", key="f_projects",
            placeholder="ResumeForge — AI resume builder\nTaskBot — Slack automation",
            height=80)
    
    if st.button("💾 Save Information", type="primary", use_container_width=True):
        st.session_state.resume_built = True
        st.success("✅ Information saved successfully!")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RESUME
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Resume":
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <h1 style="font-size: 2rem;">📄 Resume Generator</h1>
        <p>Create an ATS-optimized professional resume</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Resume Details")
        theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="resume_theme")
        summary = st.text_area("Professional Summary", key="resume_summary",
            placeholder="Experienced software engineer with 5+ years in full-stack development...",
            height=100)
    
    with col2:
        st.markdown("### 📊 Preview")
        st.markdown("---")
        st.markdown("**Resume Sections:**")
        st.markdown("✅ Personal Information")
        st.markdown("✅ Professional Summary")
        st.markdown("✅ Skills")
        st.markdown("✅ Work Experience")
        st.markdown("✅ Education")
        st.markdown("✅ Projects")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Generate Resume PDF", type="primary", use_container_width=True):
            data = {
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
                "summary": st.session_state.get("resume_summary", ""),
                "theme": st.session_state.get("resume_theme", "Classic Green"),
            }
            
            try:
                pdf_bytes = generate_resume_pdf(data)
                if pdf_bytes:
                    fname = f"{data['name'].replace(' ', '_')}_Resume.pdf"
                    st.download_button(
                        label="⬇️ Download Resume PDF",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        use_container_width=True,
                        key="resume_download"
                    )
                    st.success("✅ Resume generated successfully!")
                else:
                    st.error("Failed to generate PDF.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CV
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 CV":
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <h1 style="font-size: 2rem;">📋 CV Generator</h1>
        <p>Create a comprehensive curriculum vitae</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 CV Details")
        cv_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="cv_theme")
        publications = st.text_area("Publications", key="cv_publications",
            placeholder="• Smith, J. (2023). 'AI in Healthcare.' Journal of AI, 12(3), 45-67.",
            height=80)
    
    with col2:
        st.markdown("### 📊 CV Preview")
        st.markdown("---")
        st.markdown("**CV Sections:**")
        st.markdown("✅ Personal Information")
        st.markdown("✅ Professional Summary")
        st.markdown("✅ Skills")
        st.markdown("✅ Work Experience")
        st.markdown("✅ Education")
        st.markdown("✅ Publications")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Generate CV PDF", type="primary", use_container_width=True):
            data = {
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
                "summary": st.session_state.get("f_summary", ""),
                "publications": st.session_state.get("cv_publications", ""),
                "theme": st.session_state.get("cv_theme", "Classic Green"),
            }
            
            try:
                pdf_bytes = generate_cv_pdf(data)
                if pdf_bytes:
                    fname = f"{data['name'].replace(' ', '_')}_CV.pdf"
                    st.download_button(
                        label="⬇️ Download CV PDF",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        use_container_width=True,
                        key="cv_download"
                    )
                    st.success("✅ CV generated successfully!")
                else:
                    st.error("Failed to generate PDF.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: COVER LETTER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✉️ Cover Letter":
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <h1 style="font-size: 2rem;">✉️ Cover Letter Generator</h1>
        <p>Create personalized cover letters for job applications</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ✉️ Cover Letter Details")
        col_a, col_b = st.columns(2)
        with col_a:
            cover_company = st.text_input("Company Name *", key="cover_company", placeholder="Google")
            cover_position = st.text_input("Position *", key="cover_position", placeholder="Senior Software Engineer")
        with col_b:
            cover_recruiter = st.text_input("Recruiter Name", key="cover_recruiter", placeholder="Sarah Johnson")
        
        cover_custom = st.text_area("Additional Information", key="cover_custom",
            placeholder="Why you're interested in this role, specific achievements...",
            height=100)
        
        cover_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="cover_theme")
    
    with col2:
        st.markdown("### 📊 Letter Preview")
        st.markdown("---")
        if st.session_state.get("cover_company"):
            st.markdown(f"**To:** {st.session_state.get('cover_company')}")
            st.markdown(f"**Position:** {st.session_state.get('cover_position')}")
        else:
            st.info("Fill in the details to see preview")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Generate Cover Letter PDF", type="primary", use_container_width=True):
            data = {
                "name": st.session_state.get("f_name", ""),
                "title": st.session_state.get("f_title", ""),
                "email": st.session_state.get("f_email", ""),
                "phone": st.session_state.get("f_phone", ""),
                "location": st.session_state.get("f_loc", ""),
                "skills": st.session_state.skills,
                "company": st.session_state.get("f_company", ""),
                "role": st.session_state.get("f_exp_role", ""),
                "cover_company": st.session_state.get("cover_company", ""),
                "cover_position": st.session_state.get("cover_position", ""),
                "cover_recruiter": st.session_state.get("cover_recruiter", ""),
                "cover_custom": st.session_state.get("cover_custom", ""),
                "theme": st.session_state.get("cover_theme", "Classic Green"),
            }
            
            try:
                pdf_bytes = generate_cover_letter_pdf(data)
                if pdf_bytes:
                    fname = f"{data['name'].replace(' ', '_')}_Cover_Letter.pdf"
                    st.download_button(
                        label="⬇️ Download Cover Letter PDF",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        use_container_width=True,
                        key="cover_download"
                    )
                    st.success("✅ Cover Letter generated successfully!")
                else:
                    st.error("Failed to generate PDF.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PROPOSAL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Proposal":
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <h1 style="font-size: 2rem;">📊 Proposal Generator</h1>
        <p>Create professional project proposals</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Proposal Details")
        col_a, col_b = st.columns(2)
        with col_a:
            proposal_title = st.text_input("Proposal Title *", key="prop_title", placeholder="AI-Powered Customer Support")
            proposal_client = st.text_input("Client/Organization *", key="prop_client", placeholder="ABC Corporation")
        with col_b:
            proposal_budget = st.text_input("Budget", key="prop_budget", placeholder="$50,000 - $75,000")
            proposal_timeline = st.text_input("Timeline", key="prop_timeline", placeholder="3 months")
        
        proposal_summary = st.text_area("Executive Summary *", key="prop_summary",
            placeholder="This proposal outlines the development and implementation...",
            height=100)
        
        proposal_approach = st.text_area("Approach/Methodology *", key="prop_approach",
            placeholder="1. Requirement Analysis\n2. System Design\n3. Development Phase\n4. Testing & Deployment",
            height=80)
        
        proposal_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="prop_theme")
    
    with col2:
        st.markdown("### 📊 Proposal Preview")
        st.markdown("---")
        if st.session_state.get("prop_title"):
            st.markdown(f"**Title:** {st.session_state.get('prop_title')}")
            st.markdown(f"**Client:** {st.session_state.get('prop_client')}")
        else:
            st.info("Fill in the details to see preview")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Generate Proposal PDF", type="primary", use_container_width=True):
            data = {
                "name": st.session_state.get("f_name", ""),
                "email": st.session_state.get("f_email", ""),
                "phone": st.session_state.get("f_phone", ""),
                "location": st.session_state.get("f_loc", ""),
                "skills": st.session_state.skills,
                "proposal_title": st.session_state.get("prop_title", ""),
                "proposal_client": st.session_state.get("prop_client", ""),
                "proposal_budget": st.session_state.get("prop_budget", ""),
                "proposal_timeline": st.session_state.get("prop_timeline", ""),
                "proposal_summary": st.session_state.get("prop_summary", ""),
                "proposal_approach": st.session_state.get("prop_approach", ""),
                "theme": st.session_state.get("prop_theme", "Classic Green"),
            }
            
            try:
                pdf_bytes = generate_proposal_pdf(data)
                if pdf_bytes:
                    fname = f"{data['name'].replace(' ', '_')}_Proposal.pdf"
                    st.download_button(
                        label="⬇️ Download Proposal PDF",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        use_container_width=True,
                        key="prop_download"
                    )
                    st.success("✅ Proposal generated successfully!")
                else:
                    st.error("Failed to generate PDF.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPERIENCE LETTER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Experience":
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <h1 style="font-size: 2rem;">🏆 Experience Letter Generator</h1>
        <p>Create professional employment verification letters</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🏆 Experience Letter Details")
        col_a, col_b = st.columns(2)
        with col_a:
            exp_company = st.text_input("Company Name *", key="exp_company", placeholder="TechCorp Inc.")
            exp_employee = st.text_input("Employee Name *", key="exp_employee", placeholder="John Doe")
            exp_position = st.text_input("Position Held *", key="exp_position", placeholder="Senior Developer")
        with col_b:
            exp_period = st.text_input("Employment Period *", key="exp_period", placeholder="Jan 2020 - Dec 2023")
            exp_issuer = st.text_input("Issuer Name *", key="exp_issuer", placeholder="Jane Smith")
            exp_issuer_title = st.text_input("Issuer Title *", key="exp_issuer_title", placeholder="HR Manager")
        
        exp_remarks = st.text_area("Performance Remarks *", key="exp_remarks",
            placeholder="John was an exceptional employee who consistently exceeded expectations...",
            height=80)
        
        exp_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="exp_theme")
    
    with col2:
        st.markdown("### 🏆 Letter Preview")
        st.markdown("---")
        if st.session_state.get("exp_employee"):
            st.markdown(f"**Employee:** {st.session_state.get('exp_employee')}")
            st.markdown(f"**Position:** {st.session_state.get('exp_position')}")
            st.markdown(f"**Company:** {st.session_state.get('exp_company')}")
        else:
            st.info("Fill in the details to see preview")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Generate Experience Letter PDF", type="primary", use_container_width=True):
            data = {
                "exp_company": st.session_state.get("exp_company", ""),
                "exp_employee": st.session_state.get("exp_employee", ""),
                "exp_position": st.session_state.get("exp_position", ""),
                "exp_period": st.session_state.get("exp_period", ""),
                "exp_remarks": st.session_state.get("exp_remarks", ""),
                "exp_issuer": st.session_state.get("exp_issuer", ""),
                "exp_issuer_title": st.session_state.get("exp_issuer_title", ""),
                "theme": st.session_state.get("exp_theme", "Classic Green"),
            }
            
            try:
                pdf_bytes = generate_experience_letter_pdf(data)
                if pdf_bytes:
                    fname = f"{data['exp_employee'].replace(' ', '_')}_Experience_Letter.pdf"
                    st.download_button(
                        label="⬇️ Download Experience Letter PDF",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        use_container_width=True,
                        key="exp_download"
                    )
                    st.success("✅ Experience Letter generated successfully!")
                else:
                    st.error("Failed to generate PDF.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB SCRAPER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Job Scraper":
    st.markdown("""
    <div class="main-header" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <h1 style="font-size: 2rem;">🔍 Job Scraper</h1>
        <p>Find jobs and match your skills</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        role = st.text_input("Job Role", value="Python Developer")
        source = st.selectbox("Source", ["RemoteOK (live)", "Indeed (simulated)"])
        
        if st.button("🔍 Scrape Jobs", type="primary", use_container_width=True):
            with st.spinner("Scraping jobs..."):
                jobs = get_jobs(role, source, st.session_state.skills)
                st.session_state.jobs = jobs
            st.success(f"✅ Found {len(jobs)} jobs!")
    
    with col2:
        st.metric("Total Jobs Found", len(st.session_state.jobs))
        if st.session_state.jobs:
            avg_match = sum(j.get("match", 0) for j in st.session_state.jobs) / len(st.session_state.jobs)
            st.metric("Average Match", f"{avg_match:.1f}%")
    
    st.markdown("---")
    
    if st.session_state.jobs:
        st.markdown("### 💼 Job Listings")
        for j in st.session_state.jobs[:5]:
            with st.container():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{j['emoji']} {j['title']}**")
                    st.markdown(f"🏢 {j['company']} · 📍 {j['loc']} · {j['type']}")
                with col_b:
                    match_color = "#10b981" if j["match"] >= 70 else "#f59e0b" if j["match"] >= 40 else "#ef4444"
                    st.markdown(f"<h3 style='color:{match_color};'>{j['match']}%</h3>", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("No jobs found. Click 'Scrape Jobs' to search.")
