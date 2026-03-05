from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models.candidate import Candidate
from app.models.score import Score
from app.models.job_description import JobDescription

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def dashboard_stats(db: Session = Depends(get_db)):

    candidates = db.query(Candidate).all()
    scores = db.query(Score).all()
    jobs = db.query(JobDescription).all()

    total_candidates = len(candidates)
    total_jobs = len(jobs)
    total_rankings = len(scores)

    avg_score = (
        sum([s.final_score for s in scores]) / len(scores)
        if scores else 0
    )

    # Score distribution
    distribution = {
        "90-100": 0,
        "80-89": 0,
        "70-79": 0,
        "60-69": 0,
        "50-59": 0,
        "<50": 0
    }

    for s in scores:

        score = (s.final_score or 0) * 100

        if score >= 90:
            distribution["90-100"] += 1
        elif score >= 80:
            distribution["80-89"] += 1
        elif score >= 70:
            distribution["70-79"] += 1
        elif score >= 60:
            distribution["60-69"] += 1
        elif score >= 50:
            distribution["50-59"] += 1
        else:
            distribution["<50"] += 1

    score_distribution = [
        {"range": k, "count": v}
        for k, v in distribution.items()
    ]

    # Top skills
    skill_count = {}

    for c in candidates:

        if not c.skills:
            continue

        for skill in c.skills:
            skill_count[skill] = skill_count.get(skill, 0) + 1

    top_skills = sorted(
        skill_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    top_skills_chart = [
        {"skill": skill, "count": count}
        for skill, count in top_skills
    ]

    return {
        "totalCandidates": total_candidates,
        "totalJobs": total_jobs,
        "totalRankings": total_rankings,
        "averageScore": round(avg_score * 100, 2),
        "scoreDistribution": score_distribution,
        "topSkills": top_skills_chart
    }