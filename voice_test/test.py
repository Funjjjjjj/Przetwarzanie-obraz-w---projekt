import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import wave
import json
import time
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
TEMP_FILE = "temp_comparison.wav"
VOSK_MODEL_PATH = "vosk-model-small-pl-0.22"

print(f"\nNagrywanie przez {RECORD_SECONDS} sekund")
input("\nNaciśnij ENTER aby rozpocząć")

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("\nMów teraz")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("\nNagranie zakończone")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(TEMP_FILE, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("TEST SPEECH RECOGNITION MIKROFON")

try:
    recognizer = sr.Recognizer()

    with sr.AudioFile(TEMP_FILE) as source:
        audio = recognizer.record(source)

    print("\nRozpoznawanie...")
    start = time.time()
    text_google = recognizer.recognize_google(audio, language="pl-PL")
    elapsed_google = time.time() - start

    print(f"Rozpoznany tekst: '{text_google}'")
    print(f"Czas rozpoznawania: {elapsed_google:.2f}s")

except sr.RequestError as e:
    print(f"\nBłąd API: {e}")
except Exception as e:
    print(f"\nBłąd: {e}")

print("\nTest zakończony")

print("TEST VOSK (OFFLINE)")
try:
    if not os.path.exists(VOSK_MODEL_PATH):
        print(f"\nModel nie znaleziony: {VOSK_MODEL_PATH}")
    else:
        model = Model(VOSK_MODEL_PATH)

        wf = wave.open(TEMP_FILE, "rb")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        print("\nRozpoznawanie...")
        start = time.time()
        result_text = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                result_text += result.get('text', '') + " "

        final_result = json.loads(rec.FinalResult())
        result_text += final_result.get('text', '')

        elapsed_vosk = time.time() - start
        text_vosk = result_text.strip()

        print(f"Rozpoznany tekst: '{text_vosk}'")
        print(f"Czas rozpoznawania: {elapsed_vosk:.2f}s")

        wf.close()

except Exception as e:
    print(f"\nBłąd: {e}")

print("\nTest zakończony")

os.remove(TEMP_FILE)
