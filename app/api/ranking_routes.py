from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.candidate import Candidate
from app.models.job_description import JobDescription
from app.models.score import Score
from app.services.ranking_service import rank_candidate_service
from app.schemas.ranking_schema import RankResponse
from app.ml.skill_gap_analyzer import analyze_skill_gap

router = APIRouter()


# -----------------------------
# Rank Single Candidate
# -----------------------------
@router.post("/rank", response_model=RankResponse)
def rank_candidate(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()

    if not candidate or not job:
        raise HTTPException(status_code=404, detail="Invalid candidate or job ID")

    return rank_candidate_service(db, candidate, job)


# -----------------------------
# Rank All Candidates
# -----------------------------
@router.post("/rank-all/{job_id}")
def rank_all_candidates(job_id: int, db: Session = Depends(get_db)):

    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    candidates = db.query(Candidate).all()

    results = []

    for candidate in candidates:
        result = rank_candidate_service(db, candidate, job)
        results.append(result)

    results.sort(key=lambda x: x["final_score"], reverse=True)

    return {
        "job_id": job_id,
        "total_candidates": len(results),
        "results": results
    }


# -----------------------------
# Leaderboard (FIXED)
# -----------------------------
@router.get("/leaderboard/{job_id}")
def get_leaderboard(job_id: int, db: Session = Depends(get_db)):

    rows = (
        db.query(
            Candidate.id,
            Candidate.name,
            Candidate.email,
            func.max(Score.final_score).label("final_score"),
            func.max(Score.semantic_score).label("semantic_score"),
            func.max(Score.skill_score).label("skill_score"),
            func.max(Score.experience_score).label("experience_score"),
        )
        .join(Score, Candidate.id == Score.candidate_id)
        .filter(Score.job_id == job_id)
        .group_by(Candidate.id)
        .order_by(func.max(Score.final_score).desc())
        .all()
    )

    leaderboard = []

    for rank, row in enumerate(rows, start=1):

        leaderboard.append({
            "rank": rank,
            "candidate_id": row.id,
            "name": row.name,
            "email": row.email,
            "final_score": row.final_score,
            "semantic_score": row.semantic_score,
            "skill_score": row.skill_score,
            "experience_score": row.experience_score
        })

    return {
        "job_id": job_id,
        "total_candidates": len(leaderboard),
        "leaderboard": leaderboard
    }


# -----------------------------
# Ranking Explanation
# -----------------------------
@router.get("/ranking-explanation/{candidate_id}/{job_id}")
def ranking_explanation(candidate_id: int, job_id: int, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()

    if not candidate or not job:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")

    result = rank_candidate_service(db, candidate, job)

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "semantic_similarity": result["semantic_score"],
        "skill_match": result["skill_score"],
        "experience_score": result["experience_score"],
        "final_score": result["final_score"],
        "matched_skills": result.get("matched_skills", []),
        "missing_skills": result.get("missing_skills", []),
        "recommendation": result.get("recommendation", "")
    }


# -----------------------------
# Candidate Skill Gap
# -----------------------------
@router.get("/candidate-skill-gap/{candidate_id}/{job_id}")
def candidate_skill_gap(candidate_id: int, job_id: int, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()

    if not candidate or not job:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")

    from app.ml.skill_extractor import extract_skills_semantic

    resume_skills = extract_skills_semantic(candidate.resume_text)
    job_skills = extract_skills_semantic(job.description_text)

    gap_analysis = analyze_skill_gap(resume_skills, job_skills)

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "match_percentage": gap_analysis["match_percentage"],
        "matched_skills": gap_analysis["matched_skills"],
        "missing_skills": gap_analysis["missing_skills"],
        "recommendation": gap_analysis["recommendation"]
    }