import numpy as np

from music_of_the_day.semantics.embed import EmbeddingEngine
from music_of_the_day.semantics.features import (
    aggregate_daily_embedding,
    extract_semantic_features
)
from music_of_the_day.mapping.semantics_to_intent import build_intent

def run_pipeline(
    articles: list[str],
    rolling_embeddings: np.ndarray | None = None,
    embedding_yesterday: np.ndarray | None = None,
    velocity_yesterday: float | None = None,
    emotion_yesterday=None
):
    """
    Semantic → music mapping pipeline.
    """

    # --- Step 1: Compute embeddings ---
    embedder = EmbeddingEngine()
    embeddings_today = embedder.embed(articles)

    # --- Step 2: Aggregate daily embedding ---
    daily_embedding = aggregate_daily_embedding(embeddings_today)

    # --- Step 3: Extract semantic + emotional features ---
    features = extract_semantic_features(
        embeddings_today=embeddings_today,
        daily_embedding_today=daily_embedding,
        rolling_embeddings=rolling_embeddings,
        embedding_yesterday=embedding_yesterday,
        velocity_yesterday=velocity_yesterday,
        emotion_yesterday=emotion_yesterday
    )

    # --- Step 4: Map semantics → music ---
    intent = build_intent(features)

    return features, intent, daily_embedding
