import pretty_midi
from music_of_the_day.music.renderers.base import InstrumentRenderer

class StringsRenderer(InstrumentRenderer):

    def __init__(self):
        super().__init__(program=48, name="Strings")

    def render(self, intent):
        root = 60 if intent.harmonic_color != "dark" else 57
        T = len(intent.intensity_curve)
        dt = intent.duration_seconds / T

        for i in range(0, T, 16):
            tension = intent.tension_curve[i]
            pitch = root + (7 if tension > 0.6 else 0)

            self.instrument.notes.append(
                pretty_midi.Note(
                    velocity=int(30 + 50 * intent.intensity_curve[i]),
                    pitch=pitch,
                    start=i * dt,
                    end=(i + 16) * dt
                )
            )
