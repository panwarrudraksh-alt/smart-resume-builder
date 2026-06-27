"""
job_scraper.py - Scrapes jobs from RemoteOK
"""

import random

# Try to import scraping libs
try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False

# Simulated jobs
SIMULATED_JOBS = [
    {"title": "Python Backend Engineer", "company": "Razorpay", "emoji": "💳",
     "skills": ["python", "sql", "flask", "rest api"], "loc": "Bangalore", "type": "Full-time"},
    {"title": "Data Engineer", "company": "Flipkart", "emoji": "🛒",
     "skills": ["python", "sql", "spark", "airflow"], "loc": "Remote", "type": "Full-time"},
    {"title": "ML Engineer", "company": "Swiggy", "emoji": "🍕",
     "skills": ["python", "machine learning", "tensorflow", "docker"], "loc": "Hyderabad", "type": "Full-time"},
    {"title": "Frontend Developer", "company": "Zepto", "emoji": "⚡",
     "skills": ["react", "javascript", "html", "css"], "loc": "Mumbai", "type": "Contract"},
    {"title": "Full-Stack Developer", "company": "CRED", "emoji": "💳",
     "skills": ["python", "react", "sql", "docker"], "loc": "Remote", "type": "Full-time"},
    {"title": "DevOps Engineer", "company": "Groww", "emoji": "📈",
     "skills": ["docker", "kubernetes", "aws", "python"], "loc": "Pune", "type": "Full-time"},
    {"title": "Data Scientist", "company": "Meesho", "emoji": "🛍️",
     "skills": ["python", "machine learning", "sql", "statistics"], "loc": "Remote", "type": "Full-time"},
    {"title": "Cloud Engineer", "company": "PhonePe", "emoji": "📱",
     "skills": ["aws", "docker", "kubernetes", "python"], "loc": "Bangalore", "type": "Full-time"},
]

def scrape_remoteok(role):
    """Live scrape from RemoteOK."""
    try:
        url = "https://remoteok.com/api"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ResumeForge/1.0)"}
        resp = requests.get(url, headers=headers, timeout=8)
        data = resp.json()
        
        jobs = []
        role_lower = role.lower()
        for item in data[1:8]:  # Get first 7 jobs
            title = item.get("position", "")
            if not title or role_lower not in title.lower():
                continue
            tags = [t.lower() for t in item.get("tags", [])]
            jobs.append({
                "title": title,
                "company": item.get("company", "Unknown"),
                "emoji": "💼",
                "skills": tags[:5] if tags else ["remote"],
                "loc": "Remote",
                "type": "Full-time",
            })
        return jobs if jobs else None
    except Exception:
        return None

def match_skills(user_skills, job_skills):
    """Return match percentage."""
    if not user_skills or not job_skills:
        return random.randint(25, 55)
    matched = sum(1 for s in user_skills if s in job_skills)
    return round((matched / len(job_skills)) * 100) if job_skills else 0

def get_jobs(role, source, user_skills):
    """Main entry point."""
    jobs_raw = None
    
    if source == "RemoteOK (live)" and SCRAPING_AVAILABLE:
        jobs_raw = scrape_remoteok(role)
    
    if not jobs_raw:
        role_lower = role.lower()
        relevant = [j for j in SIMULATED_JOBS 
                    if any(w in j["title"].lower() for w in role_lower.split())]
        jobs_raw = relevant if relevant else SIMULATED_JOBS[:]
        random.shuffle(jobs_raw)
        jobs_raw = jobs_raw[:8]
    
    result = []
    for j in jobs_raw:
        job = dict(j)
        job["match"] = match_skills(user_skills, job.get("skills", []))
        result.append(job)
    
    result.sort(key=lambda x: x["match"], reverse=True)
    return result
