from music_of_the_day.semantics.features import SemanticFeatures
from music_of_the_day.mapping.music_intent import MusicIntent
import numpy as np


def generate_explanation(
    features: SemanticFeatures,
    music: MusicIntent
) -> str:
    """
    Generate a human-readable explanation linking semantic signals
    to musical interpretation.
    """

    lines: list[str] = []

    # --- Harmonic color / tonal atmosphere ---
    lines.append(
        f"The piece adopts a {music.harmonic_color} harmonic palette, "
        f"setting an emotional atmosphere aligned with the day's semantic tone."
    )

    # --- Tempo & overall energy ---
    mean_intensity = float(np.mean(music.intensity_curve))
    lines.append(
        f"A base tempo of {music.tempo_base} BPM underpins the composition, "
        f"with an average intensity of {mean_intensity:.2f} shaping its momentum."
    )

    # --- Motion / narrative arc ---
    if music.motion_profile == "rise":
        lines.append(
            "The music follows a rising trajectory, gradually building energy and expectation."
        )
    elif music.motion_profile == "wave":
        lines.append(
            "A wave-like motion alternates between tension and release, reflecting competing forces."
        )
    elif music.motion_profile == "collapse":
        lines.append(
            "A collapsing motion suggests fragmentation and loss of structural stability."
        )
    elif music.motion_profile == "drift":
        lines.append(
            "A drifting motion creates a sense of suspension and unresolved direction."
        )

    # --- Novelty & variation ---
    if features.semantic_novelty > 0.7:
        lines.append(
            "High semantic novelty drives frequent musical variation, "
            "producing surprise and instability."
        )
    elif features.semantic_novelty < 0.3:
        lines.append(
            "Low semantic novelty allows musical ideas to persist, "
            "reinforcing continuity and familiarity."
        )

    # --- Texture & density ---
    mean_density = float(np.mean(music.density_curve))
    if features.topic_entropy > 0.6:
        lines.append(
            f"Dense textures (avg. density {mean_density:.2f}) mirror a fragmented, information-heavy landscape."
        )
    elif features.topic_entropy < 0.4:
        lines.append(
            f"A more transparent texture (avg. density {mean_density:.2f}) reflects narrative focus and clarity."
        )

    # --- Harmonic / emotional tension ---
    mean_tension = float(np.mean(music.tension_curve))
    if features.intra_day_dispersion > 0.5:
        lines.append(
            f"Elevated harmonic tension (avg. {mean_tension:.2f}) conveys conflicting perspectives and uncertainty."
        )

    # --- Emotional layer ---
    valence, arousal, tension = music.emotional_vector
    lines.append(
        f"Emotionally, the piece leans "
        f"{'brighter' if valence > 0 else 'darker'}, "
        f"with arousal at {arousal:.2f} and emotional tension at {tension:.2f}."
    )

    # --- Narrative label ---
    lines.append(
        f"Overall, the day is interpreted musically as a phase of '{features.narrative_phase}'."
    )

    return "\n".join(lines)
