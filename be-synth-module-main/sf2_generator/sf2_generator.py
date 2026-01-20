from sf_utils import SfzWriter, Sf2Writer
from .synthesizer import Harmonium
from .freq_iterator import WesternFreqIterator, HindustaniFreqIterator
from . import wav_generator as wav
import io

class Sf2Generator:
    def __init__(self, base_midi: int, base_freq: float, ratios: tuple[float, ...] = None):
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
            self.freq_iterator = WesternFreqIterator(self.base_midi, self.base_freq, self.midi_low, self.midi_high)
        else:
            self.freq_iterator = HindustaniFreqIterator(self.base_midi, self.base_freq, self.midi_low, self.midi_high, ratios)
    

    def get_sf2_bytes(self) -> bytes:
        try:
            sample_vfs = wav.generate_samples_vfs(self.synth, self.freq_iterator)

            with io.StringIO() as sfz_buffer, io.BytesIO() as sf2_buffer:
                SfzWriter(sample_vfs).write(sfz_buffer)
                Sf2Writer(sfz_buffer, sample_vfs).write(sf2_buffer)
                return sf2_buffer.getvalue()

        except Exception as e:
            raise RuntimeError(f"Failed to generate SF2 bytes: {e}") from e
        
        finally:
            for buffer in sample_vfs.values():
                buffer.close()
    
    
    def write(self, file_path: str) -> None:
        try:
            sf2_bytes = self.get_sf2_bytes()
            with open(file_path, "wb") as f:
                f.write(sf2_bytes)

        except Exception as e:
            raise IOError(f"Failed to write SF2 to '{file_path}': {e}") from e