def generate_candidate_intelligence(skills, experience_years):

    strengths = []
    weaknesses = []
    recommendations = []

    # Strengths
    if "Machine Learning" in skills or "Deep Learning" in skills:
        strengths.append("Strong foundation in machine learning")

    if "FastAPI" in skills:
        strengths.append("Backend API development experience")

    if "Data Analysis" in skills:
        strengths.append("Experience with data analysis and processing")

    if "Git" in skills:
        strengths.append("Familiar with version control workflows")

    # Weaknesses
    if experience_years == 0:
        weaknesses.append("No professional industry experience yet")

    if "Cloud" not in skills and "AWS" not in skills:
        weaknesses.append("Limited cloud deployment experience")

    # Recommended Learning
    if "Docker" not in skills:
        recommendations.append("Learn Docker for containerized deployments")

    if "AWS" not in skills:
        recommendations.append("Study AWS or cloud infrastructure")

    if "System Design" not in skills:
        recommendations.append("Develop system design fundamentals")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }