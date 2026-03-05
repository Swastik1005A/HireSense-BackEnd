from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.candidate import Candidate
from app.models.education import Education

from app.ml.education_extractor import extract_education
from app.ml.skill_extractor import extract_skills_semantic
from app.ml.experience_extractor import extract_experience_years

import shutil
import os
import fitz
import docx


router = APIRouter()


# -----------------------------
# DB Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Resume Text Extractors
# -----------------------------
def extract_text_from_pdf(file_path: str):
    text = ""

    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()

    return text


def extract_text_from_docx(file_path: str):

    doc = docx.Document(file_path)

    return "\n".join([para.text for para in doc.paragraphs])


# -----------------------------
# Upload Resume Endpoint
# -----------------------------
@router.post("/upload-resume")
def upload_resume(
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    upload_dir = "uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -------- Extract Resume Text --------

    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)

    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    print("Resume text length:", len(resume_text))


    # -------- ML Extraction --------

    education_data = extract_education(resume_text)

    skills = extract_skills_semantic(resume_text)

    experience_data = extract_experience_years(resume_text)

    experience_years = experience_data["total_years"]


    # -------- Save Candidate --------

    candidate = Candidate(
        name=name,
        email=email,
        resume_text=resume_text,
        skills=skills,
        experience_years=experience_years
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)


    # -------- Save Education --------

    education = Education(
        candidate_id=candidate.id,
        degree=education_data["degree"],
        institution=education_data["institution"],
        graduation_year=education_data["graduation_year"]
    )

    db.add(education)
    db.commit()


    # -------- Return Frontend Friendly Response --------

    return {

        "candidate_id": candidate.id,

        "skills": skills,

        "education": [
            {
                "degree": education_data["degree"],
                "school": education_data["institution"],
                "year": education_data["graduation_year"]
            }
        ],

        "experience": [
            {
                "title": "Professional Experience",
                "company": "Various",
                "duration": f"{experience_years} years"
            }
        ]

    }


# -----------------------------
# Candidate Profile
# -----------------------------
@router.get("/candidate/{candidate_id}")
def get_candidate_profile(candidate_id: int, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    education = db.query(Education).filter(Education.candidate_id == candidate.id).first()

    return {

        "candidate_id": candidate.id,

        "name": candidate.name,

        "email": candidate.email,

        "experience_years": candidate.experience_years,

        "skills": candidate.skills,

        "education": {
            "degree": education.degree if education else None,
            "institution": education.institution if education else None,
            "graduation_year": education.graduation_year if education else None
        }

    }


# -----------------------------
# Resume Analysis Endpoint
# -----------------------------
@router.get("/resume-analysis/{candidate_id}")
def resume_analysis(candidate_id: int, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    resume_text = candidate.resume_text

    skills = extract_skills_semantic(resume_text)

    experience_data = extract_experience_years(resume_text)

    experience_years = experience_data["total_years"]

    resume_score = min(len(skills) * 3 + experience_years * 10, 100)

    strengths = []
    weaknesses = []
    recommended_learning = []


    if len(skills) >= 15:
        strengths.append("Strong technical skillset")

    if "Machine Learning" in skills:
        strengths.append("Machine Learning knowledge")

    if experience_years == 0:
        weaknesses.append("No professional experience detected")

    if "AWS" not in skills:
        recommended_learning.append("AWS")

    if "Docker" not in skills:
        recommended_learning.append("Docker")


    return {

        "candidate_id": candidate_id,

        "resume_score": resume_score,

        "total_skills": len(skills),

        "experience_years": experience_years,

        "skills": skills,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommended_learning": recommended_learning

    }