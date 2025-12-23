import os
import numpy as np
import pretty_midi
import pytest

from music_of_the_day.mapping.music_intent import MusicIntent
from music_of_the_day.music.ensemble import render_ensemble


def make_intent(
    duration_seconds: int = 10,
    tempo_base: int = 72,
    motion_profile: str = "wave",
    harmonic_color: str = "ambiguous",
):
    """
    Helper to construct a minimal but valid MusicIntent.
    """
    T = duration_seconds

    return MusicIntent(
        duration_seconds=duration_seconds,
        intensity_curve=np.linspace(0.2, 0.8, T),
        tension_curve=np.linspace(0.1, 0.6, T),
        density_curve=np.clip(np.random.rand(T), 0.2, 0.9),
        tempo_base=tempo_base,
        harmonic_color=harmonic_color,
        motion_profile=motion_profile,
        emotional_vector=np.array([0.1, 0.6, 0.4])
    )


def test_render_ensemble_creates_valid_midi(tmp_path):
    """
    Full integration test:
    - Ensemble rendering
    - Multiple instruments
    - Notes are written
    """
    output_path = tmp_path / "ensemble.mid"
    intent = make_intent(duration_seconds=8)

    render_ensemble(intent, str(output_path))

    # File exists and is non-empty
    assert output_path.exists()
    assert output_path.stat().st_size > 0

    midi = pretty_midi.PrettyMIDI(str(output_path))

    # Expect multiple instruments (piano, strings, bass, percussion)
    assert len(midi.instruments) >= 3

    # At least one note must exist overall
    total_notes = sum(len(inst.notes) for inst in midi.instruments)
    assert total_notes > 0


def test_music_intent_curves_are_consistent():
    """
    Validate MusicIntent structural integrity.
    """
    duration = 12
    intent = make_intent(duration_seconds=duration)

    assert intent.intensity_curve.shape == (duration,)
    assert intent.tension_curve.shape == (duration,)
    assert intent.density_curve.shape == (duration,)

    for curve in [
        intent.intensity_curve,
        intent.tension_curve,
        intent.density_curve,
    ]:
        assert np.all(curve >= 0.0)
        assert np.all(curve <= 1.0)


@pytest.mark.parametrize(
    "motion_profile",
    ["drift", "rise", "wave", "collapse"]
)
def test_motion_profiles_do_not_crash(tmp_path, motion_profile):
    """
    Renderer smoke test across narrative motion profiles.
    """
    output_path = tmp_path / f"{motion_profile}.mid"
    intent = make_intent(
        duration_seconds=6,
        motion_profile=motion_profile
    )

    render_ensemble(intent, str(output_path))

    midi = pretty_midi.PrettyMIDI(str(output_path))
    assert len(midi.instruments) > 0


@pytest.mark.parametrize(
    "harmonic_color",
    ["bright", "dark", "ambiguous"]
)
def test_harmonic_colors_render(tmp_path, harmonic_color):
    """
    Ensure harmonic color changes don't break rendering.
    """
    output_path = tmp_path / f"{harmonic_color}.mid"
    intent = make_intent(
        duration_seconds=6,
        harmonic_color=harmonic_color
    )

    render_ensemble(intent, str(output_path))

    midi = pretty_midi.PrettyMIDI(str(output_path))
    assert sum(len(i.notes) for i in midi.instruments) > 0
