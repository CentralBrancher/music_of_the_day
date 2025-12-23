import numpy as np
from music_of_the_day.mapping.music_intent import MusicIntent
from music_of_the_day.semantics.features import SemanticFeatures

def build_intent(
    features: SemanticFeatures,
    duration_seconds: int = 75,
    resolution: int = 8
) -> MusicIntent:

    T = duration_seconds * resolution
    t = np.linspace(0, 1, T)

    # --- Base intensity ---
    base_energy = np.clip(
        0.4 * features.semantic_velocity +
        0.3 * features.semantic_novelty +
        0.3 * features.topic_entropy,
        0, 1
    )

    # --- Narrative shaping ---
    if features.narrative_phase == "build_up":
        intensity = base_energy * (0.3 + 0.7 * t)
    elif features.narrative_phase == "climax":
        intensity = base_energy * (1 - np.abs(2 * t - 1))
    elif features.narrative_phase == "aftermath":
        intensity = base_energy * (1 - t)
    else:
        intensity = np.full(T, base_energy)

    # --- Tension ---
    tension = np.clip(
        intensity +
        0.4 * features.intra_day_dispersion,
        0, 1
    )

    # --- Density ---
    density = np.clip(
        0.3 + features.topic_entropy + 0.3 * intensity,
        0, 1
    )

    # --- Harmonic color ---
    if features.emotion.valence < -0.2:
        harmonic_color = "dark"
    elif features.emotion.valence > 0.3:
        harmonic_color = "bright"
    else:
        harmonic_color = "ambiguous"

    # --- Motion profile ---
    motion_profile = {
        "build_up": "rise",
        "climax": "wave",
        "aftermath": "collapse"
    }.get(features.narrative_phase, "drift")

    tempo_base = int(45 + 65 * features.emotion.arousal)

    return MusicIntent(
        duration_seconds=duration_seconds,
        intensity_curve=intensity,
        tension_curve=tension,
        density_curve=density,
        tempo_base=tempo_base,
        harmonic_color=harmonic_color,
        motion_profile=motion_profile,
        emotional_vector=np.array([
            features.emotion.valence,
            features.emotion.arousal,
            features.emotion.tension
        ])
    )
