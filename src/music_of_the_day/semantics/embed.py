from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import hashlib


class EmbeddingEngine:
    def __init__(
        self,
        model_name: str = "all-mpnet-base-v2",
        cache_dir: str = "data/cache/embeddings"
    ):
        self.model = SentenceTransformer(model_name)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _hash_texts(self, texts):
        joined = "||".join(texts)
        return hashlib.md5(joined.encode()).hexdigest()

    def embed(self, texts, use_cache: bool = True) -> np.ndarray:
        """
        Returns embeddings as a 2D array: [num_texts, embedding_dim].
        Prevents 3D arrays from nested lists.
        """
        if not isinstance(texts, list):
            raise ValueError("Input must be a list of strings")
        if len(texts) == 0:
            return np.zeros((0, self.model.get_sentence_embedding_dimension()))

        cache_key = self._hash_texts(texts)
        cache_path = self.cache_dir / f"{cache_key}.npy"

        if use_cache and cache_path.exists():
            embeddings = np.load(cache_path)
        else:
            embeddings = self.model.encode(
                texts,
                show_progress_bar=False,
                normalize_embeddings=True
            )
            np.save(cache_path, embeddings)

        # Ensure 2D array
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        elif embeddings.ndim > 2:
            embeddings = embeddings.squeeze()
        
        return embeddings
