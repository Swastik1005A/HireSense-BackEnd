from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.candidate import Candidate
from app.models.score import Score
from app.ml.skill_extractor import extract_skills_semantic
from app.ml.experience_extractor import extract_experience_years

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):

    rows = (
        db.query(Candidate, Score)
        .outerjoin(Score, Candidate.id == Score.candidate_id)
        .all()
    )

    results = []

    for candidate, score in rows:

        results.append({
            "candidate_id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "experience": candidate.experience_years,
            "skills": candidate.skills[:5] if candidate.skills else [],
            "score": score.final_score if score else 0
        })

    return results