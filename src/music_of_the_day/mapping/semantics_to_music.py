from dataclasses import dataclass
from music_of_the_day.semantics.features import SemanticFeatures


@dataclass
class MusicParameters:
    key: str
    mode: str
    tempo: int
    density: float
    dissonance: float
    register: str
    motif_variation: float

    # NEW
    energy: float          # overall intensity (0–1)
    arc: str               # "rise", "fall", "wave"


def map_semantics_to_music(features: SemanticFeatures) -> MusicParameters:
    # --- Key & mode ---
    mode = "minor" if features.semantic_shift > 0.4 else "major"
    key = "A" if mode == "minor" else "C"

    # --- Tempo ---
    tempo = int(55 + features.semantic_velocity * 55)
    tempo = max(40, min(110, tempo))

    # --- Texture ---
    density = min(1.0, 0.3 + features.topic_entropy)
    dissonance = min(1.0, features.intra_day_dispersion)

    # --- Register ---
    if features.semantic_novelty > 0.7:
        register = "high"
    elif features.semantic_shift > 0.5:
        register = "low"
    else:
        register = "mid"

    # --- Energy (THIS DRIVES OOMPH) ---
    energy = min(
        1.0,
        0.5 * features.semantic_velocity +
        0.3 * features.semantic_novelty +
        0.2 * features.topic_entropy
    )

    # --- Narrative arc ---
    if features.narrative_phase == "build_up":
        arc = "rise"
    elif features.narrative_phase == "climax":
        arc = "wave"
    else:
        arc = "fall"

    return MusicParameters(
        key=key,
        mode=mode,
        tempo=tempo,
        density=density,
        dissonance=dissonance,
        register=register,
        motif_variation=features.semantic_novelty,
        energy=energy,
        arc=arc
    )
