import subprocess
import sys
import os

def install_requirements():
    """Installiere fehlende Pakete automatisch"""
    packages = [
        'pyttsx3==2.90'
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
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', package])
                print(f"✅ {package_name} erfolgreich installiert")
            except subprocess.CalledProcessError:
                print(f"❌ Fehler bei Installation von {package_name}")
                sys.exit(1)
    
    print("\n✅ Alle Pakete sind bereit!\n")

if __name__ == "__main__":
    install_requirements()
    
    # Starte die GUI Version
    from jarvis_gui import JarvisGUI
    import tkinter as tk
    
    root = tk.Tk()
    app = JarvisGUI(root)
    root.mainloop()
