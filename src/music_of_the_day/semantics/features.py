import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from sklearn.cluster import KMeans
from dataclasses import dataclass
from typing import Optional

from music_of_the_day.semantics.emotion import EmotionState, update_emotion


@dataclass
class SemanticFeatures:
    semantic_shift: float
    semantic_novelty: float
    num_topics: int
    topic_dominance: float
    topic_entropy: float
    semantic_velocity: float
    semantic_acceleration: float
    intra_day_dispersion: float
    narrative_phase: str
    emotion: EmotionState


def aggregate_daily_embedding(
    embeddings: np.ndarray,
    weights: Optional[np.ndarray] = None
) -> np.ndarray:
    if weights is None:
        return embeddings.mean(axis=0)
    return np.average(embeddings, axis=0, weights=weights)


def compute_semantic_shift(today: np.ndarray, rolling_mean: Optional[np.ndarray]) -> float:
    if rolling_mean is None:
        return 0.0
    return float(1 - cosine_similarity([today], [rolling_mean])[0][0])


def compute_semantic_novelty(today: np.ndarray, rolling_embeddings: Optional[np.ndarray]) -> float:
    if rolling_embeddings is None or len(rolling_embeddings) == 0:
        return 0.0
    distances = cosine_distances([today], rolling_embeddings)[0]
    return float(np.percentile(distances, 90))


def cluster_topics(embeddings: np.ndarray, k: int) -> np.ndarray:
    if len(embeddings) < k:
        k = max(1, len(embeddings))
    model = KMeans(n_clusters=k, n_init=10, random_state=42)
    return model.fit_predict(embeddings)


def compute_topic_entropy(cluster_labels: np.ndarray) -> float:
    counts = np.bincount(cluster_labels)
    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log(probs + 1e-9))
    return float(entropy / np.log(len(probs))) if len(probs) > 1 else 0.0


def compute_intra_day_dispersion(embeddings: np.ndarray) -> float:
    if len(embeddings) < 2:
        return 0.0
    distances = cosine_distances(embeddings)
    return float(distances.mean())


def classify_narrative_phase(velocity: float, acceleration: float, entropy: float) -> str:
    if velocity > 0.6 and entropy > 0.6:
        return "climax"
    if acceleration > 0.2:
        return "build_up"
    if velocity < 0.3 and entropy < 0.4:
        return "aftermath"
    return "stasis"


def extract_semantic_features(
    embeddings_today: np.ndarray,
    daily_embedding_today: np.ndarray,
    rolling_embeddings: Optional[np.ndarray] = None,
    embedding_yesterday: Optional[np.ndarray] = None,
    velocity_yesterday: Optional[float] = None,
    emotion_yesterday: Optional[EmotionState] = None,
    num_clusters: int = 4
) -> SemanticFeatures:

    rolling_mean = rolling_embeddings.mean(axis=0) if rolling_embeddings is not None else None

    semantic_shift = compute_semantic_shift(daily_embedding_today, rolling_mean)
    semantic_novelty = compute_semantic_novelty(daily_embedding_today, rolling_embeddings)

    cluster_labels = cluster_topics(embeddings_today, num_clusters)
    counts = np.bincount(cluster_labels)

    num_topics = len(np.unique(cluster_labels))
    topic_dominance = float(counts.max() / counts.sum())
    topic_entropy = compute_topic_entropy(cluster_labels)

    intra_day_dispersion = compute_intra_day_dispersion(embeddings_today)

    if embedding_yesterday is not None:
        semantic_velocity = float(
            cosine_distances([daily_embedding_today], [embedding_yesterday])[0][0]
        )
    else:
        semantic_velocity = 0.0

    if velocity_yesterday is not None:
        semantic_acceleration = semantic_velocity - velocity_yesterday
    else:
        semantic_acceleration = 0.0

    narrative_phase = classify_narrative_phase(
        semantic_velocity,
        semantic_acceleration,
        topic_entropy
    )

    emotion = update_emotion(
        daily_embedding_today,
        semantic_velocity,
        semantic_novelty,
        emotion_yesterday
    )

    return SemanticFeatures(
        semantic_shift=semantic_shift,
        semantic_novelty=semantic_novelty,
        num_topics=num_topics,
        topic_dominance=topic_dominance,
        topic_entropy=topic_entropy,
        semantic_velocity=semantic_velocity,
        semantic_acceleration=semantic_acceleration,
        intra_day_dispersion=intra_day_dispersion,
        narrative_phase=narrative_phase,
        emotion=emotion
    )
