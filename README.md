# Soundfont Generator App

The Soundfont Generator App is a Python project that generates **sample-based SoundFont2 (SF2) files** for a reed harmonium using synthesized audio. It demonstrates modular, object-oriented programming and algorithmic design in Python.

The project supports multiple tuning systems:

- **Western 12-TET tuning** – standard Western semitone mapping  
- **Hindustani tuning** – shruti-based tuning with default or custom frequency ratios  

Users can generate SF2 files by specifying a **base MIDI note**, **base frequency**, and tuning system. The project synthesizes audio samples in-memory and compiles them into an SF2 SoundFont file.

---

## Features
 
- Synthesizer with **oscillators, ADSR envelope, low-pass filter, and LFO** for realistic harmonium timbres  
- Frequency iterators for Western and Hindustani tuning systems  
- Generates WAV samples programmatically and packages them into **SF2 files**  

---

## Project Structure

```

.
├── synthesizer.py      # Core synthesizer with oscillator, filter, envelope, and modulation
├── freq_iterator.py    # Iterators for generating note frequencies
├── wav_generator.py    # In-memory WAV sample generation
├── sf2_generator.py    # SF2 compilation from WAV samples
├── app/                # Optional interface (Streamlit) for SF2 generation
└── README.md           # Documentation

```
