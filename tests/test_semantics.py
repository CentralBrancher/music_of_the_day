import numpy as np
from music_of_the_day.semantics.features import extract_semantic_features


def test_semantic_feature_shapes():
    embeddings_today = np.random.rand(10, 768)
    daily_embedding = embeddings_today.mean(axis=0)
    rolling_embeddings = np.random.rand(7, 768)

    features = extract_semantic_features(
        embeddings_today=embeddings_today,
        daily_embedding_today=daily_embedding,
        rolling_embeddings=rolling_embeddings,
        embedding_yesterday=None,
        velocity_yesterday=None
    )

    assert 0.0 <= features.semantic_shift <= 1.0
    assert 0.0 <= features.semantic_novelty <= 1.5
    assert features.num_topics > 0
    assert features.narrative_phase in {
        "build_up", "climax", "aftermath", "stasis"
    }
