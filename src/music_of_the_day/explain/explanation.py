from music_of_the_day.semantics.features import SemanticFeatures
from music_of_the_day.mapping.music_intent import MusicIntent


def generate_explanation(
    features: SemanticFeatures,
    music: MusicIntent
) -> str:
    """
    Generate a human-readable explanation linking semantic signals
    to musical interpretation.
    """

    lines: list[str] = []

    # --- Tonal center ---
    lines.append(
        f"The piece centers around {music.key} {music.mode}, "
        f"establishing a tonal atmosphere aligned with the day's emotional balance."
    )

    # --- Tempo & energy ---
    lines.append(
        f"A tempo of {music.tempo} BPM reflects the momentum of current events, "
        f"with an overall energy level of {music.energy:.2f} shaping intensity."
    )

    # --- Narrative arc ---
    if music.arc == "rise":
        lines.append(
            "The composition unfolds as a gradual ascent, mirroring a build-up of tension or anticipation."
        )
    elif music.arc == "wave":
        lines.append(
            "The music follows a wave-like arc, alternating between tension and release as dominant themes collide."
        )
    elif music.arc == "fall":
        lines.append(
            "A downward arc suggests resolution or reflection following earlier intensity."
        )

    # --- Novelty & variation ---
    if features.semantic_novelty > 0.7:
        lines.append(
            "High semantic novelty drives frequent motif transformations, "
            "introducing surprise and instability."
        )
    elif features.semantic_novelty < 0.3:
        lines.append(
            "Low semantic novelty allows motifs to linger, reinforcing continuity and familiarity."
        )

    # --- Texture & density ---
    if features.topic_entropy > 0.6:
        lines.append(
            "Dense musical textures reflect a fragmented and information-heavy news landscape."
        )
    elif features.topic_entropy < 0.4:
        lines.append(
            "A more transparent texture mirrors a focused and coherent narrative space."
        )

    # --- Harmonic tension ---
    if features.intra_day_dispersion > 0.5:
        lines.append(
            "Moments of harmonic tension and dissonance convey conflicting perspectives and uncertainty."
        )

    # --- Emotional layer ---
    emotion = features.emotion
    lines.append(
        f"Emotionally, the piece leans toward a "
        f"{'brighter' if emotion.valence > 0 else 'darker'} tone, "
        f"with arousal at {emotion.arousal:.2f} and tension at {emotion.tension:.2f}."
    )

    # --- Narrative label ---
    lines.append(
        f"Overall, the day is interpreted musically as a phase of '{features.narrative_phase}'."
    )

    return "\n".join(lines)
