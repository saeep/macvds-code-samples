"""Musical frequency iterator module.

This module provides iterator classes for generating frequency sequences based on
different musical tuning systems. It implements MIDI-to-frequency conversion
algorithms and custom iterators for Western equal temperament and Hindustani
tuning systems."""
class FreqIterator:
    """Base class for frequency iteration across musical tuning systems.
    
    This class provides fundamental MIDI-to-frequency conversion functionality
    that serves as the foundation for specific tuning system implementations.
    
    Attributes:
        base_midi (int): The MIDI note number used as the reference point.
        base_freq (float): The frequency in Hz corresponding to base_midi."""
    def __init__(self, base_midi, base_freq):
        """Initialize the frequency iterator with a base MIDI note and frequency.
        
        Args:
            base_midi: MIDI note number to use as reference (0-127).
            base_freq: Frequency in Hz corresponding to the base MIDI note."""
        self.base_midi = base_midi
        self.base_freq = base_freq

    def midi_to_frequency(self, midi_num: int, base_freq: float) -> float:
        """Convert a MIDI note number to frequency using exponential calculation.
        
        Uses the formula: f = base_freq * 2^(midi_num/12)
        This implements the standard equal temperament frequency relationship
        where each octave doubles the frequency.
        
        Args:
            midi_num: The MIDI note number offset from the base.
            base_freq: The reference frequency in Hz.
            
        Returns:
            The calculated frequency in Hz."""
        return base_freq * (2 ** (midi_num / 12))
        
    def nearest_midi_freq(self, midi_num: int) -> tuple[int, float]:
        """Find the nearest base frequency for a given MIDI note.
        
        Calculates the octave-aligned base frequency and returns the offset
        within the octave (0-11 semitones) along with the base frequency.
        
        Args:
            midi_num: The target MIDI note number.
            
        Returns:
            A tuple containing:
                - int: Semitone offset within the octave (0-11).
                - float: The octave-aligned base frequency in Hz.
        """
        midi_diff = midi_num - self.base_midi

        if midi_diff % 12 == 0:
            return (0, self.midi_to_frequency(midi_diff, self.base_freq))

        n = midi_diff % 12
        midi_diff = midi_diff - n
        return(n, self.midi_to_frequency(midi_diff, self.base_freq))


class WesternFreqIterator(FreqIterator):
    """Iterator for Western 12-tone equal temperament tuning system.
    
    Implements the standard Western musical scale where each semitone is
    separated by a frequency ratio of 2^(1/12), creating 12 equal divisions
    of the octave.
    
    Attributes:
        semitone_freq_multiplier (float): The ratio between adjacent semitones (2^(1/12)).
        start_midi (int): Starting MIDI note number for iteration.
        stop_midi (int): Ending MIDI note number (exclusive)."""
    
    semitone_freq_multiplier = 2 ** (1 / 12)

    def __init__(self, base_midi: int, base_freq: float, start_midi: int, stop_midi: int):
        """Initialize the Western frequency iterator.
        
        Args:
            base_midi: Reference MIDI note number (0-127).
            base_freq: Frequency in Hz for the base MIDI note.
            start_midi: First MIDI note to generate.
            stop_midi: MIDI note at which to stop iteration (exclusive)."""
        super().__init__(base_midi, base_freq)

        self.start_midi = start_midi
        self.stop_midi = stop_midi
        
    def __iter__(self):
        """Initialize the iterator state.
        
        Sets up the starting MIDI note and calculates the initial frequency
        based on the nearest octave-aligned base frequency.
        
        Returns:
            self: The iterator instance."""
        self.midi = self.start_midi

        midi_diff, base_freq = self.nearest_midi_freq(self.start_midi)

        self.freq = self.midi_to_frequency(midi_diff, base_freq)

        return self
    
    def __next__(self) -> tuple[int, float]:
        """Generate the next MIDI note and frequency pair.
        
        Advances through the MIDI range, calculating frequencies using
        equal temperament (each semitone multiplied by 2^(1/12)).
        
        Returns:
            A tuple containing:
                - int: Current MIDI note number.
                - float: Corresponding frequency in Hz.
                
        Raises:
            StopIteration: When stop_midi is reached."""
        if self.midi == self.stop_midi:
            raise StopIteration
        
        midi = self.midi
        self.midi += 1

        freq = self.freq
        self.freq *= self.semitone_freq_multiplier

        return (midi, freq)


class HindustaniFreqIterator(FreqIterator):
    """Iterator for Hindustani (Indian classical music) tuning system.
    
    Implements just intonation based on precise frequency ratios (shrutis)
    rather than equal temperament. Each note is defined by a specific
    mathematical ratio relative to the fundamental frequency.
    
    Attributes:
        freq_multipliers (tuple[float]): Sequence of frequency ratios for each shruti.
        start_midi (int): Starting MIDI note number for iteration.
        stop_midi (int): Ending MIDI note number (exclusive).
        index (int): Current position in the freq_multipliers sequence."""
    def __init__(self, base_midi: int, base_freq: float, start_midi: int, stop_midi: int, freq_multipliers: tuple[float]):
        """
        Initialize the Hindustani frequency iterator.
        
        Args:
            base_midi: Reference MIDI note number (0-127).
            base_freq: Frequency in Hz for the base MIDI note (Sa).
            start_midi: First MIDI note to generate.
            stop_midi: MIDI note at which to stop iteration (exclusive).
            freq_multipliers: Tuple of frequency ratios defining the shruti intervals.
        """
        super().__init__(base_midi, base_freq)

        self.freq_multipliers = freq_multipliers
        self.start_midi = start_midi
        self.stop_midi = stop_midi
        
    def __iter__(self):
        """
        Initialize the iterator state.
        
        Sets up the starting MIDI note and calculates the initial position
        within the shruti cycle based on the nearest octave-aligned base frequency.
        
        Returns:
            self: The iterator instance.
        """
        self.midi = self.start_midi

        midi_diff, base_freq = self.nearest_midi_freq(self.start_midi)

        self.freq = base_freq
        self.index = midi_diff

        return self
    
    def __next__(self) -> tuple[int, float]:
        """
        Generate the next MIDI note and frequency pair using shruti ratios.
        
        Advances through the MIDI range, calculating frequencies by applying
        successive frequency multipliers from the shruti system. When the cycle
        completes, the base frequency is doubled for the next octave.
        
        Returns:
            A tuple containing:
                - int: Current MIDI note number.
                - float: Corresponding frequency in Hz based on just intonation.
                
        Raises:
            StopIteration: When stop_midi is reached.
        """
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
        """
        Increment the index within the frequency multipliers cycle.
        
        Wraps around to 0 when reaching the end of the freq_multipliers tuple,
        enabling continuous iteration across multiple octaves.
        """
        self.index = (self.index + 1) % len(self.freq_multipliers)
