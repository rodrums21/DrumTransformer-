import os
from google.colab import drive
from data.prepare_dataset import process_midi_files
from train.train_model import train_model
from generate.generate_music import load_trained_model, generate_text_sequence, text_to_midi
from audio.audio_utils import midi_to_wav, install_audio_dependencies

def main():
    # Montar Google Drive (si estás en Colab)
    drive.mount('/content/drive')
    
    # 1. Procesar datos
    folder_path = '/content/drive/MyDrive/Proyecto Maestría/BaseSint/Normalizada_120'
    process_midi_files(folder_path)
    
    # 2. Entrenar modelo
    model_path = '/content/drive/MyDrive/Proyecto Maestría/500 - 9 eps/saved_model_digitpt2_9_500'
    model, tokenizer = train_model(model_path)
    
    # 3. Generar música
    model, tokenizer = load_trained_model(model_path)
    input_text = 'ftm, 0.2 | snr, 0.3 | snr, 0.2 | phh, 0.3'
    generated_text = generate_text_sequence(model, tokenizer, input_text)
    
    # 4. Convertir a MIDI
    midi_path = text_to_midi(generated_text)
    
    # 5. Instalar dependencias de audio y convertir a WAV
    install_audio_dependencies()
    wav_path = midi_to_wav(midi_path)
    
    print("¡Proceso completado!")
    print(f"MIDI generado: {midi_path}")
    print(f"Audio WAV generado: {wav_path}")

if __name__ == "__main__":
    main()