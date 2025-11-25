from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time

MODEL_PATH = "vosk-model-small-pl-0.22"
RATE = 16000
CHUNK = 4000

print("\nŁadowanie")

try:
    model = Model(MODEL_PATH)
    print("Model załadowany")
except:
    print(f"Nie znaleziono modelu")
    exit(1)

rec = KaldiRecognizer(model, RATE)
rec.SetWords(True)

p = pyaudio.PyAudio()

print("Przygotowanie mikrofonu")

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Mikrofon gotowy")

print("\nMów teraz")

start = None
result_text = ""

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)

        if rec.AcceptWaveform(data):
            if start is None:
                start = time.time()

            result = json.loads(rec.Result())
            text = result.get('text', '').strip()

            if text:
                result_text = text
                elapsed = time.time() - start

                print("Nagrano audio")
                print("\nRozpoznawanie...")

                print(f"Rozpoznany tekst: '{result_text}'")
                print(f"Czas rozpoznawania: {elapsed:.2f}s")

                break

except KeyboardInterrupt:
    print("\nPrzerwano test")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

print("\nTest zakończony")