import os

def midi_to_wav(midi_file_path, wav_file_path='/content/melodia.wav'):
    os.system(f"fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 {midi_file_path} -F {wav_file_path} -r 44100 -g{2.5}")
    print(f"Archivo WAV generado en: {wav_file_path}")
    return wav_file_path

def install_audio_dependencies():
    import subprocess
    subprocess.run(["apt-get", "install", "-y", "fluidsynth"])
    subprocess.run(["pip", "install", "pydub", "pygame"])
    subprocess.run(["apt-get", "install", "-y", "ffmpeg"])
    subprocess.run(["apt-get", "install", "-y", "timidity"])