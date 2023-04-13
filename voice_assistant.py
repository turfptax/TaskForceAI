# voice_assistant.py

import pygame
import wave
import json
from gtts import gTTS
from vosk import Model, KaldiRecognizer
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup
import json
import subprocess




def change_speed_and_pitch(input_file, output_file, speed_factor, pitch_factor):
    batch_file = "ffmpeg_run.bat"
    subprocess.run([batch_file, input_file, str(speed_factor), str(pitch_factor), output_file], check=True)

def recognize_speech_vosk(model_path, keyphrase="hey assistant"):
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("Listening...")
    while True:
        data = stream.read(8000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print(f"Recognized text: {result['text']}")
            if keyphrase.lower() in result['text'].lower():
                stream.stop_stream()
                stream.close()
                p.terminate()
                return result['text']
        else:
            partial_result = json.loads(recognizer.PartialResult())
            print(f"Partial: {partial_result['partial']}")

def text_to_speech(text, lang="en", filename="output.mp3"):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def wait_for_keyphrase(model_path, keyphrase="hey assistant"):
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("Listening for keyphrase...")
    while True:
        data = stream.read(8000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print(f"Recognized text: {result['text']}")
            if keyphrase.lower() in result['text'].lower():
                stream.stop_stream()
                stream.close()
                p.terminate()
                return True
        else:
            partial_result = json.loads(recognizer.PartialResult())
            print(f"Partial: {partial_result['partial']}")

def get_user_input(model_path):
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    print("Listening for user input...")
    while True:
        data = stream.read(8000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print(f"Recognized text: {result['text']}")
            stream.stop_stream()
            stream.close()
            p.terminate()
            return result['text']
        else:
            partial_result = json.loads(recognizer.PartialResult())
            print(f"Partial: {partial_result['partial']}")
