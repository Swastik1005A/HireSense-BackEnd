from pydantic import BaseModel
from typing import List


class RankResponse(BaseModel):
    candidate_id: int
    job_id: int
    semantic_score: float
    skill_score: float
    experience_score: float
    final_score: float
    resume_skills: List[str]
    job_skills: List[str]


class ExperienceDetails(BaseModel):
    total_years: float
    raw_matches: List[str]
    confidence: float