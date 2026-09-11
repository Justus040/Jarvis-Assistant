import pyttsx3
import datetime
import os
from google.cloud import speech_v1
import io

class JarvisAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_tts()
        self.client = speech_v1.SpeechClient()
        self.running = True

    def setup_tts(self):
        """Richte Text-to-Speech ein"""
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
    def listen(self):
        """Höre auf Spracheinput"""
        try:
            print("🎤 Höre zu...")
            self.speak("Ich bin bereit")
            
            # Einfache Alternative: Benutzer-Input
            text = input("Du: ")
            return text.lower()
        except Exception as e:
            print(f"Fehler: {e}")
            return None

    def speak(self, text):
        """Spreche den Text aus"""
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def get_time(self):
        """Gebe die aktuelle Uhrzeit aus"""
        now = datetime.datetime.now()
        return f"Es ist {now.strftime('%H:%M')} Uhr"

    def handle_command(self, text):
        """Verarbeite Befehle"""
        if "uhrzeit" in text or "zeit" in text or "wie spät" in text:
            return self.get_time()
        elif "tag" in text or "datum" in text:
            return f"Heute ist {datetime.datetime.now().strftime('%d.%m.%Y')}"
        elif "hallo" in text or "hi" in text:
            return "Hallo! Wie kann ich dir helfen?"
        elif "hilfe" in text:
            return "Ich kann dir die Uhrzeit sagen, das Datum anzeigen und mit dir reden. Frag mich nach der Zeit!"
        else:
            return f"Du hast gesagt: {text}"

    def run(self):
        """Starte den Hauptloop"""
        self.speak("Hallo, ich bin Jarvis. Wie kann ich dir helfen?")
        
        while self.running:
            text = self.listen()
            if text:
                if "stopp" in text or "beende" in text or "exit" in text:
                    self.speak("Auf Wiedersehen!")
                    self.running = False
                else:
                    response = self.handle_command(text)
                    if response:
                        self.speak(response)

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
