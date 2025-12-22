import os
import pretty_midi
import pytest

from music_of_the_day.music.midi_generator import generate_piano_midi
from music_of_the_day.mapping.semantics_to_music import MusicParameters


@pytest.mark.parametrize(
    "params,expect_warning",
    [
        # Low register incompatible with C major scale
        (MusicParameters(
            key="C",
            mode="major",
            tempo=60,
            density=0.5,
            dissonance=0.2,
            register="low",
            motif_variation=0.3
        ), True),

        # Mid register compatible with A minor
        (MusicParameters(
            key="A",
            mode="minor",
            tempo=90,
            density=0.8,
            dissonance=0.5,
            register="mid",
            motif_variation=0.6
        ), False),

        # High register compatible with C major
        (MusicParameters(
            key="C",
            mode="major",
            tempo=75,
            density=0.3,
            dissonance=0.1,
            register="high",
            motif_variation=0.1
        ), False),
    ]
)
def test_generate_piano_midi(tmp_path, params, expect_warning, capsys):
    """
    Test full MIDI generation including:
    - melody + left-hand chords
    - register filtering
    - warning printed if register incompatible
    """
    output_path = tmp_path / "test.mid"

    result_path = generate_piano_midi(
        params,
        duration_seconds=10,
        output_path=str(output_path)
    )

    # File exists
    assert os.path.exists(result_path)

    # File is non-empty
    assert os.path.getsize(result_path) > 0

    # Load MIDI and check instruments
    midi = pretty_midi.PrettyMIDI(result_path)
    assert len(midi.instruments) == 1
    notes = midi.instruments[0].notes
    assert len(notes) > 0

    # Optional: Check note pitches within safe MIDI range
    for note in notes:
        assert 24 <= note.pitch <= 84

    # Capture stdout for warning
    captured = capsys.readouterr()
    if expect_warning:
        assert "⚠️ Warning: Register" in captured.out
    else:
        assert "⚠️ Warning: Register" not in captured.out
