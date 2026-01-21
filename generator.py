import torch
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from utils.midi_utils import drum2midi_map
import mido
from mido import MidiFile, MidiTrack, Message

def load_trained_model(model_path):
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    model.eval()
    return model, tokenizer

def generate_text_sequence(model, tokenizer, input_text, num_sequences=2, max_length=333):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    
    results_str = ""
    for i in range(num_sequences):
        inputs = tokenizer(input_text, return_tensors='pt').to(device)
        
        generated_ids = model.generate(
            inputs['input_ids'],
            max_length=max_length,
            temperature=0.75,
            top_k=50,
            do_sample=True,
            num_return_sequences=1
        )
        
        generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        results_str += generated_text[5:] + " |"
        
        sections = [section.strip() for section in generated_text.split('|')]
        pattern = r"^[a-zA-Z]{3}, \d\.\d{1,2}$"
        valid_sections = [section for section in sections if re.match(pattern, section)]
        
        input_text = " | ".join(valid_sections[-4:])
        print(input_text)
        inputs = tokenizer(input_text, return_tensors='pt').to(device)
    
    return results_str

def text_to_midi(results_str, output_path='melodia.mid'):
    notas = []
    for item in results_str.split(' | '):
        item = item.strip()
        if ',' in item:
            try:
                nota, duracion = item.split(', ')
                duracion = float(duracion.strip())
                if nota in drum2midi_map:
                    notas.append((nota, duracion))
                else:
                    print(f"Nota desconocida: {nota}")
            except ValueError:
                print(f"Error al convertir la duración: {item}")
        else:
            print(f"Formato incorrecto: {item}")
    
    # Crear archivo MIDI
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)
    
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
    
    for nota, duracion in notas:
        note = drum2midi_map[nota]
        track.append(Message('note_on', note=note, velocity=64, time=0, channel=9))
        track.append(Message('note_off', note=note, velocity=64, time=int(duracion * 480), channel=9))
    
    midi.save(output_path)
    print(f"Archivo MIDI creado: {output_path}")
    return output_path