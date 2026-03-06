from sentence_transformers import util
from app.ml.skill_taxonomy import TECH_SKILLS
from app.ml.model import embedding_model
import re

# Reference to embedding model
model = getattr(embedding_model, "model", None)

# Lazy cached skill embeddings
skill_embeddings = None

SIMILARITY_THRESHOLD = 0.48


def _ensure_model():
    """
    Ensure embedding model is loaded.
    Prevents NoneType crashes.
    """
    global model

    if model is None:
        raise RuntimeError(
            "SentenceTransformer model not loaded. "
            "Check app/ml/model.py initialization."
        )


def _get_skill_embeddings():
    """
    Lazy-load skill embeddings once.
    """
    global skill_embeddings

    if skill_embeddings is None:
        skill_embeddings = model.encode(
            TECH_SKILLS,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

    return skill_embeddings


def extract_skills_semantic(text: str):
    """
    Extract skills from resume using semantic similarity.
    """

    _ensure_model()
    embeddings = _get_skill_embeddings()

    detected_skills = set()

    # Split resume text into chunks
    chunks = re.split(r"[,\n•\-:]", text)

    for chunk in chunks:
        chunk = chunk.strip().lower()

        if len(chunk) < 3:
            continue

        chunk_embedding = model.encode(
            chunk,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        similarities = util.cos_sim(chunk_embedding, embeddings)[0]

        for i, score in enumerate(similarities):
            if score.item() > SIMILARITY_THRESHOLD:
                detected_skills.add(TECH_SKILLS[i])

    return list(detected_skills)