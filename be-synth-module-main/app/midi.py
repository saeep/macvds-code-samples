import re

notes = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

def midi_to_note(midi_number: int) -> str:
    if not (0 <= midi_number <= 127):
        raise ValueError(f"Midi Value {midi_number} out of range")
    
    note = notes[midi_number % 12]
    octave = (midi_number // 12) - 1  # Adjust for correct octave range

    return f"{note}{octave}"


def note_to_midi(note: str) -> int:
    match = re.match(r"^([A-G]#?)(-1|\d)?$", note)

    if not match:
        raise ValueError(f"Invalid note {note}")
    
    groups = match.groups()

    note_name = groups[0]

    if groups[1]:
        octave = int(groups[1])
    else:
        octave = 4

    midi_number = (octave + 1) * 12 + notes.index(note_name)

    if not (0 <= midi_number <= 127):
        raise ValueError(f"Midi Value {midi_number} out of range for {note}")

    return midi_number

def get_base_note(note: str) -> str:
    match = re.match(r"^([A-G]#?)(-1|\d)?$", note)

    if not match:
        raise ValueError(f"Invalid note {note}")

    return match.group(1)