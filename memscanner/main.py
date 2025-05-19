import os
import subprocess
from memory_search import search_memory_value  # Importiere die Funktion zum Suchen im Speicher

def main():
    # Schritt 1: Führe `cat /proc/7224/maps > ram_adresses.txt` aus
    print("Speicherbereiche von RetroArch extrahieren...")
    subprocess.run("cat /proc/7224/maps > ram_adresses.txt", shell=True, check=True)
    
    # Schritt 2: Öffne die Textdatei und lies die Adressen
    with open('ram_adresses.txt', 'r') as file:
        addresses = [line.split()[0] for line in file.readlines()]
    
    # Schritt 3: Beginne die Iterationen
    while True:
        # Schritt 3a: Frage nach dem Wert, nach dem gesucht werden soll
        search_value = input("Bitte gib den Wert ein, nach dem du suchen möchtest (z.B. '1'): ")
        try:
            search_value = int(search_value)  # Versuche, den Wert in eine Zahl umzuwandeln
        except ValueError:
            print("Ungültiger Wert! Bitte gib eine Zahl ein.")
            continue  # Wenn der Wert nicht eine Zahl ist, wiederhole die Eingabe

        # Schritt 3b: Durchsuche jede Adresse nach dem Wert
        print(f"Suche nach Wert {search_value} in den Adressen...")
        results = []
        for idx, address in enumerate(addresses):
            # Konvertiere die Adresse von Hex (z.B. 00400000) in eine Ganzzahl
            address_int = int(address.split('-')[0], 16)
            
            # Prüfe den Wert an dieser Adresse (hier wird die Funktion aus memory_search verwendet)
            if search_memory_value(address_int, search_value):
                results.append(address)
            
            # Zeige den Fortschritt in der Konsole an
            if (idx + 1) % 100 == 0:  # Alle 100 Adressen anzeigen
                print(f"Prüfe Adresse {idx + 1}/{len(addresses)}...")
        
        # Schritt 3c: Ergebnisse anzeigen
        if results:
            print(f"Gefundene Adressen mit Wert {search_value}:")
            for result in results:
                print(result)
        else:
            print(f"Keine Adressen mit Wert {search_value} gefunden.")
        
        # Schritt 3d: Frage, ob eine neue Iteration gestartet werden soll
        repeat = input("Möchtest du mit einem neuen Wert weitermachen? (y/n): ")
        if repeat.lower() != 'y':
            print("Beende das Programm.")
            break

if __name__ == "__main__":
    main()
