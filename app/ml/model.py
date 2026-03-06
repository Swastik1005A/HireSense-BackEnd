from sentence_transformers import SentenceTransformer, util
import threading


class EmbeddingModel:
    """
    Singleton-style embedding model manager.

    Features
    --------
    • Lazy model loading
    • Thread-safe initialization
    • Batch encoding support
    • Built-in cosine similarity
    """

    def __init__(self):
        self.model = None
        self._lock = threading.Lock()

    def load_model(self):
        """
        Load SentenceTransformer only once.
        Thread-safe for FastAPI workers.
        """
        if self.model is None:
            with self._lock:
                if self.model is None:
                    self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, text, normalize=True, to_tensor=True):
        """
        Encode text or list of texts into embeddings.
        """
        self.load_model()

        return self.model.encode(
            text,
            convert_to_tensor=to_tensor,
            normalize_embeddings=normalize
        )

    def similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.
        """
        emb1 = self.encode(text1)
        emb2 = self.encode(text2)

        score = util.cos_sim(emb1, emb2).item()
        return float(score)


# Global singleton
embedding_model = EmbeddingModel()