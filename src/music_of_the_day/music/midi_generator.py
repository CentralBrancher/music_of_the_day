import random
import pretty_midi
from typing import List
from music_of_the_day.mapping.semantics_to_music import MusicParameters

# -------------------------
# Piano ranges
# -------------------------
REGISTER_RANGES = {
    "low": (36, 52),   # C2–E3
    "mid": (48, 72),   # C3–C5
    "high": (60, 84),  # C4–C6
}

SCALES = {
    ("C", "major"): [60, 62, 64, 65, 67, 69, 71],
    ("A", "minor"): [57, 59, 60, 62, 64, 65, 67],
}


# -------------------------
# Utility functions
# -------------------------
def expand_register(base_range, energy):
    low, high = base_range
    expansion = int(12 * energy)
    return low - expansion, high + expansion


def generate_motif(scale: List[int], length: int, variation: float) -> List[int]:
    motif = []
    current = random.choice(scale)

    for _ in range(length):
        step = random.choice([-2, -1, 1, 2])
        if random.random() < variation:
            step *= random.choice([1, 2])

        idx = min(range(len(scale)), key=lambda i: abs(scale[i] - current))
        idx = max(0, min(len(scale) - 1, idx + step))
        current = scale[idx]
        motif.append(current)

    return motif


def invert_motif(motif: List[int], center: int) -> List[int]:
    return [center - (n - center) for n in motif]


def stretch_motif(motif: List[int], factor: int) -> List[int]:
    return motif[::max(1, factor)]


def apply_dissonance(note: int, amount: float) -> int:
    if random.random() < amount:
        return note + random.choice([-1, 1])
    return note


def phrase_velocity(step: int, total: int, energy: float) -> int:
    arc = abs((step / total) - 0.5) * 2
    return int(50 + (1 - arc) * 50 * energy)


def add_left_hand(
    piano: pretty_midi.Instrument,
    root: int,
    start: float,
    duration: float,
    energy: float,
    dissonance: float
):
    chord = [root - 12, root - 5]  # octave + fifth

    if energy > 0.5:
        chord.append(root + 2)  # add9 tension

    if dissonance > 0.6:
        chord.append(root - 11)  # cluster tension

    for pitch in chord:
        piano.notes.append(
            pretty_midi.Note(
                velocity=int(40 + energy * 50),
                pitch=pitch,
                start=start,
                end=start + duration
            )
        )


# -------------------------
# Main generator
# -------------------------
def generate_piano_midi(
    params: MusicParameters,
    duration_seconds: int = 75,
    output_path: str = "music.mid"
) -> str:

    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)

    scale = SCALES[(params.key, params.mode)]
    base_range = REGISTER_RANGES[params.register]
    reg_min, reg_max = expand_register(base_range, params.energy)

    scale = [n for n in scale if reg_min <= n <= reg_max]
    if not scale:
        scale = SCALES[(params.key, params.mode)]

    seconds_per_beat = 60.0 / params.tempo
    note_duration = seconds_per_beat * 0.9
    chord_duration = seconds_per_beat * 4

    motif = generate_motif(scale, 8, params.motif_variation)

    time = 0.0
    next_chord_time = 0.0

    while time < duration_seconds:

        # --- Left hand ---
        if time >= next_chord_time and random.random() < params.density:
            root = random.choice(scale)
            add_left_hand(
                piano,
                root=root,
                start=time,
                duration=chord_duration,
                energy=params.energy,
                dissonance=params.dissonance
            )
            next_chord_time = time + chord_duration

        # --- Right hand ---
        for i, note in enumerate(motif):
            if time >= duration_seconds:
                break

            if random.random() > params.density:
                time += note_duration
                continue

            pitch = apply_dissonance(note, params.dissonance)
            velocity = phrase_velocity(i, len(motif), params.energy)

            piano.notes.append(
                pretty_midi.Note(
                    velocity=velocity,
                    pitch=pitch,
                    start=time,
                    end=time + note_duration
                )
            )
            time += note_duration

        # --- Motif evolution ---
        if params.arc == "rise":
            motif = invert_motif(motif, motif[0])
        elif params.arc == "fall":
            motif = stretch_motif(motif, 2)
        elif random.random() < params.motif_variation:
            motif = generate_motif(scale, 8, params.motif_variation)

    pm.instruments.append(piano)
    pm.write(output_path)
    return output_path
