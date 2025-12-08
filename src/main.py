import mido
import time
from irrationals_in_bases import *

scale = 60
port = None
velocity = 64  # Medium velocity

def main():
    global scale
    scale = note_name_to_midi(input("What key should the song play in? (e.g., C, D#, F): ").strip().upper())
    digits = get_irrational_digits(input("What number should we listen to? ").strip().lower(),
                                   int(input("And for how many digits? ")),
                                   base=7)

    port_name = mido.get_output_names()[0]  # Select the first available MIDI output port

    global port
    with mido.open_output(port_name) as port:
        for digit in digits:
            notes = [note_from_scale_degree(digit) for digit in triad_in_key(int(digit))]
            duration = 0.5  # Duration in seconds
            for note in notes:
                start_note(note)
            for i in range(4):
                start_note(note_from_scale_degree(digit + i))
                time.sleep(duration)
            for note in notes:
                end_note(note)

def start_note(note, channel=0):
    global port
    global velocity
    note_on = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
    port.send(note_on)
    return note_on

def end_note(note, channel=0):
    global port
    note_off = mido.Message('note_off', note=note, velocity=0, channel=channel)
    port.send(note_off)
    return note_off

def note_name_to_midi(note_name):
    """Convert a note name (e.g., C, D#, F) to its corresponding MIDI number."""
    note_names = ['C', 'ε', 'D', 'ε', 'E', 'F', 'ε', 'G', 'ε', 'A', 'ε', 'B']
    octave = 4  # Default octave
    if len(note_name) > 2 and note_name[-1].isdigit():
        octave = int(note_name[-1])
        note_name = note_name[:-1]
    if note_name[0] in note_names:
        note_index = note_names.index(note_name[0])
        base_note = 12 * (octave + 1) + note_index
        return(base_note + 1 if "#" in note_name else (base_note - 1 if "b" in note_name else base_note))
    else:
        raise ValueError(f"Invalid note name: " + note_name)

def note_from_scale_degree(degree_num: int) -> int:
    """Convert a scale degree to a MIDI note number based on the global scale variable."""
    global scale
    return scale + degree_num - 1

def triad_in_key(root: int) -> list[int]:
    return [root, (root + 2) % 8, (root + 4) % 8]

def get_irrational_digits(irr_name, num_digits, base = 7) -> list[int]:
    mp.dps = num_digits + 5  # Set decimal places for mpmath
    match irr_name:
        case "pi":
            pi_str = convert_base(mp.pi, base, num_digits).split(".")[1]  # Only digits after the decimal point
            return [int(digit) + 1 for digit in pi_str[:num_digits]] # Add one since we one-indexed the scale degrees
        # Same pattern for other irrationals
        case "e":
            e_str = convert_base(mp.e, base, num_digits).split(".")[1]
            return [int(digit) + 1 for digit in e_str[:num_digits]]
        case "phi":
            phi_str = convert_base((1 + mp.sqrt(5)) / 2, base, num_digits).split(".")[1]
            return [int(digit) + 1 for digit in phi_str[:num_digits]]
        case _:
            raise ValueError("Unsupported irrational number. Please use 'pi' or 'e'.")

if __name__ == "__main__":
    main()