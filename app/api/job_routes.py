from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job_description import JobDescription

router = APIRouter()


# -----------------------------
# CREATE JOB
# -----------------------------
@router.post("/create-job")
def create_job(description_text: str, db: Session = Depends(get_db)):

    text = description_text.strip()

    # Extract title safely
    first_line = text.split("\n")[0].strip()

    if "Job Title:" in first_line:
        title = first_line.replace("Job Title:", "").strip()
    else:
        title = first_line

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

        first_line = text.split("\n")[0].strip()

        if "Job Title:" in first_line:
            title = first_line.replace("Job Title:", "").strip()
        else:
            title = first_line

        results.append({
            "job_id": job.id,
            "title": title,
            "description": text
        })

    return results