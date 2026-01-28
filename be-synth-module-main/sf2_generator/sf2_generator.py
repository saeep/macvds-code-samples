"""
SF2 generation module.

This module provides functionality to generate a SoundFont2 (SF2) file for a
synthesized reed harmonium. It supports both Western 12-TET tuning and
Hindustani shruti-based tuning using optional ratio mappings.
"""

from sf_utils import SfzWriter, Sf2Writer
from .synthesizer import Harmonium
from .freq_iterator import WesternFreqIterator, HindustaniFreqIterator
from . import wav_generator as wav
import io


class Sf2Generator:
    """
    Generate a SoundFont2 (SF2) file from synthesized harmonium samples.

    The generator builds a set of WAV samples (one per MIDI note in a given
    range), writes an SFZ definition, and then converts the SFZ + WAV samples
    into a final SF2 byte stream.

    Attributes:
        base_midi: MIDI note number used as the tuning reference (0–127).
        base_freq: Frequency in Hz for the reference MIDI note.
        midi_low: Lower bound (inclusive) of MIDI note range to generate.
        midi_high: Upper bound (exclusive) of MIDI note range to generate.
        synth: Harmonium synthesizer instance used to generate waveforms.
        freq_iterator: Iterator yielding (midi_note, frequency_hz) pairs based
            on Western or Hindustani tuning.
    """

    def __init__(self, base_midi: int, base_freq: float, ratios: tuple[float, ...] = None):
        """
        Initialize the SF2 generator.

        Args:
            base_midi: Reference MIDI note number (0–127).
            base_freq: Reference frequency in Hz for the base MIDI note.
            ratios: Optional tuple of frequency ratios for Hindustani tuning.
                If provided, HindustaniFreqIterator will be used; otherwise
                WesternFreqIterator will be used.

        Raises:
            ValueError: If base_midi is not within 0–127 or base_freq is not positive.
        """
        if not (0 <= base_midi <= 127):
            raise ValueError(f"base_midi must be in 0-127, got {base_midi}")
        if base_freq <= 0:
            raise ValueError(f"base_freq must be positive, got {base_freq}")

        self.base_midi = base_midi
        self.base_freq = base_freq
        self.midi_low = 48
        self.midi_high = 89 + 1

        self.synth = Harmonium()

        if not ratios:
            self.freq_iterator = WesternFreqIterator(
                self.base_midi, self.base_freq, self.midi_low, self.midi_high
            )
        else:
            self.freq_iterator = HindustaniFreqIterator(
                self.base_midi, self.base_freq, self.midi_low, self.midi_high, ratios
            )

    def get_sf2_bytes(self) -> bytes:
        """
        Generate the SF2 file content as bytes.

        This method:
        1) Generates WAV samples in memory using the synthesizer and frequency iterator.
        2) Writes an SFZ representation into an in-memory text buffer.
        3) Converts the SFZ + WAV samples into an SF2 binary stream.

        Returns:
            The generated SF2 file as a bytes object.

        Raises:
            RuntimeError: If SF2 generation fails at any stage.
        """
        try:
            sample_vfs = wav.generate_samples_vfs(self.synth, self.freq_iterator)

            with io.StringIO() as sfz_buffer, io.BytesIO() as sf2_buffer:
                SfzWriter(sample_vfs).write(sfz_buffer)
                Sf2Writer(sfz_buffer, sample_vfs).write(sf2_buffer)
                return sf2_buffer.getvalue()

        except Exception as e:
            raise RuntimeError(f"Failed to generate SF2 bytes: {e}") from e

        finally:
            # Ensure all in-memory WAV buffers are closed.
            for buffer in sample_vfs.values():
                buffer.close()

    def write(self, file_path: str) -> None:
        """
        Generate and write an SF2 file to disk.

        Args:
            file_path: Output file path where the SF2 file should be saved.

        Raises:
            IOError: If the SF2 file cannot be generated or written to disk.
        """
        try:
            sf2_bytes = self.get_sf2_bytes()
            with open(file_path, "wb") as f:
                f.write(sf2_bytes)

        except Exception as e:
            raise IOError(f"Failed to write SF2 to '{file_path}': {e}") from e
