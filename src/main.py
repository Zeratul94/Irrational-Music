import mido
import time
from irrationals_in_bases import *

scale = 60
port = None
velocity = 64  # Medium velocity

def main():
    global scale
    scale = note_name_to_midi(input("What key should the song play in? (e.g., C, D#, F): ").strip().upper())
    digits = get_digits(input("What number should we listen to? ").strip().lower(),
                                   int(input("And for how many digits? ")),
                                   base=7)

    port_name = mido.get_output_names()[0]  # Select the first available MIDI output port
    
    beat_time = 0.5  # Duration in seconds
    
    print(f"{note_from_scale_degree(0)}")
    global port
    with mido.open_output(port_name) as port:
        last_triad =  None
        for digit in digits:
            triad = [note_from_scale_degree(chord_note) for chord_note in triad_in_key(int(digit), prev_triad=last_triad)]
            for note in triad:
                start_note(note)
            for i in range(4):
                start_note(note_from_scale_degree(digit + i))
                time.sleep(beat_time)
            for note in triad:
                end_note(note)
            
            last_triad = triad

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

# Convert a note name (e.g., C, D#, F) to its corresponding MIDI number.
def note_name_to_midi(note_name):
    note_names = ['C', 'ε', 'D', 'ε', 'E', 'F', 'ε', 'G', 'ε', 'A', 'ε', 'B']
    octave = 3  # Default octave
    if len(note_name) > 2 and note_name[-1].isdigit():
        octave = int(note_name[-1])
        note_name = note_name[:-1]
    if note_name[0] in note_names:
        note_index = note_names.index(note_name[0])
        base_note = 12 * (octave + 1) + note_index
        return(base_note + 1 if "#" in note_name else (base_note - 1 if "b" in note_name else base_note))
    else:
        raise ValueError(f"Invalid note name: " + note_name)

# Convert a scale degree to a MIDI note number based on the global scale variable.
def note_from_scale_degree(degree_num: int) -> int:
    global scale
    octaves, net_degree = divmod(degree_num - 1, 7)
    return (scale + octaves * 12 + ((net_degree * 2) if net_degree <= 2
                                    else 5 + (net_degree - 3) * 2))

def triad_in_key(root: int, prev_triad: list[int] = []) -> list[int]:
    notes_to_place = [root, (root + 2 - 1) % 7 + 1, (root + 4 - 1) % 7 + 1]  # 1-indexed scale degrees for root, third, fifth
    if prev_triad and len(prev_triad) == 3:
        old_notes = prev_triad[:]
        new_notes: list[int] = []
        distance_matrix: list[list[tuple[int, int]]] = [] # Each row is one desired note; each column is an old note; entries are (distance, best octave placement)
        for note in notes_to_place:
            distance_matrix.append([])
            candidates = [note + 7 * k for k in range(-2, 3)]  # Consider two octaves up and down
            for old_note in old_notes:
                nearest_candidate = min(candidates, key=lambda c: note_dist(note_from_scale_degree(c), old_note))
                distance_matrix[-1].append((note_dist(note_from_scale_degree(nearest_candidate), old_note), nearest_candidate))

        while len(distance_matrix) > 1:
            min_dist = float('inf')
            best_row_idx = -1
            best_col_idx = -1
            for row_idx, row in enumerate(distance_matrix):
                for col_idx, (dist, _) in enumerate(row):
                    if dist < min_dist:
                        min_dist = dist
                        best_row_idx = row_idx
                        best_col_idx = col_idx
            
            new_notes.append(distance_matrix[best_row_idx][best_col_idx][1])
            
            distance_matrix.pop(best_row_idx)
            for row in distance_matrix:
                row.pop(best_col_idx)
        
        if len(distance_matrix) == 1:
            new_notes.append(distance_matrix[0][0][1])
        return new_notes
    
    return notes_to_place

# Calculate the distance in semitones betweeen two scale degrees
def note_dist(note1: int, note2: int) -> int:
    return abs(note_from_scale_degree(note1) - note_from_scale_degree(note2))

def get_digits(num_str, num_digits, base = 7) -> list[int]:
    mp.dps = num_digits + 5  # Set decimal places for mpmath
    match num_str:
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
    
    if "ln" in num_str:
        arg = float(num_str[num_str.index("(")+1:num_str.index(")")])
        ln_str = convert_base(mp.ln(arg), base, num_digits).split(".")[1]
        return [int(digit) + 1 for digit in ln_str[:num_digits]]
    if "sqrt" in num_str:
        arg = float(num_str[num_str.index("(")+1:num_str.index(")")])
        sqrt_str = convert_base(mp.sqrt(arg), base, num_digits).split(".")[1]
        return [int(digit) + 1 for digit in sqrt_str[:num_digits]]
    if num_str.isnumeric():
        num = float(num_str)
        num_str_base = convert_base(num, base, num_digits).split(".")[1]
        return [int(digit) + 1 for digit in num_str_base[:num_digits]]
    raise ValueError(f"Unrecognized number string: {num_str}")


if __name__ == "__main__":
    main()