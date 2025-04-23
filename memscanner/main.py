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
    
    # Schritt 3: Durchsuche jede Adresse nach dem Wert 1
    print("Überprüfe Speicheradressen auf Wert '1'...")
    results = []
    for address in addresses:
        # Konvertiere die Adresse von Hex (z.B. 00400000) in eine Ganzzahl
        address_int = int(address.split('-')[0], 16)
        
        # Prüfe den Wert an dieser Adresse (hier wird die Funktion aus memory_search verwendet)
        if search_memory_value(address_int, 1):  # Hier wird nach Wert "1" gesucht
            results.append(address)
    
    # Ausgabe der gefundenen Adressen
    if results:
        print("Gefundene Adressen mit Wert 1:")
        for result in results:
            print(result)
    else:
        print("Keine Adressen mit Wert 1 gefunden.")

if __name__ == "__main__":
    main()
