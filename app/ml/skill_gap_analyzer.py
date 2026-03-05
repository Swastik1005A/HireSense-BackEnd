from typing import List


def analyze_skill_gap(resume_skills: List[str], job_skills: List[str]):

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched_skills = list(resume_set & job_set)
    missing_skills = list(job_set - resume_set)

    match_percentage = 0
    if job_skills:
        match_percentage = len(matched_skills) / len(job_skills)

    recommendation = generate_recommendation(missing_skills)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": round(match_percentage, 2),
        "recommendation": recommendation
    }


def generate_recommendation(missing_skills: List[str]):

    if not missing_skills:
        return "Candidate already meets the technical skill requirements for this role."

    if len(missing_skills) == 1:
        return f"Candidate could improve their profile by learning {missing_skills[0]}."

    if len(missing_skills) <= 3:
        skills = ", ".join(missing_skills)
        return f"Candidate could improve their match for this role by developing skills in {skills}."

    skills = ", ".join(missing_skills[:3])
    return f"Candidate is missing several key skills including {skills}. Improving these areas could significantly increase the job match score."