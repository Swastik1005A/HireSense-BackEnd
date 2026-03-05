from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.candidate import Candidate
from app.models.score import Score

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):

    candidates = db.query(Candidate).all()
    scores = db.query(Score).all()

    # --------------------------------
    # Summary Metrics
    # --------------------------------

    total_candidates = len(candidates)

    avg_score = (
        sum([s.final_score for s in scores]) / len(scores)
        if scores else 0
    )

    top_score = max([s.final_score for s in scores], default=0)

    # --------------------------------
    # Skill Distribution
    # --------------------------------

    skill_count = {}

    for c in candidates:

        if not c.skills:
            continue

        for skill in c.skills:

            skill_count[skill] = skill_count.get(skill, 0) + 1

    # take top 6 skills only
    top_skills = sorted(
        skill_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:6]

    skill_distribution = [
        {"name": skill, "value": count}
        for skill, count in top_skills
    ]

    # --------------------------------
    # Ranking Distribution
    # --------------------------------

    ranking_ranges = {
        "90-100": 0,
        "80-89": 0,
        "70-79": 0,
        "60-69": 0,
        "50-59": 0,
        "< 50": 0
    }

    for s in scores:

        score = (s.final_score or 0) * 100

        if score >= 90:
            ranking_ranges["90-100"] += 1
        elif score >= 80:
            ranking_ranges["80-89"] += 1
        elif score >= 70:
            ranking_ranges["70-79"] += 1
        elif score >= 60:
            ranking_ranges["60-69"] += 1
        elif score >= 50:
            ranking_ranges["50-59"] += 1
        else:
            ranking_ranges["< 50"] += 1

    ranking_distribution = [
        {"range": k, "count": v}
        for k, v in ranking_ranges.items()
    ]

    # --------------------------------
    # Avg Score Trend (mock for now)
    # --------------------------------

    avg_score_trend = [
        {"month": "Jan", "score": 65},
        {"month": "Feb", "score": 70},
        {"month": "Mar", "score": 72},
        {"month": "Apr", "score": 74},
        {"month": "May", "score": 76},
        {"month": "Jun", "score": 78}
    ]

    # --------------------------------
    # Final Response
    # --------------------------------

    return {
        "summary": {
            "totalCandidates": total_candidates,
            "averageScore": round(avg_score * 100, 2),
            "topScore": round(top_score * 100, 2)
        },
        "avgScoreOverTime": avg_score_trend,
        "skillDistribution": skill_distribution,
        "rankingDistribution": ranking_distribution
    }