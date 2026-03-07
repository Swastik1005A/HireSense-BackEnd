from sentence_transformers import util
from app.ml.skill_taxonomy import TECH_SKILLS
from app.ml.model import embedding_model
import re

# Higher threshold to prevent false matches
SIMILARITY_THRESHOLD = 0.65

# cached embeddings
skill_embeddings = None


def get_skill_embeddings():
    """
    Compute skill embeddings once and cache them.
    """
    global skill_embeddings

    if skill_embeddings is None:
        skill_embeddings = embedding_model.encode(TECH_SKILLS)

    return skill_embeddings


def extract_skills_semantic(text: str):
    """
    Extract skills from resume using:
    1. Keyword matching
    2. Semantic similarity
    """

    detected_skills = set()

    text_lower = text.lower()

    # -----------------------------
    # 1️⃣ KEYWORD MATCH (FAST PASS)
    # -----------------------------
    for skill in TECH_SKILLS:
        if skill.lower() in text_lower:
            detected_skills.add(skill)

    # -----------------------------
    # 2️⃣ SEMANTIC MATCH
    # -----------------------------

    embeddings = get_skill_embeddings()

    # split resume into chunks
    chunks = re.split(r"[,\n•\-:|/]", text_lower)

    cleaned_chunks = []

    for chunk in chunks:

        chunk = chunk.strip()

        # ignore useless chunks
        if len(chunk) < 4:
            continue

        # ignore very long sentences
        if len(chunk) > 120:
            continue

        cleaned_chunks.append(chunk)

    if not cleaned_chunks:
        return sorted(list(detected_skills))

    # encode chunks
    chunk_embeddings = embedding_model.encode(cleaned_chunks)

    for chunk_embedding in chunk_embeddings:

        similarities = util.cos_sim(chunk_embedding, embeddings)[0]

        for i, score in enumerate(similarities):

            if score.item() >= SIMILARITY_THRESHOLD:

                skill = TECH_SKILLS[i]

                # avoid very short skill noise
                if len(skill) < 2:
                    continue

                detected_skills.add(skill)

    return sorted(list(detected_skills))