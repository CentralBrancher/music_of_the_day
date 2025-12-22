import pretty_midi
from pathlib import Path
import scipy.io.wavfile as wavfile


def render_midi_to_wav(
    midi_path: str,
    wav_path: str,
    soundfont_path: str
) -> str:
    """
    Converts a MIDI file to WAV using the given SoundFont.

    Args:
        midi_path: path to the input MIDI file
        wav_path: path to the output WAV file
        soundfont_path: path to a .sf2 SoundFont file

    Returns:
        Path to the WAV file.
    """
    midi = pretty_midi.PrettyMIDI(midi_path)
    audio = midi.fluidsynth(fs=44100, sf2_path=soundfont_path)

    wavfile.write(wav_path, 44100, audio)
    return wav_path
