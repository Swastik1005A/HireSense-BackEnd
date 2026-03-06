from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.candidate import Candidate
from app.models.score import Score
from app.models.job_description import JobDescription

router = APIRouter()


@router.get("/dashboard")
def dashboard_stats(db: Session = Depends(get_db)):

    # -----------------------------
    # Basic counts (fast SQL queries)
    # -----------------------------

    total_candidates = db.query(func.count(Candidate.id)).scalar() or 0
    total_jobs = db.query(func.count(JobDescription.id)).scalar() or 0
    total_rankings = db.query(func.count(Score.id)).scalar() or 0

    # -----------------------------
    # Average score
    # -----------------------------

    avg_score = db.query(func.avg(Score.final_score)).scalar() or 0
    average_score = round(avg_score * 100, 2)

    # -----------------------------
    # Score distribution
    # -----------------------------

    scores = db.query(Score.final_score).all()

    distribution = {
        "90-100": 0,
        "80-89": 0,
        "70-79": 0,
        "60-69": 0,
        "50-59": 0,
        "<50": 0
    }

    for s in scores:

        score = (s[0] or 0) * 100

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

    # -----------------------------
    # Top skills
    # -----------------------------

    candidates = db.query(Candidate.skills).all()

    skill_count = {}

    for c in candidates:

        skills = c[0]

        if not skills:
            continue

        for skill in skills:
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

    # -----------------------------
    # Response
    # -----------------------------

    return {
        "totalCandidates": total_candidates,
        "totalJobs": total_jobs,
        "totalRankings": total_rankings,
        "averageScore": average_score,
        "scoreDistribution": score_distribution,
        "topSkills": top_skills_chart
    }