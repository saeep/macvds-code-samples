import numpy as np
from abc import ABC, abstractmethod

class Oscillator:
    """Generates a waveform with harmonics."""
    def __init__(self, frequency=440, harmonics=[1, 2, 3, 4, 5], amplitudes=[1.0, 0.6, 0.4, 0.3, 0.2], sample_rate=44100):
        self.frequency = frequency
        self.harmonics = harmonics
        self.amplitudes = amplitudes
        self.sample_rate = sample_rate

    def generate(self, duration=2.0):
        """Generates the waveform."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        waveform = sum(amp * np.sin(2 * np.pi * freq * t) for freq, amp in zip([self.frequency * h for h in self.harmonics], self.amplitudes))
        return t, waveform


class LowPassFilter:
    """Applies a simple low-pass filter using FFT."""
    def __init__(self, cutoff_freq=5000, sample_rate=44100):
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate

    def apply(self, signal):
        fft_signal = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(len(signal), 1/self.sample_rate)
        fft_signal[np.abs(frequencies) > self.cutoff_freq] = 0
        return np.fft.ifft(fft_signal).real


class ADSREnvelope:
    """Applies an ADSR envelope to the waveform."""
    def __init__(self, attack=0.1, decay=0.1, sustain=0.7, release=0.3, sample_rate=44100):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.sample_rate = sample_rate

    def apply(self, signal):
        total_samples = len(signal)
        attack_samples = int(self.attack * self.sample_rate)
        decay_samples = int(self.decay * self.sample_rate)
        release_samples = int(self.release * self.sample_rate)
        sustain_samples = total_samples - (attack_samples + decay_samples + release_samples)

        attack_env = np.linspace(0, 1, attack_samples)
        decay_env = np.linspace(1, self.sustain, decay_samples)
        sustain_env = np.ones(sustain_samples) * self.sustain
        release_env = np.linspace(self.sustain, 0, release_samples)

        envelope_curve = np.concatenate([attack_env, decay_env, sustain_env, release_env])
        envelope_curve = envelope_curve[:total_samples]  # Match length

        return signal * envelope_curve


class LFO:
    """Applies a Low-Frequency Oscillator (LFO) for modulation."""
    def __init__(self, rate=5, depth=0.1, sample_rate=44100):
        self.rate = rate
        self.depth = depth
        self.sample_rate = sample_rate

    def apply(self, signal):
        t = np.linspace(0, len(signal) / self.sample_rate, len(signal), endpoint=False)
        modulation = 1 + self.depth * np.sin(2 * np.pi * self.rate * t)
        return signal * modulation
    

class Synthesizer(ABC):
    """Abstract base class for all synthesizers."""

    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    @abstractmethod
    def generate(self, frequency: float, duration: float):
        """Generate waveform for a given frequency and duration."""
        pass


class Harmonium(Synthesizer):
    """Combines all modules to create a harmonium-like sound."""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

        # Instantiate components
        self.filter = LowPassFilter(cutoff_freq=5000, sample_rate=sample_rate)
        self.envelope = ADSREnvelope(sample_rate=sample_rate)
        self.lfo = LFO(sample_rate=sample_rate)

    def generate(self, frequency=440, duration=2.0):
        """Generates the final waveform."""

        self.oscillator = Oscillator(frequency, sample_rate=self.sample_rate)
        t, waveform = self.oscillator.generate(duration)

        waveform = self.filter.apply(waveform)
        waveform = self.envelope.apply(waveform)
        waveform = self.lfo.apply(waveform)
        
        # Normalize
        waveform /= np.max(np.abs(waveform))
        return t, waveform