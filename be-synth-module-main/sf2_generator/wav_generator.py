"""
WAV sample generation utilities.

This module provides helper functionality to generate WAV audio samples
in-memory using a synthesizer and a frequency iterator. The output is stored
as a simple virtual file system (VFS) mapping file paths to BytesIO buffers.
"""

import soundfile, io
from .synthesizer import Synthesizer
from .freq_iterator import FreqIterator


def generate_samples_vfs(
    synth: Synthesizer,
    freq_iterator: FreqIterator,
    virtual_dir: str = "samples"
) -> dict[str, io.BytesIO]:
    """
    Generate WAV samples in-memory for a sequence of MIDI notes.

    For each (midi_num, frequency) produced by the given frequency iterator,
    this function uses the synthesizer to generate a waveform and writes it as
    a 16-bit PCM WAV file into an in-memory buffer.

    The resulting buffers are stored in a dictionary that acts as a virtual file
    system (VFS), where keys are virtual file paths and values are BytesIO
    objects containing WAV data.

    Args:
        synth: Synthesizer instance used to generate waveforms.
        freq_iterator: Iterator yielding (midi_num, frequency_hz) pairs.
        virtual_dir: Virtual directory name used as prefix for generated file paths.

    Returns:
        A dictionary mapping virtual WAV file paths (e.g. "samples/60.wav")
        to BytesIO buffers containing WAV audio data.
    """
    vfs = {}

    for midi_num, freq in freq_iterator:
        _, waveform = synth.generate(freq)

        file_name = f"{midi_num}.wav"
        vfs_path = f"{virtual_dir}/{file_name}"

        buffer = io.BytesIO()
        soundfile.write(buffer, waveform, synth.sample_rate, format='WAV', subtype='PCM_16')
        buffer.seek(0)  # reset pointer for reading later

        vfs[vfs_path] = buffer

    return vfs
