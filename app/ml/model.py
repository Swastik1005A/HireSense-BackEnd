from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class EmbeddingModel:
    def __init__(self):
        self.model = None  # do not load immediately

    def load_model(self):
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, text: str):
        self.load_model()
        embedding = self.model.encode(text)
        return embedding

    def similarity(self, text1: str, text2: str):
        emb1 = self.encode(text1)
        emb2 = self.encode(text2)

        emb1 = emb1.reshape(1, -1)
        emb2 = emb2.reshape(1, -1)

        score = cosine_similarity(emb1, emb2)[0][0]
        return float(score)


# Singleton instance
embedding_model = EmbeddingModel()