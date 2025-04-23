import sys
import struct
import subprocess  # Hier wird subprocess benötigt, um die PID zu holen

def read_memory(pid, address, size):
    try:
        # Öffnet den Speicher des Prozesses
        with open(f"/proc/{pid}/mem", "rb") as mem:
            mem.seek(address)
            data = mem.read(size)  # Liest die angeforderte Anzahl an Bytes
            return data
    except Exception as e:
        print(f"Fehler beim Lesen der Adresse {hex(address)}: {e}")
        return None

def search_in_memory(pid, search_value, size):
    # Konvertiert den gesuchten Wert in Bytes
    packed_value = struct.pack('<B', search_value)  # Suche nach 1 Byte (unsigned char)
    addresses_found = []

    # Durchsucht den gesamten Speicherbereich des Prozesses
    with open(f"/proc/{pid}/maps", "r") as maps:
        for line in maps:
            parts = line.split()
            start, end = [int(x, 16) for x in parts[0].split('-')]
            
            # Sucht im jeweiligen Bereich nach dem Wert
            for addr in range(start, end, size):
                data = read_memory(pid, addr, size)
                if data and data == packed_value:
                    addresses_found.append(addr)
                    print(f"Gefunden bei Adresse: {hex(addr)}")  # Zeigt die Adresse an

    return addresses_found

def get_pid(process_name):
    try:
        pid = int(subprocess.check_output(["pgrep", "-n", process_name]).strip())
        return pid
    except subprocess.CalledProcessError:
        print(f"Prozess '{process_name}' nicht gefunden.")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 ram_reader.py <Prozessname> <Wert>")
        sys.exit(1)

    process_name = sys.argv[1]
    search_value = int(sys.argv[2])

    pid = get_pid(process_name)
    print(f"PID des Prozesses {process_name}: {pid}")

    print(f"Suche nach Wert {search_value} im RAM des Prozesses...")
    
    addresses = search_in_memory(pid, search_value, 1)  # 1 Byte pro Adresse
    if not addresses:
        print(f"Kein Treffer für Wert {search_value} gefunden.")
    else:
        print(f"Adressen mit Wert {search_value} gefunden: {addresses}")

if __name__ == "__main__":
    main()
