from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.candidate import Candidate
from app.models.score import Score
from app.models.education import Education

from app.ml.candidate_intelligence import generate_candidate_intelligence

router = APIRouter()


# -----------------------------------------
# Get All Candidates
# -----------------------------------------
@router.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):

    rows = (
        db.query(
            Candidate.id,
            Candidate.name,
            Candidate.email,
            Candidate.experience_years,
            Candidate.skills,
            Education.degree,
            Education.institution,
            Education.graduation_year,
            func.max(Score.final_score).label("score")
        )
        .outerjoin(Score, Candidate.id == Score.candidate_id)
        .outerjoin(Education, Candidate.id == Education.candidate_id)
        .group_by(
            Candidate.id,
            Candidate.name,
            Candidate.email,
            Candidate.experience_years,
            Candidate.skills,
            Education.degree,
            Education.institution,
            Education.graduation_year
        )
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
            "education": {
                "degree": row.degree,
                "institution": row.institution,
                "year": row.graduation_year
            },
            "score": row.score if row.score else 0
        })

    return results


# -----------------------------------------
# Candidate Intelligence
# -----------------------------------------
@router.get("/candidate-intelligence/{candidate_id}")
def get_candidate_intelligence(candidate_id: int, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    intelligence = generate_candidate_intelligence(
        candidate.skills,
        candidate.experience_years
    )

    return intelligence