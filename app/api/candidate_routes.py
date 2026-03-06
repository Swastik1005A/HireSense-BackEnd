from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.candidate import Candidate
from app.models.score import Score

router = APIRouter()


@router.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):

    rows = (
        db.query(
            Candidate.id,
            Candidate.name,
            Candidate.email,
            Candidate.experience_years,
            Candidate.skills,
            func.max(Score.final_score).label("score")
        )
        .outerjoin(Score, Candidate.id == Score.candidate_id)
        .group_by(Candidate.id)
        .all()
    )

    results = []

    for row in rows:

        results.append({
            "candidate_id": row.id,
            "name": row.name,
            "email": row.email,
            "experience": row.experience_years,
            "skills": row.skills[:5] if row.skills else [],
            "score": row.score if row.score else 0
        })

    return results