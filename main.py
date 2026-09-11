import subprocess
import sys
import os

def install_requirements():
    """Installiere fehlende Pakete automatisch"""
    packages = [
        'SpeechRecognition==3.10.0',
        'pyttsx3==2.90',
        'pyaudio==0.2.13'
    ]
    
    print("🔍 Prüfe ob alle Pakete installiert sind...")
    
    for package in packages:
        package_name = package.split('==')[0]
        try:
            __import__(package_name.lower().replace('-', '_'))
            print(f"✅ {package_name} ist installiert")
        except ImportError:
            print(f"⬇️  Installiere {package_name}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package_name} erfolgreich installiert")
            except subprocess.CalledProcessError:
                print(f"❌ Fehler bei Installation von {package_name}")
                sys.exit(1)
    
    print("\n✅ Alle Pakete sind bereit!\n")

if __name__ == "__main__":
    install_requirements()
    
    # Importiere jetzt die Hauptdatei
    from jarvis_main import JarvisAssistant
    
    jarvis = JarvisAssistant()
    jarvis.run()
