from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class EmotionState:
    """
    Continuous emotional state derived from semantics.
    """
    valence: float   # -1 → 1  (sad ↔ happy)
    arousal: float   # 0 → 1   (calm ↔ energetic)
    tension: float   # 0 → 1   (stable ↔ anxious)


def update_emotion(
    daily_embedding: np.ndarray,
    semantic_velocity: float,
    semantic_novelty: float,
    emotion_yesterday: Optional[EmotionState] = None,
    alpha: float = 0.7
) -> EmotionState:
    """
    Compute today's emotion and smoothly update from yesterday.
    """

    # --- Raw emotion extraction ---
    valence = float(np.tanh(daily_embedding.mean()))
    arousal = float(min(1.0, semantic_velocity * 1.5))
    tension = float(min(1.0, 0.5 * semantic_novelty + 0.5 * semantic_velocity))

    raw = EmotionState(
        valence=valence,
        arousal=arousal,
        tension=tension
    )

    # --- No continuity available ---
    if emotion_yesterday is None:
        return raw

    # --- Exponential smoothing ---
    return EmotionState(
        valence=alpha * emotion_yesterday.valence + (1 - alpha) * raw.valence,
        arousal=alpha * emotion_yesterday.arousal + (1 - alpha) * raw.arousal,
        tension=alpha * emotion_yesterday.tension + (1 - alpha) * raw.tension,
    )
