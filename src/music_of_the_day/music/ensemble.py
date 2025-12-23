import pretty_midi
from music_of_the_day.mapping.music_intent import MusicIntent
from music_of_the_day.music.renderers.piano import PianoRenderer
from music_of_the_day.music.renderers.strings import StringsRenderer
from music_of_the_day.music.renderers.bass import BassRenderer
from music_of_the_day.music.renderers.percussion import PercussionRenderer

def render_ensemble(intent: MusicIntent, output_path: str):
    pm = pretty_midi.PrettyMIDI()

    renderers = [
        StringsRenderer(),
        BassRenderer(),
        PianoRenderer(),
        PercussionRenderer()
    ]

    for r in renderers:
        r.render(intent)
        pm.instruments.append(r.instrument)

    pm.write(output_path)
