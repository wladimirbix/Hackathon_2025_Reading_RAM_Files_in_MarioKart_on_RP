import sys
import time
from scanner.process import get_pid, get_memory_regions
from scanner.memory import initial_scan, filter_scan
from scanner.utils import prompt_int

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 main.py <Prozessname> <byte|word>")
        sys.exit(1)

    proc_name = sys.argv[1]
    mode = sys.argv[2].lower()
    size = 1 if mode == 'byte' else 4

    pid = get_pid(proc_name)
    print(f"[+] Gefundene PID: {pid}")
    regions = get_memory_regions(pid)

    val = prompt_int("Erster Wert eingeben (z.B. 1): ")
    candidates = initial_scan(pid, regions, val, size)
    print(f"[+] Initial: {len(candidates)} Treffer gefunden.")

    while len(candidates) > 1:
        input("Position im Spiel ändern, dann ENTER drücken …")
        val = prompt_int("Neuer Wert: ")
        candidates = filter_scan(pid, candidates, val, size)
        print(f"[+] {len(candidates)} Treffer verbleiben.")

    if candidates:
        print(f"[✓] Verdächtige Adresse gefunden: 0x{candidates[0]:08X}")
    else:
        print("[!] Keine Adresse gefunden.")

if __name__ == "__main__":
    main()
