import sys
import time
from memory_search import get_pid, scan_entire_memory, filter_candidates

def prompt_int(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")

def main():
    if len(sys.argv) < 2:
        print("Usage: sudo python3 main.py <Prozessname>")
        sys.exit(1)

    proc_name = sys.argv[1]
    pid = get_pid(proc_name)
    print(f"[+] Gefundene PID: {pid}")

    val = prompt_int("Erster Wert eingeben (z.B. 1): ")
    candidates = scan_entire_memory(pid, val)
    print(f"[+] Initial: {len(candidates)} Treffer gefunden.")

    while len(candidates) > 1:
        input("Position im Spiel ändern, dann ENTER drücken …")
        val = prompt_int("Neuer Wert: ")
        candidates = filter_candidates(pid, candidates, val)
        print(f"[+] {len(candidates)} Treffer verbleiben.")

    if candidates:
        print(f"[✓] Verdächtige Adresse gefunden: 0x{candidates[0]:08X}")
    else:
        print("[!] Keine Adresse gefunden.")

if __name__ == "__main__":
    main()
