def skill_match_score(resume_skills, job_skills):
    if not job_skills:
        return 0.0

    matched = set(resume_skills) & set(job_skills)

    return len(matched) / len(job_skills)