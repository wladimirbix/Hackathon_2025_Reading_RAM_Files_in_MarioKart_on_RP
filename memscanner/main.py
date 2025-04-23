import sys
from memory_search import get_pid, get_memory_regions, initial_scan, filter_scan

# Eingabeaufforderung für die Zahl (für die erste Eingabe oder für den neuen Wert)
def prompt_int(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <Prozessname>")
        sys.exit(1)

    proc_name = sys.argv[1]

    pid = get_pid(proc_name)
    print(f"[+] Gefundene PID: {pid}")
    regions = get_memory_regions(pid)

    val = prompt_int("Erster Wert eingeben (z.B. 2): ")
    candidates = initial_scan(pid, regions, val)
    print(f"[+] Initial: {len(candidates)} Treffer gefunden.")

    # Schleife für die weiteren Scans
    while len(candidates) > 1:
        input("Position im Spiel ändern, dann ENTER drücken …")
        val = prompt_int("Neuer Wert: ")
        candidates = filter_scan(pid, candidates, val)
        print(f"[+] {len(candidates)} Treffer verbleiben.")

    if candidates:
        print(f"[✓] Verdächtige Adresse gefunden: 0x{candidates[0]:08X}")
    else:
        print("[!] Keine Adresse gefunden.")

if __name__ == "__main__":
    main()
