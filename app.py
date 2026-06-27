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

/* Main background */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2.5rem 3rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.main-header h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    margin: 0;
    letter-spacing: -1px;
    background: linear-gradient(to right, #fff, #e0e7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.main-header p {
    margin: 0.5rem 0 0;
    opacity: 0.9;
    font-size: 1.1rem;
    color: #e0e7ff;
}

/* Document Cards */
.doc-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.document-card {
    background: white;
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    cursor: pointer;
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}
.document-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    transform: scaleX(0);
    transition: transform 0.3s;
}
.document-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
    border-color: #667eea;
}
.document-card:hover::before {
    transform: scaleX(1);
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
    margin-bottom: 0.25rem;
}
.document-card .desc {
    font-size: 0.85rem;
    color: #6b7280;
    line-height: 1.4;
}

/* Section Cards */
.section-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.05);
}

/* Sidebar */
.css-1d391kg {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
.css-1d391kg .stRadio > label {
    color: white !important;
}
.css-1d391kg .stMetric {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.5rem;
}

/* Buttons */
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

/* Inputs */
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 2px solid #e5e7eb !important;
    transition: all 0.3s;
}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    transition: all 0.3s;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(102, 126, 234, 0.05);
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

/* Skill badges */
.skill-badge {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.2rem;
    transition: all 0.3s;
}
.skill-badge:hover {
    transform: scale(1.05);
}

/* Document Preview */
.preview-container {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border: 2px solid #e5e7eb;
    min-height: 300px;
    transition: all 0.3s;
}
.preview-container:hover {
    border-color: #667eea;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1);
}

/* Download button */
.download-btn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s !important;
}
.download-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3) !important;
}

