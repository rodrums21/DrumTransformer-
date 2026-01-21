import os

def process_midi_files(folder_path, output_file='melodias_para_entrenamiento.txt'):
    from utils.midi_utils import midi_to_text_drums
    
    midi_files = [f for f in os.listdir(folder_path) if f.endswith('.mid')]
    windows = []
    
    for midi_file in midi_files:
        midi_path = os.path.join(folder_path, midi_file)
        text = midi_to_text_drums(midi_path)
        
        window_size = 500
        start = 0
        
        while start < len(text):
            end = start + window_size
            if end < len(text):
                end = text.rfind('|', start, end) + 1
            if end == 0:
                end = start + window_size
            window = text[start:end]
            if window and window[0] == ' ':
                window = window[1:]
            windows.append(window)
            start = end
            windows.append('\n')
    
    windows_val = windows[int(len(windows) * 0.8):]
    windows_tr = windows[0:int(len(windows) * 0.8)]
    
    with open(output_file, 'w') as file:
        file.write(''.join(windows_tr))
    
    print(f"Procesados {len(midi_files)} archivos MIDI y guardados en {output_file}.")
    return windows_tr, windows_val