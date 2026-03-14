# 📄 ResumeForge — Smart Resume Builder

A full-stack resume builder with real PDF export, job scraping, and skill matching. Built with **Streamlit** + **ReportLab** + **BeautifulSoup**.

---

## 🚀 Live Demo

Deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) — **completely free**.

---

## 📁 Project Structure

```
smart_resume_builder/
├── app.py               ← Main Streamlit UI (4 pages)
├── pdf_generator.py     ← ReportLab PDF engine (3 themes)
├── job_scraper.py       ← BeautifulSoup scraper + skill matcher
├── requirements.txt     ← All dependencies
├── .streamlit/
│   └── config.toml      ← Streamlit theme config
└── README.md
```

---

## ✨ Features

| Feature | Module | Tech |
|---|---|---|
| Resume form (live preview) | Builder | Streamlit |
| Resume score (0–100) | Builder | Python |
| **Real PDF download** | Export | ReportLab |
| **3 color themes** | Export | ReportLab |
| Job scraping | Job Scraper | BeautifulSoup + Requests |
| Skill matching % | Job Scraper | Python |
| Skill gap analysis | Job Scraper | Python |

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/smart-resume-builder.git
cd smart-resume-builder

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## ☁️ Deploy to Streamlit Community Cloud

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit — ResumeForge"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smart-resume-builder.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo → branch `main` → main file `app.py`
5. Click **Deploy** — done in ~60 seconds!

Your app will be live at:
```
https://YOUR_USERNAME-smart-resume-builder-app-XXXXX.streamlit.app
```

---

## 🎨 Themes

| Theme | Accent Color | Use Case |
|---|---|---|
| Classic Green | `#1D9E75` | Tech / Startup roles |
| Corporate Blue | `#185FA5` | Finance / Consulting |
| Creative Purple | `#533AB7` | Design / Creative |

---

## 📦 Dependencies

```
streamlit>=1.32.0      ← UI framework
reportlab>=4.1.0       ← PDF generation
beautifulsoup4>=4.12.0 ← Job scraping
requests>=2.31.0       ← HTTP fetching
```

---

## 🛠️ How PDF Generation Works

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4

# Theme color is applied to the header bar and section headings
# User clicks "Download PDF" → generate_resume_pdf(data) → bytes
# Streamlit's st.download_button streams bytes to the browser
```

---

## 🔍 How Job Scraping Works

```python
import requests
from bs4 import BeautifulSoup

# RemoteOK provides a JSON API endpoint
url = "https://remoteok.com/api"
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
jobs = resp.json()
# Filter by role keyword, extract title, company, tags
```

---

## 🏆 Hackathon Bonuses Included

- ✅ Resume score 0–100
- ✅ Skill gap analysis
- ✅ 3 downloadable PDF themes
- ✅ Live job scraping (RemoteOK)
- ✅ Skill match % per job
- ✅ Filter by match / remote / full-time

---

## 📄 License

MIT — use freely for hackathons, portfolios, or personal projects.
