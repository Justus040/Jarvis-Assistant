import pyttsx3
import datetime

class JarvisAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_tts()
        self.running = True

    def setup_tts(self):
        """Richte Text-to-Speech ein"""
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
    def listen(self):
        """Höre auf Text-Input"""
        try:
            print("\n🎤 Was möchtest du sagen? (oder 'stopp' zum Beenden)")
            text = input("Du: ").strip()
            return text.lower() if text else None
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

    def get_date(self):
        """Gebe das aktuelle Datum aus"""
        now = datetime.datetime.now()
        weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        day_name = weekdays[now.weekday()]
        return f"Heute ist {day_name}, der {now.strftime('%d.%m.%Y')}"

    def handle_command(self, text):
        """Verarbeite Befehle"""
        # Uhrzeit
        if any(word in text for word in ["uhrzeit", "zeit", "wie spät", "spät", "uhr"]):
            return self.get_time()
        
        # Datum
        elif any(word in text for word in ["tag", "datum", "heute", "welcher tag"]):
            return self.get_date()
        
        # Begrüßung
        elif any(word in text for word in ["hallo", "hi", "hey", "moin"]):
            return "Hallo! Ich bin Jarvis, dein persönlicher Assistent. Wie kann ich dir helfen?"
        
        # Hilfe
        elif any(word in text for word in ["hilfe", "was kannst", "funktionen", "befehle"]):
            return "Ich kann dir die Uhrzeit sagen, das Datum anzeigen und mit dir reden. Frag mich nach: 'uhrzeit', 'datum', oder sag einfach hallo!"
        
        # Name
        elif any(word in text for word in ["wie heißt", "wer bist", "dein name"]):
            return "Ich bin Jarvis, dein sprachgesteuerter Assistent. Schön dich kennenzulernen!"
        
        # Alltägliches
        elif "wie geht" in text:
            return "Mir geht es großartig! Danke der Nachfrage. Wie kann ich dir heute helfen?"
        
        elif "danke" in text or "vielen dank" in text:
            return "Sehr gerne! Ich helfe immer gern."
        
        else:
            return f"Du hast gesagt: '{text}'. Das ist interessant! Wie kann ich dir weiterhelfen?"

    def run(self):
        """Starte den Hauptloop"""
        print("=" * 50)
        print("🤖 JARVIS VOICE ASSISTANT 🤖")
        print("=" * 50)
        self.speak("Hallo, ich bin Jarvis. Wie kann ich dir helfen?")
        
        while self.running:
            text = self.listen()
            if text:
                if any(word in text for word in ["stopp", "beende", "exit", "quit", "tschüss", "auf wiedersehen"]):
                    self.speak("Auf Wiedersehen! Bis bald!")
                    self.running = False
                else:
                    response = self.handle_command(text)
                    if response:
                        self.speak(response)
        
        print("\n👋 Jarvis beendet. Auf Wiedersehen!")

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
