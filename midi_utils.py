midi_drum_map = {
    35: "bdr",  36: "kck",  37: "stk",  38: "snr",  39: "clp",
    40: "esn",  41: "ltm",  42: "chh",  43: "ftm",  44: "phh",
    45: "mtm",  46: "ohh",  47: "lmt",  48: "hmt",  49: "cym",
    50: "htm",  51: "ryd",  52: "chn",  53: "rbl",  54: "tam",
    55: "spl",  56: "cbl",  57: "cy2",  58: "vib",  59: "ry2",
    60: "bng",  61: "bgl",  62: "mhc",  63: "ohc",  64: "lco",
    65: "htb",  66: "ltb",  67: "hag",  68: "lag",  69: "cab",
    70: "mar",  71: "swh",  72: "lwh",  73: "sgu",  74: "lgu",
    75: "clv",  76: "hwb",  77: "lwb",  78: "mcu",  79: "ocu",
    80: "mtr",  81: "otr"
}

drum2midi_map = {v: k for k, v in midi_drum_map.items()}

def midi_to_text_drums(midi_path):
    import pretty_midi
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    note_sequence = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            pitch = note.pitch
            if pitch in midi_drum_map:
                pitch = midi_drum_map[pitch]
            duration = round(note.end - note.start, 2)
            note_sequence.append(f'{pitch}, {duration}')
    return ' | '.join(note_sequence)