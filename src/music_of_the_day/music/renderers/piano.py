import numpy as np
import pretty_midi
from music_of_the_day.music.renderers.base import InstrumentRenderer

class PianoRenderer(InstrumentRenderer):

    def __init__(self):
        super().__init__(program=0, name="Piano")

    def render(self, intent):
        root = 60
        T = len(intent.intensity_curve)
        dt = intent.duration_seconds / T

        for i in range(T):
            if np.random.rand() > intent.density_curve[i]:
                continue

            pitch = root + np.random.choice([0, 3, 7, 10])
            velocity = int(50 + 40 * intent.intensity_curve[i])

            self.instrument.notes.append(
                pretty_midi.Note(
                    velocity=velocity,
                    pitch=pitch,
                    start=i * dt,
                    end=i * dt + dt
                )
            )
