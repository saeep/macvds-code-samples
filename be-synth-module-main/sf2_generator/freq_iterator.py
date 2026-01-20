class FreqIterator:
    def __init__(self, base_midi, base_freq):
        self.base_midi = base_midi
        self.base_freq = base_freq

    def midi_to_frequency(self, midi_num: int, base_freq: float) -> float:
        return base_freq * (2 ** (midi_num / 12))
        
    def nearest_midi_freq(self, midi_num: int) -> tuple[int, float]:
        midi_diff = midi_num - self.base_midi

        if midi_diff % 12 == 0:
            return (0, self.midi_to_frequency(midi_diff, self.base_freq))

        n = midi_diff % 12
        midi_diff = midi_diff - n
        return(n, self.midi_to_frequency(midi_diff, self.base_freq))


class WesternFreqIterator(FreqIterator):
    semitone_freq_multiplier = 2 ** (1 / 12)

    def __init__(self, base_midi: int, base_freq: float, start_midi: int, stop_midi: int):
        super().__init__(base_midi, base_freq)

        self.start_midi = start_midi
        self.stop_midi = stop_midi
        
    def __iter__(self):
        self.midi = self.start_midi

        midi_diff, base_freq = self.nearest_midi_freq(self.start_midi)

        self.freq = self.midi_to_frequency(midi_diff, base_freq)

        return self
    
    def __next__(self) -> tuple[int, float]:
        if self.midi == self.stop_midi:
            raise StopIteration
        
        midi = self.midi
        self.midi += 1

        freq = self.freq
        self.freq *= self.semitone_freq_multiplier

        return (midi, freq)
       

class HindustaniFreqIterator(FreqIterator):
    def __init__(self, base_midi: int, base_freq: float, start_midi: int, stop_midi: int, freq_multipliers: tuple[float]):
        super().__init__(base_midi, base_freq)

        self.freq_multipliers = freq_multipliers
        self.start_midi = start_midi
        self.stop_midi = stop_midi
        
    def __iter__(self):
        self.midi = self.start_midi

        midi_diff, base_freq = self.nearest_midi_freq(self.start_midi)

        self.freq = base_freq
        self.index = midi_diff

        return self
    
    def __next__(self) -> tuple[int, float]:
        if self.midi == self.stop_midi:
            raise StopIteration
        
        midi = self.midi
        self.midi += 1
        
        freq = self.freq * self.freq_multipliers[self.index]

        self.inc_index()

        if self.index == 0:
            self.freq *= 2
        
        return (midi, freq)
    
    def inc_index(self):
        self.index = (self.index + 1) % len(self.freq_multipliers)