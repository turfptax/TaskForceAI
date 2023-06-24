# voice_assistant.py
import pyttsx3
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
from colorama import init, Cursor
init()
import sys

keyphrase = "question"
model_path = "../vosk-model-small"

def clear_line():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\033[F")  # Move the cursor one line up

def recognize_speech_vosk(model_path, keyphrase=keyphrase):
    last_partial = ''
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
            sys.stdout.write(f"still-talking-deteced:{partial_result['partial']}\r")
            sys.stdout.flush()

def text_to_speech(text, lang="en-gb"):
    engine = pyttsx3.init()
    engine.say(text)
    engine.startLoop(False)
    result = ''
    while True:
        if 'stop' in result:
            engine.stop()
            break
        if not engine.isBusy():
            break
        engine.iterate()
    engine.endLoop()

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def wait_for_keyphrase(model_path, keyphrase=keyphrase):
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
            sys.stdout.write(f"still-talking-deteced:{partial_result['partial']}\r")
            sys.stdout.flush()

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
