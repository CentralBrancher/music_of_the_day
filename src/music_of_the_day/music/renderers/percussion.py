import numpy as np
import pretty_midi
from music_of_the_day.music.renderers.base import InstrumentRenderer

class PercussionRenderer(InstrumentRenderer):

    def __init__(self):
        super().__init__(program=0, name="Percussion")
        self.instrument.is_drum = True

    def render(self, intent):
        T = len(intent.intensity_curve)
        dt = intent.duration_seconds / T

        for i in range(T):
            if intent.intensity_curve[i] < 0.4:
                continue

            if np.random.rand() < intent.intensity_curve[i]:
                self.instrument.notes.append(
                    pretty_midi.Note(
                        velocity=int(40 + 50 * intent.intensity_curve[i]),
                        pitch=36,  # kick
                        start=i * dt,
                        end=i * dt + dt * 0.5
                    )
                )
