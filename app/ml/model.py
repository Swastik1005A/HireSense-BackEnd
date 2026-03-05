from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class EmbeddingModel:
    def __init__(self):
        # Load pre-trained sentence transformer model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, text: str):
        # Convert text into embedding vector
        embedding = self.model.encode(text)
        return embedding

    def similarity(self, text1: str, text2: str):
        emb1 = self.encode(text1)
        emb2 = self.encode(text2)

        # Reshape because sklearn expects 2D arrays
        emb1 = emb1.reshape(1, -1)
        emb2 = emb2.reshape(1, -1)

        score = cosine_similarity(emb1, emb2)[0][0]

        return float(score)


# Singleton instance (load once)
embedding_model = EmbeddingModel()