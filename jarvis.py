import speech_recognition as sr
import pyttsx3
import datetime
import os
from settings import Settings
from commands import CommandHandler

class JarvisAssistant:
    def __init__(self):
        self.settings = Settings()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.command_handler = CommandHandler(self.engine, self.settings)
        self.setup_tts()
        self.running = True

    def setup_tts(self):
        """Richte Text-to-Speech ein"""
        self.engine.setProperty('rate', self.settings.speech_rate)
        self.engine.setProperty('volume', self.settings.volume)
        
    def listen(self):
        """Höre auf Spracheinput"""
        try:
            with sr.Microphone(device_index=self.settings.mic_index) as source:
                print("🎤 Höre zu...")
                self.engine.say("Ich bin bereit")
                self.engine.runAndWait()
                
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language='de-DE')
                print(f"Du: {text}")
                return text.lower()
        except sr.UnknownValueError:
            self.speak("Entschuldigung, ich habe das nicht verstanden")
            return None
        except sr.RequestError:
            self.speak("Internet-Fehler beim Spracherkennung")
            return None
        except Exception as e:
            print(f"Fehler: {e}")
            return None

    def speak(self, text):
        """Spreche den Text aus"""
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

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
                    response = self.command_handler.handle(text)
                    if response:
                        self.speak(response)

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
