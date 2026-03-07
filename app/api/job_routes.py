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

    # Order matters (more specific first)

    if "machine learning engineer" in t or "machine learning" in t:
        return "Machine Learning Engineer"

    if "data science intern" in t:
        return "Data Science Intern"

    if "data scientist" in t:
        return "Data Scientist"

    if "data analyst" in t:
        return "Data Analyst"

    if "backend developer" in t or "backend" in t:
        return "Backend Developer"

    if "frontend developer" in t or "frontend" in t:
        return "Frontend Developer"

    if "full stack" in t or "fullstack" in t:
        return "Full Stack Developer"

    if "ai engineer" in t or "artificial intelligence" in t:
        return "AI Engineer"

    if "software engineer" in t:
        return "Software Engineer"

    # fallback: first line
    first_line = text.split("\n")[0].strip()

    if len(first_line) > 60:
        return first_line[:60] + "..."

    return first_line


# -----------------------------
# CREATE JOB
# -----------------------------
@router.post("/create-job")
def create_job(description_text: str, db: Session = Depends(get_db)):

    text = description_text.strip()

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
        "description_text": text
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