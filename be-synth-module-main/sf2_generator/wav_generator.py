import soundfile, io
from .synthesizer import Synthesizer
from .freq_iterator import FreqIterator



def generate_samples_vfs(synth: Synthesizer, freq_iterator: FreqIterator, virtual_dir: str = "samples") -> dict[str, io.BytesIO]:
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