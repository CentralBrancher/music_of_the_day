import pretty_midi
from music_of_the_day.music.renderers.base import InstrumentRenderer

class BassRenderer(InstrumentRenderer):

    def __init__(self):
        super().__init__(program=32, name="Bass")

    def render(self, intent):
        root = 48
        T = len(intent.intensity_curve)
        dt = intent.duration_seconds / T

        for i in range(0, T, 8):
            if intent.intensity_curve[i] < 0.3:
                continue

            self.instrument.notes.append(
                pretty_midi.Note(
                    velocity=int(30 + 40 * intent.intensity_curve[i]),
                    pitch=root,
                    start=i * dt,
                    end=(i + 4) * dt
                )
            )
