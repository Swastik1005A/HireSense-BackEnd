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

    job = JobDescription(
        description_text=description_text
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "title": description_text.split("\n")[0].replace("Job Title:", "").strip(),
        "description_text": job.description_text
    }


# -----------------------------
# GET ALL JOBS
# -----------------------------
@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(JobDescription).all()

    results = []

    for job in jobs:

        text = job.description_text.strip()

        # Extract title from first line
        title = text.split("\n")[0].replace("Job Title:", "").strip()

        results.append({
            "job_id": job.id,
            "title": title,
            "description": text
        })

    return results