/* Status indicators */
.status-success {
    color: #10b981;
    font-weight: 600;
}
.status-warning {
    color: #f59e0b;
    font-weight: 600;
}
.status-error {
    color: #ef4444;
    font-weight: 600;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.fade-in {
    animation: fadeInUp 0.6s ease-out;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* Responsive */
@media (max-width: 768px) {
    .main-header h1 {
        font-size: 2rem;
    }
    .doc-grid {
        grid-template-columns: 1fr 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
defaults = {
    "skills": [],
    "jobs": [],
    "template": "Classic Green",
    "resume_built": False,
    "active_doc": "Resume",
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
    
    # Quick stats
    st.markdown("### 📊 Stats")
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
    <div class="main-header fade-in">
        <h1>✨ Create Professional Documents Instantly</h1>
        <p>One platform for all your professional document needs — Resumes, CVs, Cover Letters, Proposals & more</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Document grid
    col1, col2, col3, col4 = st.columns(4)
    
    docs = [
        ("📄", "Resume", "ATS-optimized resume", "Generate"),
        ("📋", "CV", "Comprehensive CV", "Generate"),
        ("✉️", "Cover Letter", "Customizable cover letter", "Generate"),
        ("📊", "Proposal", "Professional proposals", "Generate"),
        ("🏆", "Experience", "Employment verification", "Generate"),
    ]
    
    for i, (icon, title, desc, action) in enumerate(docs):
        col = [col1, col2, col3, col4][i % 4]
        with col:
            st.markdown(f"""
            <div class="document-card fade-in" style="animation-delay: {i * 0.1}s;">
                <span class="icon">{icon}</span>
                <div class="title">{title}</div>
                <div class="desc">{desc}</div>
                <div style="margin-top: 1rem;">
                    <span style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                 color: white; padding: 0.25rem 0.75rem; border-radius: 20px; 
                                 font-size: 0.75rem; font-weight: 600;">{action}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # How it works
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
# PAGE: BUILDER (Common Information)
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Builder":
    st.markdown("""
    <div class="main-header fade-in" style="padding: 1.5rem 2rem;">
        <h1 style="font-size: 2rem;">📝 Document Builder</h1>
        <p>Fill your information once. All documents will use this data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Personal", "💼 Experience", "🎓 Education", "🛠️ Skills", "📝 Additional"
    ])
    
    with tab1:
        st.markdown("### 👤 Personal Information")
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
        st.markdown("### 💼 Work Experience")
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company", key="f_company", placeholder="Tech Corp")
            role = st.text_input("Role", key="f_exp_role", placeholder="Senior Developer")
        with col2:
            duration = st.text_input("Duration", key="f_duration", placeholder="Jan 2020 - Present")
            employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract", "Internship"])
        exp_desc = st.text_area("Job Description", key="f_exp_desc", 
            placeholder="• Built REST APIs serving 10k users/day\n• Led team of 5 developers\n• Reduced latency by 40%",
            height=120)
    
    with tab3:
        st.markdown("### 🎓 Education")
        col1, col2, col3 = st.columns(3)
        with col1:
            degree = st.text_input("Degree", key="f_degree", placeholder="B.Tech Computer Science")
        with col2:
            institution = st.text_input("Institution", key="f_inst", placeholder="Stanford University")
        with col3:
            year = st.text_input("Year", key="f_year", placeholder="2016 - 2020")
        
        st.markdown("### 📜 Certifications")
        certs = st.text_area("Certifications", key="f_certs", 
            placeholder="• AWS Certified Solutions Architect\n• Google Professional Data Engineer",
            height=80)
    
    with tab4:
        st.markdown("### 🛠️ Skills")
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
            st.markdown("**Your Skills:**")
            cols = st.columns(6)
            for i, sk in enumerate(st.session_state.skills):
                with cols[i % 6]:
                    if st.button(f"✕ {sk.title()}", key=f"rm_{sk}"):
                        st.session_state.skills.remove(sk)
                        st.rerun()
        else:
            st.info("No skills added yet. Add your skills above.")
        
        st.markdown("### 📂 Projects")
        projects = st.text_area("Projects (one per line)", key="f_projects",
            placeholder="ResumeForge — AI resume builder with 92% ATS match rate\nTaskBot — Slack automation",
            height=100)
    
    with tab5:
        st.markdown("### 📝 Additional Information")
        summary = st.text_area("Professional Summary", key="f_summary",
            placeholder="Experienced software engineer with 5+ years in full-stack development...",
            height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            languages = st.text_input("Languages", key="f_languages", placeholder="English, Spanish, French")
        with col2:
            interests = st.text_input("Interests", key="f_interests", placeholder="AI, Open Source, Chess")
        
        references = st.text_area("References", key="f_refs",
            placeholder="John Smith, Senior Manager, Tech Corp, john@techcorp.com",
            height=60)
    
    # Save button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save All Information", type="primary", use_container_width=True):
            st.session_state.resume_built = True
            st.success("✅ All information saved successfully!")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RESUME
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Resume":
    st.markdown("""
    <div class="main-header fade-in" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <h1 style="font-size: 2rem;">📄 Resume Generator</h1>
        <p>Create an ATS-optimized professional resume</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Resume Details")
        
        # Theme selection
        st.markdown("#### 🎨 Theme")
        theme = st.selectbox("Select Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], 
                            key="resume_theme")
        
        # Additional resume-specific fields
        with st.expander("📌 Additional Details", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                resume_summary = st.text_area("Professional Summary", key="resume_summary",
                    placeholder="Experienced software engineer with 5+ years in full-stack development...",
                    height=100)
            with col_b:
                resume_achievements = st.text_area("Key Achievements", key="resume_achievements",
                    placeholder="• Increased revenue by 30%\n• Reduced costs by 25%",
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
        
        if st.button("🔄 Refresh Preview", use_container_width=True):
            st.rerun()
    
    # Generate Resume
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
                    st.error("Failed to generate PDF. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CV
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 CV":
    st.markdown("""
    <div class="main-header fade-in" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <h1 style="font-size: 2rem;">📋 CV Generator</h1>
        <p>Create a comprehensive curriculum vitae</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 CV Details")
        
        # Theme
        cv_theme = st.selectbox("🎨 Theme", ["Classic Green", "Corporate Blue", "Creative Purple"], key="cv_theme")
        
        with st.expander("📚 Additional CV Sections", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                publications = st.text_area("Publications", key="cv_publications",
                    placeholder="• Smith, J. (2023). 'AI in Healthcare.' Journal of AI, 12(3), 45-67.",
                    height=100)
                affiliations = st.text_input("Professional Affiliations", key="cv_affiliations",
                    placeholder="IEEE, ACM, PMI")
            with col_b:
                research = st.text_area("Research Experience", key="cv_research",
                    placeholder="• Led research on machine learning algorithms\n• Published 5 papers",
                    height=100)
                teaching = st.text_area("Teaching Experience", key="cv_teaching",
                    placeholder="• Teaching Assistant for CS101\n• Guest Lecturer for ML course",
                    height=100)
    
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
        st.markdown("✅ Research Experience")
        st.markdown("✅ Teaching Experience")
        st.markdown("✅ Professional Affiliations")
        st.markdown("---")
    
    # Generate CV
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
                "affiliations": st.session_state.get("cv_affiliations", ""),
                "research": st.session_state.get("cv_research", ""),
                "teaching": st.session_state.get("cv_teaching", ""),
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
                    st.error("Failed to generate PDF. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: COVER LETTER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✉️ Cover Letter":
    st.markdown("""
    <div class="main-header fade-in" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
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
            cover_recruiter = st.text_input("Recruiter/Hiring Manager Name", key="cover_recruiter", 
                                          placeholder="Sarah Johnson")
            cover_date = st.date_input("Date", key="cover_date")
        
        st.markdown("#### 📝 Letter Content")
        cover_opening = st.text_area("Opening Paragraph", key="cover_opening",
            placeholder="I am writing to express my strong interest in the Software Engineer position at Google...",
            height=80)
        
        cover_body = st.text_area("Body Paragraph (Skills & Experience)", key="cover_body",
            placeholder="In my current role as Senior Developer at Tech Corp, I have developed expertise in...",
            height=120)
        
        cover_closing = st.text_area("Closing Paragraph", key="cover_closing",
            placeholder="I would welcome the opportunity to discuss how my experience can contribute to Google's success...",
            height=80)
        
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
        st.markdown("**Letter Structure:**")
        st.markdown("✅ Header & Contact")
        st.markdown("✅ Date & Recipient")
        st.markdown("✅ Opening Paragraph")
        st.markdown("✅ Body Paragraph")
        st.markdown("✅ Closing Paragraph")
        st.markdown("✅ Signature")
    
    # Generate Cover Letter
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
                "cover_date": st.session_state.get("cover_date", datetime.now()),
                "cover_opening": st.session_state.get("cover_opening", ""),
                "cover_body": st.session_state.get("cover_body", ""),
                "cover_closing": st.session_state.get("cover_closing", ""),
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
                    st.error("Failed to generate PDF. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PROPOSAL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Proposal":
    st.markdown("""
    <div class="main-header fade-in" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <h1 style="font-size: 2rem;">📊 Proposal Generator</h1>
        <p>Create professional project proposals</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Proposal Details")
        
        col_a, col_b = st.columns(2)
        with col_a:
            proposal_title = st.text_input("Proposal Title *", key="prop_title", 
                                         placeholder="AI-Powered Customer Support System")
            proposal_client = st.text_input("Client/Organization *", key="prop_client", 
                                          placeholder="ABC Corporation")
        with col_b:
            proposal_budget = st.text_input("Budget", key="prop_budget", placeholder="$50,000 - $75,000")
            proposal_timeline = st.text_input("Timeline", key="prop_timeline", placeholder="3 months")
        
        st.markdown("#### 📝 Proposal Content")
        proposal_summary = st.text_area("Executive Summary *", key="prop_summary",
            placeholder="This proposal outlines the development and implementation of an AI-powered customer support system...",
            height=100)
        
        proposal_approach = st.text_area("Approach/Methodology *", key="prop_approach",
            placeholder="1. Requirement Analysis\n2. System Design\n3. Development Phase\n4. Testing & Deployment",
            height=100)
        
        proposal_benefits = st.text_area("Benefits/Value Proposition *", key="prop_benefits",
            placeholder="• 50% reduction in response time\n• 24/7 automated support\n• 30% increase in satisfaction",
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
        st.markdown("**Proposal Structure:**")
        st.markdown("✅ Title & Header")
        st.markdown("✅ Executive Summary")
        st.markdown("✅ Approach & Methodology")
        st.markdown("✅ Value Proposition")
        st.markdown("✅ Budget & Timeline")
        st.markdown("✅ About Us")
    
    # Generate Proposal
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
                "proposal_benefits": st.session_state.get("prop_benefits", ""),
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
                    st.error("Failed to generate PDF. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPERIENCE LETTER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏆 Experience":
    st.markdown("""
    <div class="main-header fade-in" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
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
            exp_reason = st.text_input("Reason for Leaving", key="exp_reason", placeholder="Career growth opportunity")
            exp_issuer = st.text_input("Issuer Name *", key="exp_issuer", placeholder="Jane Smith")
            exp_issuer_title = st.text_input("Issuer Title *", key="exp_issuer_title", placeholder="HR Manager")
        
        exp_remarks = st.text_area("Performance Remarks *", key="exp_remarks",
            placeholder="John was an exceptional employee who consistently exceeded expectations. He led a team of 5 developers and delivered projects on time with high quality.",
            height=100)
        
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
        st.markdown("**Letter Structure:**")
        st.markdown("✅ Company Letterhead")
        st.markdown("✅ Date & Reference")
        st.markdown("✅ Employee Details")
        st.markdown("✅ Employment Period")
        st.markdown("✅ Performance Remarks")
        st.markdown("✅ Issuer Information")
        st.markdown("✅ Signature")
    
    # Generate Experience Letter
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Generate Experience Letter PDF", type="primary", use_container_width=True):
            data = {
                "exp_company": st.session_state.get("exp_company", ""),
                "exp_employee": st.session_state.get("exp_employee", ""),
                "exp_position": st.session_state.get("exp_position", ""),
                "exp_period": st.session_state.get("exp_period", ""),
                "exp_reason": st.session_state.get("exp_reason", ""),
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
                    st.error("Failed to generate PDF. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB SCRAPER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Job Scraper":
    st.markdown("""
    <div class="main-header fade-in" style="padding: 1.5rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <h1 style="font-size: 2rem;">🔍 Job Scraper</h1>
        <p>Find jobs and match your skills</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔍 Search Jobs")
        role = st.text_input("Job Role", value="Python Developer", placeholder="Python Developer, Data Scientist...")
        source = st.selectbox("Source", ["RemoteOK (live)", "Indeed (simulated)", "LinkedIn (simulated)"])
        
        if st.button("🔍 Scrape Jobs", type="primary", use_container_width=True):
            with st.spinner("Scraping jobs..."):
                jobs = get_jobs(role, source, st.session_state.skills)
                st.session_state.jobs = jobs
            st.success(f"✅ Found {len(jobs)} jobs!")
    
    with col2:
        st.markdown("### 📊 Job Stats")
        st.metric("Total Jobs Found", len(st.session_state.jobs))
        if st.session_state.jobs:
            avg_match = sum(j.get("match", 0) for j in st.session_state.jobs) / len(st.session_state.jobs)
            st.metric("Average Match", f"{avg_match:.1f}%")
    
    st.markdown("---")
    
    # Job listings
    if st.session_state.jobs:
        st.markdown("### 💼 Job Listings")
        for j in st.session_state.jobs[:10]:
            with st.container():
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.markdown(f"**{j['emoji']} {j['title']}**")
                    st.markdown(f"🏢 {j['company']} · 📍 {j['loc']} · {j['type']}")
                with col_b:
                    match_color = "#10b981" if j["match"] >= 70 else "#f59e0b" if j["match"] >= 40 else "#ef4444"
                    st.markdown(f"<h3 style='color:{match_color};'>{j['match']}%</h3>", unsafe_allow_html=True)
                with col_c:
                    st.markdown("Match")
                st.markdown("---")
    else:
        st.info("No jobs found. Click 'Scrape Jobs' to search.")
