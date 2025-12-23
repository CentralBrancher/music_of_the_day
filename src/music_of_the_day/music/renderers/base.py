import pretty_midi
from abc import ABC, abstractmethod
from music_of_the_day.mapping.music_intent import MusicIntent

class InstrumentRenderer(ABC):

    def __init__(self, program: int, name: str):
        self.instrument = pretty_midi.Instrument(program=program, name=name)

    @abstractmethod
    def render(self, intent: MusicIntent):
        pass
