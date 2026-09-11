import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pyttsx3
import datetime
import json
import os

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 JARVIS - Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        # Variablen
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.settings_file = "jarvis_settings.json"
        self.load_settings()
        
        # GUI erstellen
        self.create_gui()
        
    def load_settings(self):
        """Lade gespeicherte Einstellungen"""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                'volume': 0.9,
                'rate': 150,
                'voice_index': 0
            }
            self.save_settings()
    
    def save_settings(self):
        """Speichere Einstellungen"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)
    
    def create_gui(self):
        """Erstelle die Benutzeroberfläche"""
        # Header
        header = tk.Label(self.root, text="🤖 JARVIS - Voice Assistant", 
                         font=("Arial", 24, "bold"), bg="#1a1a1a", fg="#00ff00")
        header.pack(pady=20)
        
        # Chat-Box
        chat_frame = tk.Frame(self.root, bg="#1a1a1a")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(chat_frame, text="Konversation:", font=("Arial", 12, "bold"), 
                bg="#1a1a1a", fg="#00ff00").pack(anchor="w")
        
        self.chat_box = tk.Text(chat_frame, height=15, width=80, bg="#0a0a0a", 
                               fg="#00ff00", font=("Courier", 10))
        self.chat_box.pack(fill=tk.BOTH, expand=True, pady=10)
        self.chat_box.config(state=tk.DISABLED)
        
        # Input
        input_frame = tk.Frame(self.root, bg="#1a1a1a")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(input_frame, text="Du:", font=("Arial", 11, "bold"), 
                bg="#1a1a1a", fg="#00ff00").pack(side=tk.LEFT)
        
        self.input_field = tk.Entry(input_frame, font=("Arial", 11), bg="#0a0a0a", 
                                   fg="#00ff00", insertbackground="#00ff00")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#1a1a1a")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        send_btn = tk.Button(button_frame, text="📤 Senden", command=self.send_message,
                            bg="#00ff00", fg="#000000", font=("Arial", 11, "bold"),
                            padx=20, pady=5)
        send_btn.pack(side=tk.LEFT, padx=5)
        
        settings_btn = tk.Button(button_frame, text="⚙️ Einstellungen", command=self.open_settings,
                                bg="#00ff00", fg="#000000", font=("Arial", 11, "bold"),
                                padx=20, pady=5)
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="🗑️ Löschen", command=self.clear_chat,
                             bg="#00ff00", fg="#000000", font=("Arial", 11, "bold"),
                             padx=20, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Willkommensnachricht
        self.add_message("Jarvis", "Hallo! Ich bin Jarvis, dein persönlicher Assistent. "
                        "Wie kann ich dir heute helfen? 🎯")
        self.speak("Hallo! Ich bin Jarvis.")
    
    def add_message(self, sender, message):
        """Füge eine Nachricht zum Chat hinzu"""
        self.chat_box.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.chat_box.insert(tk.END, f"\n[{timestamp}] {sender}: {message}\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)
    
    def send_message(self):
        """Sende eine Nachricht"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        self.add_message("Du", message)
        
        # Verarbeite in neuem Thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Verarbeite die Nachricht"""
        response = self.handle_command(message.lower())
        self.add_message("Jarvis", response)
        self.speak(response)
    
    def handle_command(self, text):
        """Verarbeite Befehle"""
        # Uhrzeit
        if any(word in text for word in ["uhrzeit", "zeit", "wie spät", "spät", "uhr"]):
            now = datetime.datetime.now()
            return f"Es ist {now.strftime('%H:%M')} Uhr"
        
        # Datum
        elif any(word in text for word in ["tag", "datum", "heute", "welcher tag"]):
            now = datetime.datetime.now()
            weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
            day_name = weekdays[now.weekday()]
            return f"Heute ist {day_name}, der {now.strftime('%d.%m.%Y')}"
        
        # Begrüßung
        elif any(word in text for word in ["hallo", "hi", "hey", "moin"]):
            return "Hallo! Schön, dich zu sehen! 👋"
        
        # Hilfe
        elif any(word in text for word in ["hilfe", "was kannst", "funktionen", "befehle"]):
            return "Ich kann dir helfen mit: Uhrzeit sagen, Datum anzeigen, Rechnen und einfach mit dir reden! 💬"
        
        # Name
        elif any(word in text for word in ["wie heißt", "wer bist", "dein name"]):
            return "Ich bin Jarvis, dein intelligenter Sprachassistent! 🤖"
        
        # Gefühl
        elif "wie geht" in text:
            return "Mir geht es ausgezeichnet! Danke der Nachfrage. Wie kann ich dir helfen?"
        
        # Dank
        elif "danke" in text or "vielen dank" in text:
            return "Sehr gerne! Ich helfe immer gern. 😊"
        
        # Rechnen
        elif "rechne" in text or "plus" in text or "minus" in text:
            try:
                # Versuche zu berechnen
                result = eval(text.replace("rechne", "").replace("plus", "+").replace("minus", "-"))
                return f"Das Ergebnis ist: {result}"
            except:
                return "Entschuldigung, ich konnte das nicht berechnen. 🤔"
        
        # Standard
        else:
            return f"Das ist interessant! Du sagtest: '{text}'. Wie kann ich dir weiterhelfen?"
    
    def speak(self, text):
        """Spreche den Text aus"""
        if self.is_speaking:
            return
        
        self.is_speaking = True
        
        def speak_thread():
            try:
                self.engine.setProperty('rate', self.settings['rate'])
                self.engine.setProperty('volume', self.settings['volume'])
                voices = self.engine.getProperty('voices')
                if self.settings['voice_index'] < len(voices):
                    self.engine.setProperty('voice', voices[self.settings['voice_index']].id)
                
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Sprachfehler: {e}")
            finally:
                self.is_speaking = False
        
        threading.Thread(target=speak_thread, daemon=True).start()
    
    def open_settings(self):
        """Öffne Einstellungen"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Einstellungen")
        settings_window.geometry("400x300")
        settings_window.configure(bg="#1a1a1a")
        
        # Lautstärke
        tk.Label(settings_window, text="🔊 Lautstärke:", font=("Arial", 11, "bold"),
                bg="#1a1a1a", fg="#00ff00").pack(pady=10)
        
        volume_var = tk.DoubleVar(value=self.settings['volume'])
        volume_slider = tk.Scale(settings_window, from_=0, to=1, resolution=0.1, 
                                orient=tk.HORIZONTAL, bg="#0a0a0a", fg="#00ff00",
                                variable=volume_var, length=300)
        volume_slider.pack(padx=20, fill=tk.X)
        
        # Geschwindigkeit
        tk.Label(settings_window, text="⚡ Sprechgeschwindigkeit:", font=("Arial", 11, "bold"),
                bg="#1a1a1a", fg="#00ff00").pack(pady=10)
        
        rate_var = tk.IntVar(value=self.settings['rate'])
        rate_slider = tk.Scale(settings_window, from_=50, to=300, orient=tk.HORIZONTAL,
                              bg="#0a0a0a", fg="#00ff00", variable=rate_var, length=300)
        rate_slider.pack(padx=20, fill=tk.X)
        
        # Stimme
        tk.Label(settings_window, text="👤 Stimme:", font=("Arial", 11, "bold"),
                bg="#1a1a1a", fg="#00ff00").pack(pady=10)
        
        voices = self.engine.getProperty('voices')
        voice_options = [f"Stimme {i+1}" for i in range(len(voices))]
        voice_var = tk.IntVar(value=self.settings['voice_index'])
        voice_combo = ttk.Combobox(settings_window, values=voice_options, 
                                  state="readonly", textvariable=voice_var)
        voice_combo.pack(padx=20, fill=tk.X)
        
        # Speichern
        def save():
            self.settings['volume'] = volume_var.get()
            self.settings['rate'] = rate_var.get()
            self.settings['voice_index'] = voice_var.get()
            self.save_settings()
            self.speak("Einstellungen gespeichert!")
            settings_window.destroy()
        
        save_btn = tk.Button(settings_window, text="💾 Speichern", command=save,
                            bg="#00ff00", fg="#000000", font=("Arial", 11, "bold"))
        save_btn.pack(pady=20)
    
    def clear_chat(self):
        """Lösche den Chat"""
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.delete(1.0, tk.END)
        self.chat_box.config(state=tk.DISABLED)
        self.add_message("Jarvis", "Chat gelöscht! 🗑️")

if __name__ == "__main__":
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()
