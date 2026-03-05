

from sentence_transformers import util
from app.ml.skill_taxonomy import TECH_SKILLS
from app.ml.model import embedding_model
import re
from sentence_transformers import util


# Use the already loaded model
model = embedding_model.model

# Precompute once
skill_embeddings = model.encode(
    TECH_SKILLS,
    convert_to_tensor=True,
    normalize_embeddings=True
)

SIMILARITY_THRESHOLD = 0.48

def extract_skills_semantic(text: str):

    detected_skills = set()

    # Split resume into smaller chunks
    chunks = re.split(r"[,\n•\-:]", text)

    for chunk in chunks:
        chunk = chunk.strip()

        if len(chunk) < 3:
            continue

        chunk_embedding = model.encode(
            chunk,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        similarities = util.cos_sim(chunk_embedding, skill_embeddings)[0]

        for i, score in enumerate(similarities):
            if score.item() > SIMILARITY_THRESHOLD:
                detected_skills.add(TECH_SKILLS[i])

    return list(detected_skills)


