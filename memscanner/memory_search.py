import psutil
import os
import struct

# Funktion zum Abrufen des Prozesses
def get_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if name.lower() in proc.info['name'].lower():
            return proc
    return None

# Funktion zum Durchsuchen des Speichers nach einer Zahl
def search_memory_in_process(process_name, target_value):
    process = get_process_by_name(process_name)
    if not process:
        print(f"Prozess {process_name} nicht gefunden.")
        return []
    
    addresses = []
    try:
        pid = process.info['pid']
        # Der Pfad zum Speicherauszug des Prozesses
        mem_file_path = f"/proc/{pid}/mem"
        
        with open(mem_file_path, "rb") as mem_file:
            # Wir lesen den Speicherbereich in kleinen Teilen
            for address in range(0x10000000, 0x10010000, 4):  # Beispielbereich
                mem_file.seek(address)
                data = mem_file.read(4)
                if len(data) == 4:
                    value = struct.unpack('I', data)[0]  # 'I' steht für unsigned int
                    if value == target_value:
                        addresses.append(address)
    except Exception as e:
        print(f"Fehler beim Abrufen des Speichers: {e}")
    return addresses

# Funktion zum fortlaufenden Filtern von Adressen
def filter_addresses(addresses, target_value):
    filtered_addresses = []
    for address in addresses:
        # Hier würden wir erneut den Speicher lesen und nach der neuen Zahl suchen
        if search_memory_in_process("retroarch", target_value):
            filtered_addresses.append(address)
    return filtered_addresses

# Hauptfunktion zum Ausführen des gesamten Prozesses
def memory_search():
    all_addresses = []
    while True:
        try:
            target_value = int(input("Gib eine Zahl ein, um nach dieser zu suchen: "))
            new_addresses = search_memory_in_process("retroarch", target_value)
            all_addresses.extend(new_addresses)
            print(f"Gefundene Adressen: {new_addresses}")
            while len(all_addresses) > 1:
                target_value = int(input("Gib eine neue Zahl ein, um weiter zu filtern: "))
                all_addresses = filter_addresses(all_addresses, target_value)
                print(f"Gefilterte Adressen: {all_addresses}")
            if len(all_addresses) == 1:
                print(f"Die übriggebliebene Adresse ist: {all_addresses[0]}")
                break
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
