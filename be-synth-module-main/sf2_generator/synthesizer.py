"""
Digital audio synthesis module.

This module implements a modular synthesizer architecture for generating musical
waveforms. It includes components for oscillation, filtering, envelope shaping,
and modulation, combining digital signal processing techniques to create
harmonium-like sounds.
"""

import numpy as np
from abc import ABC, abstractmethod


class Oscillator:
    """
    Generates harmonic waveforms using additive synthesis.
    
    Creates complex tones by summing multiple sine waves (harmonics) with
    specified frequencies and amplitudes. This implements the additive synthesis
    technique commonly used in physical modeling of acoustic instruments.
    
    Attributes:
        frequency (float): Fundamental frequency in Hz.
        harmonics (list): List of harmonic multipliers (e.g., [1, 2, 3] for first three harmonics).
        amplitudes (list): Amplitude coefficients for each harmonic.
        sample_rate (int): Audio sample rate in Hz.
    """
    
    def __init__(self, frequency=440, harmonics=[1, 2, 3, 4, 5], amplitudes=[1.0, 0.6, 0.4, 0.3, 0.2], sample_rate=44100):
        """
        Initialize the oscillator with harmonic content.
        
        Args:
            frequency: Fundamental frequency in Hz (default: 440 Hz, A4).
            harmonics: List of harmonic multipliers relative to fundamental.
            amplitudes: Amplitude weight for each corresponding harmonic.
            sample_rate: Sample rate in Hz for digital audio generation.
        """
        self.frequency = frequency
        self.harmonics = harmonics
        self.amplitudes = amplitudes
        self.sample_rate = sample_rate

    def generate(self, duration=2.0):
        """
        Generate the harmonic waveform using additive synthesis.
        
        Synthesizes audio by summing weighted sine waves at harmonic frequencies.
        Each harmonic contributes according to its amplitude coefficient, creating
        a rich, complex timbre.
        
        Args:
            duration: Length of the waveform in seconds.
            
        Returns:
            A tuple containing:
                - ndarray: Time array in seconds.
                - ndarray: Generated waveform samples.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        waveform = sum(amp * np.sin(2 * np.pi * freq * t) for freq, amp in zip([self.frequency * h for h in self.harmonics], self.amplitudes))
        return t, waveform


class LowPassFilter:
    """
    Applies frequency-domain low-pass filtering using FFT.
    
    Implements a brick-wall low-pass filter by transforming the signal to the
    frequency domain via Fast Fourier Transform (FFT), removing frequencies
    above the cutoff, and transforming back to the time domain.
    
    Attributes:
        cutoff_freq (float): Cutoff frequency in Hz. Frequencies above this are attenuated.
        sample_rate (int): Audio sample rate in Hz.
    """
    
    def __init__(self, cutoff_freq=5000, sample_rate=44100):
        """
        Initialize the low-pass filter.
        
        Args:
            cutoff_freq: Cutoff frequency in Hz. Frequencies above are removed.
            sample_rate: Sample rate in Hz of the audio signal.
        """
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate

    def apply(self, signal):
        """
        Apply the low-pass filter to an audio signal using FFT.
        
        Algorithm:
        1. Transform signal to frequency domain using FFT
        2. Zero out frequency components above cutoff_freq
        3. Transform back to time domain using inverse FFT
        
        Args:
            signal: Input audio signal as a NumPy array.
            
        Returns:
            ndarray: Filtered signal in the time domain.
        """
        fft_signal = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(len(signal), 1/self.sample_rate)
        fft_signal[np.abs(frequencies) > self.cutoff_freq] = 0
        return np.fft.ifft(fft_signal).real


class ADSREnvelope:
    """
    Applies an ADSR (Attack-Decay-Sustain-Release) envelope to shape amplitude over time.
    
    ADSR is a standard envelope model in synthesis:
    - Attack: Initial rise from 0 to peak amplitude
    - Decay: Fall from peak to sustain level
    - Sustain: Held at constant level during note
    - Release: Final fade to silence
    
    This shapes the dynamic contour of the sound, making it more natural and expressive.
    
    Attributes:
        attack (float): Attack time in seconds.
        decay (float): Decay time in seconds.
        sustain (float): Sustain amplitude level (0.0 to 1.0).
        release (float): Release time in seconds.
        sample_rate (int): Audio sample rate in Hz.
    """
    
    def __init__(self, attack=0.1, decay=0.1, sustain=0.7, release=0.3, sample_rate=44100):
        """
        Initialize the ADSR envelope parameters.
        
        Args:
            attack: Time in seconds for amplitude to rise from 0 to 1.
            decay: Time in seconds to fall from 1 to sustain level.
            sustain: Amplitude level to hold during note (0.0-1.0).
            release: Time in seconds to fade from sustain to 0.
            sample_rate: Sample rate in Hz for calculating sample counts.
        """
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.sample_rate = sample_rate

    def apply(self, signal):
        """
        Apply the ADSR envelope to an audio signal.
        
        Constructs an envelope curve by concatenating linear segments for each
        ADSR phase, then multiplies the input signal by this envelope to shape
        its amplitude over time.
        
        Args:
            signal: Input audio signal as a NumPy array.
            
        Returns:
            ndarray: Signal with ADSR envelope applied.
        """
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
    """
    Applies Low-Frequency Oscillator (LFO) modulation for tremolo effect.
    
    An LFO modulates the amplitude of the signal with a slow-moving sine wave,
    creating a periodic variation in volume (tremolo). This adds movement and
    character to the sound.
    
    Attributes:
        rate (float): LFO frequency in Hz (how fast the modulation oscillates).
        depth (float): Modulation depth (0.0-1.0), controlling intensity of effect.
        sample_rate (int): Audio sample rate in Hz.
    """
    
    def __init__(self, rate=5, depth=0.1, sample_rate=44100):
        """
        Initialize the LFO modulator.
        
        Args:
            rate: LFO frequency in Hz (typically 0.1-20 Hz for tremolo).
            depth: Modulation depth (0.0-1.0). Higher values = stronger effect.
            sample_rate: Sample rate in Hz of the audio signal.
        """
        self.rate = rate
        self.depth = depth
        self.sample_rate = sample_rate

    def apply(self, signal):
        """
        Apply LFO amplitude modulation to an audio signal.
        
        Creates a sine wave at the LFO rate and uses it to modulate the signal's
        amplitude, producing a tremolo effect. The modulation is scaled by the
        depth parameter.
        
        Args:
            signal: Input audio signal as a NumPy array.
            
        Returns:
            ndarray: Signal with LFO modulation applied.
        """
        t = np.linspace(0, len(signal) / self.sample_rate, len(signal), endpoint=False)
        modulation = 1 + self.depth * np.sin(2 * np.pi * self.rate * t)
        return signal * modulation
    

class Synthesizer(ABC):
    """
    Abstract base class for all synthesizer implementations.
    
    Defines the interface that all concrete synthesizers must implement.
    This allows for polymorphic use of different synthesis algorithms while
    maintaining a consistent API.
    
    Attributes:
        sample_rate (int): Audio sample rate in Hz.
    """

    def __init__(self, sample_rate=44100):
        """
        Initialize the base synthesizer.
        
        Args:
            sample_rate: Sample rate in Hz for audio generation.
        """
        self.sample_rate = sample_rate

    @abstractmethod
    def generate(self, frequency: float, duration: float):
        """
        Generate a waveform for a given frequency and duration.
        
        This method must be implemented by all subclasses to define their
        specific synthesis algorithm.
        
        Args:
            frequency: Fundamental frequency in Hz.
            duration: Length of the waveform in seconds.
            
        Returns:
            Implementation-specific return value (typically time and waveform arrays).
        """
        pass


class Harmonium(Synthesizer):
    """
    Harmonium synthesizer implementing a complete signal chain.
    
    Combines multiple DSP components (oscillator, filter, envelope, LFO) to
    synthesize harmonium-like sounds. The signal chain is:
    1. Harmonic oscillator (additive synthesis)
    2. Low-pass filter (removes high frequencies)
    3. ADSR envelope (shapes amplitude contour)
    4. LFO (adds tremolo modulation)
    5. Normalization (ensures consistent output level)
    
    This architecture demonstrates composition and modular design in audio synthesis.
    
    Attributes:
        sample_rate (int): Audio sample rate in Hz.
        filter (LowPassFilter): Low-pass filter component.
        envelope (ADSREnvelope): ADSR envelope shaper.
        lfo (LFO): Low-frequency oscillator for modulation.
        oscillator (Oscillator): Harmonic oscillator (created per note).
    """
    
    def __init__(self, sample_rate=44100):
        """
        Initialize the Harmonium synthesizer and its components.
        
        Sets up the complete signal processing chain with default parameters
        tuned for harmonium-like timbres.
        
        Args:
            sample_rate: Sample rate in Hz for audio generation.
        """
        self.sample_rate = sample_rate

        # Instantiate components
        self.filter = LowPassFilter(cutoff_freq=5000, sample_rate=sample_rate)
        self.envelope = ADSREnvelope(sample_rate=sample_rate)
        self.lfo = LFO(sample_rate=sample_rate)

    def generate(self, frequency=440, duration=2.0):
        """
        Generate a harmonium-like waveform at the specified frequency.
        
        Synthesizes audio by passing a harmonic oscillator output through
        the complete signal chain: filtering, envelope shaping, modulation,
        and normalization.
        
        Args:
            frequency: Fundamental frequency in Hz.
            duration: Length of the waveform in seconds.
            
        Returns:
            A tuple containing:
                - ndarray: Time array in seconds.
                - ndarray: Synthesized and normalized waveform samples.
        """
        self.oscillator = Oscillator(frequency, sample_rate=self.sample_rate)
        t, waveform = self.oscillator.generate(duration)

        waveform = self.filter.apply(waveform)
        waveform = self.envelope.apply(waveform)
        waveform = self.lfo.apply(waveform)
        
        # Normalize
        waveform /= np.max(np.abs(waveform))
        return t, waveform
