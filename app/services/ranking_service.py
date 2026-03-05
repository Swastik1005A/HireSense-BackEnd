from app.ml.skill_extractor import extract_skills_semantic
from app.ml.model import embedding_model
from app.ml.scorer import skill_match_score
from app.models.score import Score
from app.ml.experience_extractor import extract_experience_years
from app.ml.bias_detector import detect_bias
from app.ml.skill_gap_analyzer import analyze_skill_gap



def rank_candidate_service(db, candidate, job):

    # ---------- 1️⃣ Semantic Similarity ----------
    semantic_score = embedding_model.similarity(
        candidate.resume_text,
        job.description_text
    )

    # ---------- 2️⃣ Skill Extraction ----------
    resume_skills = extract_skills_semantic(candidate.resume_text)
    job_skills = extract_skills_semantic(job.description_text)

    # ---------- 3️⃣ Skill Score ----------
    skill_score = skill_match_score(resume_skills, job_skills)

    # ---------- 4️⃣ Experience Extraction ----------
    experience_data = extract_experience_years(candidate.resume_text)

    experience_years = experience_data["total_years"]

    # Normalize experience to score (max useful experience = 5 yrs)
    experience_score = min(experience_years / 5, 1.0)

    # ---------- 5️⃣ Bias Detection ----------
    bias_report = detect_bias(candidate.resume_text)

    bias_flag = bias_report["bias_flag"]

    # ---------- Optional: Skill Gap Analysis ----------
    skill_gap_report = analyze_skill_gap(resume_skills, job_skills)

    missing_skills = skill_gap_report["missing_skills"]
    matched_skills = skill_gap_report["matched_skills"]
    skill_match_percentage = skill_gap_report["match_percentage"]
    recommendation = skill_gap_report["recommendation"]

    # ---------- 6️⃣ Final Score ----------
    final_score = (
        0.5 * semantic_score +
        0.3 * skill_score +
        0.2 * experience_score
    )

    # ---------- 7️⃣ Save Score ----------
    score_entry = Score(
        candidate_id=candidate.id,
        job_id=job.id,
        semantic_score=semantic_score,
        skill_score=skill_score,
        experience_score=experience_score,
        final_score=final_score,
        bias_flag=bias_flag
    )

    db.add(score_entry)
    db.commit()
    db.refresh(score_entry)

    # ---------- 8️⃣ Response ----------
    return {
        "candidate_id": candidate.id,
        "job_id": job.id,
        "semantic_score": semantic_score,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "final_score": final_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": skill_match_percentage,
        "recommendation": recommendation,
        "experience_years": experience_years
}