from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job_description import JobDescription

router = APIRouter()


# -----------------------------
# JOB TITLE DETECTOR
# -----------------------------
def detect_job_title(text: str) -> str:

    t = text.lower()

    # Most specific roles first

    if "data science intern" in t:
        return "Data Science Intern"

    if "data scientist" in t:
        return "Data Scientist"

    if "data analyst" in t:
        return "Data Analyst"

    if "ai engineer" in t or "artificial intelligence engineer" in t:
        return "AI Engineer"

    if "machine learning engineer" in t:
        return "Machine Learning Engineer"

    if "machine learning" in t:
        return "Machine Learning Engineer"

    if "full stack" in t or "fullstack" in t:
        return "Full Stack Developer"

    if "backend" in t:
        return "Backend Developer"

    if "frontend" in t:
        return "Frontend Developer"

    if "software engineer" in t:
        return "Software Engineer"

    # fallback → first line
    first_line = text.split("\n")[0].strip()

    if len(first_line) > 60:
        return first_line[:60] + "..."

    return first_line


# -----------------------------
# CLEAN DESCRIPTION
# -----------------------------
def clean_description(text: str):

    text = text.strip()

    # Remove "Job Title:" line if user pasted it
    if text.lower().startswith("job title:"):
        lines = text.split("\n")

        if len(lines) > 1:
            text = "\n".join(lines[1:]).strip()

    return text


# -----------------------------
# CREATE JOB
# -----------------------------
@router.post("/create-job")
def create_job(description_text: str, db: Session = Depends(get_db)):

    text = clean_description(description_text)

    title = detect_job_title(text)

    job = JobDescription(
        description_text=text
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "title": title,
        "description": text
    }


# -----------------------------
# GET ALL JOBS
# -----------------------------
@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(JobDescription).all()

    results = []

    for job in jobs:

        text = (job.description_text or "").strip()

        if not text:
            continue

        title = detect_job_title(text)

        results.append({
            "job_id": job.id,
            "title": title,
            "description": text
        })

    return results