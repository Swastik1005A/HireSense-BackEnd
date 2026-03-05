from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job_description import JobDescription

router = APIRouter()

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
        "description_text": job.description_text
    }