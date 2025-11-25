import speech_recognition as sr
import time

recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0

print("\nPrzygotowanie mikrofonu")

with sr.Microphone() as source:
    print("Mikrofon gotowy")

    print("\nMów teraz")

    try:
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        print("Nagrano audio")

        print("\nRozpoznawanie...")
        start = time.time()
        text = recognizer.recognize_google(audio, language="pl-PL")
        elapsed = time.time() - start

        print(f"Rozpoznany tekst: '{text}'")
        print(f"Czas rozpoznawania: {elapsed:.2f}s")

    except sr.WaitTimeoutError:
        print("\nNie wykryto mowy")
    except sr.RequestError as e:
        print(f"\nBłąd API: {e}")

print("\nTest zakończony")