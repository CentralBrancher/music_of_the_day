from music_of_the_day.semantics.features import SemanticFeatures
from music_of_the_day.mapping.semantics_to_music import MusicParameters


def generate_explanation(
    features: SemanticFeatures,
    music: MusicParameters
) -> str:
    lines = []

    lines.append(
        f"The piece is set in {music.key} {music.mode}, reflecting the day's overall tone."
    )

    lines.append(
        f"A tempo of {music.tempo} BPM mirrors the pace of unfolding events."
    )

    if features.semantic_novelty > 0.7:
        lines.append(
            "High semantic novelty introduces evolving motifs and unexpected turns."
        )

    if features.topic_entropy > 0.6:
        lines.append(
            "Dense textures reflect a fragmented and information-heavy news cycle."
        )

    if features.intra_day_dispersion > 0.5:
        lines.append(
            "Dissonant moments capture conflicting narratives and uncertainty."
        )

    lines.append(
        f"The narrative phase is interpreted as '{features.narrative_phase}'."
    )

    return "\n".join(lines)
