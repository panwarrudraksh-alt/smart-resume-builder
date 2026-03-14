import streamlit as st
import io
from pdf_generator import generate_resume_pdf
from job_scraper import get_jobs, match_skills

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeForge – Smart Resume Builder",
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

.metric-card {
    background: #f8fffe; border: 1px solid #9FE1CB;
    border-radius: 12px; padding: 1.2rem; text-align: center;
}
.metric-card .num { font-size: 2rem; font-weight: 600; color: #1D9E75; }
.metric-card .lbl { font-size: 0.8rem; color: #666; margin-top: 4px; }

.section-card {
    background: white; border: 1px solid #e8e8e8;
    border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
}

.job-card {
    background: white; border: 1px solid #e8e8e8;
    border-radius: 10px; padding: 1rem 1.2rem;
    margin-bottom: 0.8rem; transition: border-color 0.2s;
}
.job-card:hover { border-color: #1D9E75; }

.match-high { color: #1D9E75; font-weight: 600; }
.match-mid  { color: #EF9F27; font-weight: 600; }
.match-low  { color: #E24B4A; font-weight: 600; }

.skill-badge {
    display: inline-block; padding: 3px 10px;
    background: #E1F5EE; color: #085041;
    border-radius: 20px; font-size: 0.78rem;
    font-weight: 500; margin: 2px;
}
.skill-badge-missing {
    display: inline-block; padding: 3px 10px;
    background: #ffeaea; color: #A32D2D;
    border-radius: 20px; font-size: 0.78rem;
    font-weight: 500; margin: 2px;
}

.stDownloadButton > button {
    background: #1D9E75 !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important; font-size: 1rem !important;
    width: 100% !important;
}
.stDownloadButton > button:hover { background: #085041 !important; }

.template-preview {
    border: 2px solid #e0e0e0; border-radius: 10px;
    padding: 0; cursor: pointer; overflow: hidden;
    transition: border-color 0.2s;
}
.template-preview.selected { border-color: #1D9E75; }

div[data-testid="stSidebar"] { background: #f8fffe; }
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
        ["🏠 Home", "📝 Resume Builder", "🔍 Job Scraper", "⬇️ Export PDF"],
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
        <p>Build ATS-ready resumes · Match skills to live jobs · Export polished PDFs</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, title, desc, mod in [
        (c1, "📝", "Resume Builder", "Fill your details, see a live preview", "Module 1"),
        (c2, "🔍", "Job Scraper", "Pulls jobs using BeautifulSoup", "Module 2"),
        (c3, "⚡", "Skill Matching", "Match % vs job requirements", "Module 3"),
        (c4, "📄", "PDF Export", "3 themes · Real PDF download", "Module 4"),
    ]:
        with col:
            st.markdown(f"""
            <div class="section-card" style="text-align:center;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-weight:600;margin:8px 0 4px;">{title}</div>
                <div style="font-size:0.82rem;color:#666;">{desc}</div>
                <div style="margin-top:10px;display:inline-block;padding:2px 10px;
                    background:#E1F5EE;color:#085041;border-radius:4px;font-size:0.75rem;
                    font-weight:500;">{mod}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### How it works")
    steps = [
        ("1️⃣", "Fill your resume details in the **Resume Builder** tab"),
        ("2️⃣", "Choose a role and scrape live job listings"),
        ("3️⃣", "See your skill match score against each job"),
        ("4️⃣", "Pick a theme and **download your PDF** instantly"),
    ]
    for icon, text in steps:
        st.markdown(f"{icon} {text}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RESUME BUILDER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝 Resume Builder":
    st.markdown("## 📝 Resume Builder")
    st.markdown("Fill in your details. Everything is saved for PDF generation.")

    left, right = st.columns([1, 1], gap="large")

    with left:
        # ── Section 1: Personal Info ──────────────────────────────────────────
        with st.expander("① Personal Information", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                name    = st.text_input("Full Name *", key="f_name", placeholder="Jane Doe")
                email   = st.text_input("Email *",    key="f_email", placeholder="jane@email.com")
                phone   = st.text_input("Phone",      key="f_phone", placeholder="+91 9876543210")
            with col2:
                title   = st.text_input("Job Title",  key="f_title", placeholder="Software Engineer")
                loc     = st.text_input("Location",   key="f_loc",   placeholder="New Delhi, India")
                linkedin= st.text_input("LinkedIn",   key="f_linkedin", placeholder="linkedin.com/in/jane")

        # ── Section 2: Skills ─────────────────────────────────────────────────
        with st.expander("② Skills", expanded=True):
            new_skill = st.text_input("Add a skill (press Enter)", key="skill_input",
                                      placeholder="Python, React, SQL...")
            if st.button("➕ Add Skill") and new_skill.strip():
                s = new_skill.strip().lower()
                if s not in st.session_state.skills:
                    st.session_state.skills.append(s)
                st.rerun()

            if st.session_state.skills:
                st.markdown("**Your skills:**")
                cols = st.columns(4)
                for i, sk in enumerate(st.session_state.skills):
                    with cols[i % 4]:
                        if st.button(f"✕ {sk}", key=f"rm_{sk}"):
                            st.session_state.skills.remove(sk)
                            st.rerun()
            else:
                st.caption("No skills added yet.")

        # ── Section 3: Experience ─────────────────────────────────────────────
        with st.expander("③ Work Experience", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                company  = st.text_input("Company",  key="f_company",  placeholder="TechCorp")
                exp_role = st.text_input("Role",      key="f_exp_role", placeholder="Backend Developer")
            with col2:
                duration = st.text_input("Duration",  key="f_duration", placeholder="Jan 2022 – Present")
            exp_desc = st.text_area("Description", key="f_exp_desc",
                placeholder="• Built REST APIs serving 10k users/day\n• Reduced latency by 40%")

        # ── Section 4: Education ──────────────────────────────────────────────
        with st.expander("④ Education", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1: degree = st.text_input("Degree", key="f_degree", placeholder="B.Tech CS")
            with col2: inst   = st.text_input("Institution", key="f_inst", placeholder="IIT Delhi")
            with col3: year   = st.text_input("Year", key="f_year", placeholder="2018–2022")

        # ── Section 5: Projects ───────────────────────────────────────────────
        with st.expander("⑤ Projects", expanded=True):
            projects = st.text_area("Projects (one per line)", key="f_projects",
                placeholder="ResumeForge — AI resume builder with 92% ATS match rate\nTaskBot — Slack bot automating 200+ daily workflows")

        if st.button("✅ Save Resume", type="primary", use_container_width=True):
            st.session_state.resume_built = True
            st.success("Resume saved! Head to Export PDF to download.")

    with right:
        # ── Score ─────────────────────────────────────────────────────────────
        st.markdown("#### Resume Score")
        score = 0
        tips  = []
        if st.session_state.get("f_name"):  score += 15
        else: tips.append("Add your name")
        if st.session_state.get("f_email"): score += 10
        else: tips.append("Add email")
        if len(st.session_state.skills) >= 3: score += 20
        elif st.session_state.skills:         score += 10
        else: tips.append("Add 3+ skills")
        if st.session_state.get("f_exp_role") and st.session_state.get("f_company"): score += 20
        else: tips.append("Fill work experience")
        if st.session_state.get("f_exp_desc") and len(st.session_state.get("f_exp_desc","")) > 30: score += 15
        else: tips.append("Expand experience description")
        if st.session_state.get("f_degree"): score += 10
        else: tips.append("Add education")
        if st.session_state.get("f_projects"): score += 10
        score = min(score, 100)

        color = "#1D9E75" if score >= 70 else "#EF9F27" if score >= 40 else "#E24B4A"
        st.markdown(f"""
        <div style="text-align:center;padding:1.5rem;background:white;
            border:1px solid #e8e8e8;border-radius:12px;margin-bottom:1rem;">
            <div style="font-size:3rem;font-weight:700;color:{color};">{score}</div>
            <div style="font-size:0.85rem;color:#666;">out of 100</div>
            <div style="background:#f0f0f0;border-radius:8px;height:8px;margin:12px 0;">
                <div style="width:{score}%;height:100%;border-radius:8px;
                    background:{color};transition:width 0.8s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if tips:
            st.markdown("**To improve your score:**")
            for t in tips[:4]:
                st.markdown(f"• {t}")
        else:
            st.success("🎉 Excellent resume! Ready to export.")

        # ── Live Preview ──────────────────────────────────────────────────────
        st.markdown("#### Live Preview")
        accent = {"Classic Green": "#1D9E75", "Corporate Blue": "#185FA5",
                  "Creative Purple": "#533AB7"}.get(st.session_state.template, "#1D9E75")

        pname  = st.session_state.get("f_name", "Your Name") or "Your Name"
        ptitle = st.session_state.get("f_title", "Job Title") or "Job Title"
        pemail = st.session_state.get("f_email", "") or ""
        pphone = st.session_state.get("f_phone", "") or ""
        ploc   = st.session_state.get("f_loc", "") or ""
        prole  = st.session_state.get("f_exp_role", "Role") or "Role"
        pco    = st.session_state.get("f_company", "") or ""
        pdur   = st.session_state.get("f_duration", "") or ""
        pdesc  = st.session_state.get("f_exp_desc", "") or ""
        pdeg   = st.session_state.get("f_degree", "Degree") or "Degree"
        pinst  = st.session_state.get("f_inst", "") or ""
        pyear  = st.session_state.get("f_year", "") or ""
        pproj  = st.session_state.get("f_projects", "") or ""
        skills_html = "".join(f'<span class="skill-badge">{s}</span>'
                              for s in st.session_state.skills) or \
                      '<span style="color:#999;font-size:0.8rem;">Add skills above</span>'

        st.markdown(f"""
        <div style="border:1px solid #e0e0e0;border-radius:12px;overflow:hidden;font-size:0.82rem;">
            <div style="background:{accent};color:white;padding:18px 20px;">
                <div style="font-size:1.3rem;font-weight:600;">{pname}</div>
                <div style="opacity:.85;margin:3px 0;">{ptitle}</div>
                <div style="font-size:0.75rem;opacity:.8;margin-top:6px;">
                    {pemail} {"·" if pemail and pphone else ""} {pphone}
                    {"·" if (pemail or pphone) and ploc else ""} {ploc}
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1.5fr;gap:16px;padding:16px 20px;">
                <div>
                    <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;
                        letter-spacing:1px;color:{accent};border-bottom:1.5px solid #E1F5EE;
                        padding-bottom:4px;margin-bottom:8px;">Skills</div>
                    {skills_html}
                    <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;
                        letter-spacing:1px;color:{accent};border-bottom:1.5px solid #E1F5EE;
                        padding-bottom:4px;margin:12px 0 8px;">Education</div>
                    <div style="font-weight:600;">{pdeg}</div>
                    <div style="color:#666;">{pinst} {("· " + pyear) if pyear else ""}</div>
                </div>
                <div>
                    <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;
                        letter-spacing:1px;color:{accent};border-bottom:1.5px solid #E1F5EE;
                        padding-bottom:4px;margin-bottom:8px;">Experience</div>
                    <div style="font-weight:600;">{prole}</div>
                    <div style="color:#666;margin:2px 0 6px;">{pco} {("· " + pdur) if pdur else ""}</div>
                    <div style="white-space:pre-line;color:#444;">{pdesc[:200] + ("…" if len(pdesc)>200 else "")}</div>
                    {('<div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:' + accent + ';border-bottom:1.5px solid #E1F5EE;padding-bottom:4px;margin:12px 0 8px;">Projects</div><div style="white-space:pre-line;color:#444;">' + pproj[:150] + ("…" if len(pproj)>150 else "") + "</div>") if pproj else ""}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: JOB SCRAPER
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Job Scraper":
    st.markdown("## 🔍 Job Scraper + Skill Matching")

    col_cfg, col_gap = st.columns([1, 1], gap="large")

    with col_cfg:
        st.markdown("#### Scraper Config")
        role   = st.text_input("Job role to search", value="Python Developer",
                                placeholder="Python Developer, Data Scientist…")
        source = st.selectbox("Source", ["RemoteOK (live)", "Indeed (simulated)",
                                          "LinkedIn (simulated)"])
        if st.button("🔍 Scrape Jobs", type="primary", use_container_width=True):
            with st.spinner("Scraping jobs…"):
                jobs = get_jobs(role, source, st.session_state.skills)
                st.session_state.jobs = jobs
            st.success(f"Found {len(jobs)} listings!")

    with col_gap:
        st.markdown("#### Skill Gap Analysis")
        top_skills = ["python", "sql", "react", "docker", "machine learning",
                      "aws", "javascript", "git"]
        if not st.session_state.skills:
            st.info("Add skills in the Resume Builder to see your gap analysis.")
        else:
            for js in top_skills:
                has     = js in st.session_state.skills
                partial = not has and any(js in s or s in js
                                          for s in st.session_state.skills)
                pct   = 100 if has else 40 if partial else 0
                color = "#1D9E75" if has else "#EF9F27" if partial else "#E24B4A"
                label = "✓ Have it" if has else "~ Partial" if partial else "✕ Missing"
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                    <div style="min-width:120px;font-size:0.85rem;">{js}</div>
                    <div style="flex:1;background:#f0f0f0;border-radius:4px;height:6px;">
                        <div style="width:{pct}%;height:100%;border-radius:4px;
                            background:{color};"></div>
                    </div>
                    <div style="min-width:70px;font-size:0.78rem;font-weight:500;
                        color:{color};">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Job Listings")

    if not st.session_state.jobs:
        st.info("Click **Scrape Jobs** above to load listings.")
    else:
        fil = st.radio("Filter", ["All", "High match (70%+)", "Remote", "Full-time"],
                       horizontal=True)
        jobs = st.session_state.jobs
        if fil == "High match (70%+)": jobs = [j for j in jobs if j["match"] >= 70]
        if fil == "Remote":            jobs = [j for j in jobs if j["loc"] == "Remote"]
        if fil == "Full-time":         jobs = [j for j in jobs if j["type"] == "Full-time"]

        for j in jobs:
            mc = "match-high" if j["match"]>=70 else "match-mid" if j["match"]>=40 else "match-low"
            matched   = [s for s in st.session_state.skills if s in j["skills"]]
            unmatched = [s for s in j["skills"]  if s not in st.session_state.skills]
            badges = "".join(f'<span class="skill-badge">{s}</span>' for s in matched)
            miss   = "".join(f'<span class="skill-badge-missing">{s}</span>' for s in unmatched)
            st.markdown(f"""
            <div class="job-card">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div style="font-weight:600;font-size:1rem;">{j['emoji']} {j['title']}</div>
                        <div style="color:#666;font-size:0.85rem;margin:3px 0 8px;">
                            {j['company']} · {j['loc']} · {j['type']}
                        </div>
                        {badges}{miss}
                    </div>
                    <div style="text-align:right;min-width:60px;">
                        <div class="{mc}" style="font-size:1.4rem;">{j['match']}%</div>
                        <div style="font-size:0.7rem;color:#999;">match</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPORT PDF
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⬇️ Export PDF":
    st.markdown("## ⬇️ Export Resume as PDF")

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("#### Choose a Theme")
        themes = {
            "Classic Green":   {"color": "#1D9E75", "preview": "#E1F5EE"},
            "Corporate Blue":  {"color": "#185FA5", "preview": "#E6F1FB"},
            "Creative Purple": {"color": "#533AB7", "preview": "#EEEDFE"},
        }
        chosen = st.radio(
            "Theme",
            list(themes.keys()),
            index=list(themes.keys()).index(st.session_state.template),
            label_visibility="collapsed",
        )
        st.session_state.template = chosen

        # Visual theme swatches
        tcols = st.columns(3)
        for i, (tname, tval) in enumerate(themes.items()):
            with tcols[i]:
                border = "3px solid #333" if tname == chosen else "2px solid #ddd"
                st.markdown(f"""
                <div style="border:{border};border-radius:10px;overflow:hidden;
                    cursor:pointer;height:90px;">
                    <div style="background:{tval['color']};height:35px;"></div>
                    <div style="padding:6px;background:white;">
                        <div style="background:{tval['preview']};height:6px;
                            border-radius:3px;margin-bottom:4px;"></div>
                        <div style="background:#eee;height:4px;border-radius:3px;
                            width:80%;margin-bottom:3px;"></div>
                        <div style="background:#eee;height:4px;border-radius:3px;
                            width:60%;"></div>
                    </div>
                </div>
                <div style="text-align:center;font-size:0.75rem;margin-top:5px;
                    color:{'#1D9E75' if tname==chosen else '#666'};font-weight:
                    {'600' if tname==chosen else '400'};">{tname}</div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Pre-flight Checklist")
        checks = [
            (bool(st.session_state.get("f_name")),   "Name added"),
            (bool(st.session_state.get("f_email")),  "Email added"),
            (len(st.session_state.skills) >= 3,      "3+ skills listed"),
            (bool(st.session_state.get("f_exp_role")),"Work experience filled"),
            (bool(st.session_state.get("f_degree")), "Education added"),
            (bool(st.session_state.get("f_projects")),"Projects included"),
        ]
        for ok, label in checks:
            icon  = "✅" if ok else "⬜"
            color = "#1D9E75" if ok else "#999"
            st.markdown(
                f'<div style="color:{color};margin:4px 0;">{icon} {label}</div>',
                unsafe_allow_html=True)

    with right:
        st.markdown("#### Download Your Resume")

        # Collect all form values
        resume_data = {
            "name":       st.session_state.get("f_name", ""),
            "title":      st.session_state.get("f_title", ""),
            "email":      st.session_state.get("f_email", ""),
            "phone":      st.session_state.get("f_phone", ""),
            "location":   st.session_state.get("f_loc", ""),
            "linkedin":   st.session_state.get("f_linkedin", ""),
            "skills":     st.session_state.skills,
            "company":    st.session_state.get("f_company", ""),
            "role":       st.session_state.get("f_exp_role", ""),
            "duration":   st.session_state.get("f_duration", ""),
            "exp_desc":   st.session_state.get("f_exp_desc", ""),
            "degree":     st.session_state.get("f_degree", ""),
            "institution":st.session_state.get("f_inst", ""),
            "year":       st.session_state.get("f_year", ""),
            "projects":   st.session_state.get("f_projects", ""),
            "theme":      st.session_state.template,
        }

        fname = (resume_data["name"].replace(" ", "_") or "Resume") + "_Resume.pdf"

        if not resume_data["name"]:
            st.warning("⚠️ Please fill in your name in the Resume Builder first.")
        else:
            pdf_bytes = generate_resume_pdf(resume_data)
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name=fname,
                mime="application/pdf",
                use_container_width=True,
            )
            st.success(f"Your **{st.session_state.template}** resume is ready!")
            st.markdown(f"""
            <div style="background:#f8fffe;border:1px solid #9FE1CB;border-radius:10px;
                padding:1rem;margin-top:1rem;font-size:0.85rem;">
                <strong>📄 {fname}</strong><br>
                <span style="color:#666;">Theme: {st.session_state.template} ·
                Skills: {len(st.session_state.skills)} ·
                Generated with ReportLab</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### Tech Stack")
        st.code("""# PDF generated server-side with ReportLab
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4

# Theme colors map to accent colors:
# Classic Green  → #1D9E75
# Corporate Blue → #185FA5
# Creative Purple→ #533AB7
""", language="python")
