import os
import re
import struct
import time

def find_pid_by_name(name):
    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                with open(f"/proc/{pid}/comm", "r") as f:
                    if name in f.read():
                        return int(pid)
            except Exception:
                pass
    return None

def get_memory_regions(pid):
    regions = []
    with open(f"/proc/{pid}/maps", "r") as f:
        for line in f:
            if 'rw' in line.split()[1]:  # Nur beschreibbare Bereiche
                m = re.match(r"([0-9a-f]+)-([0-9a-f]+)", line)
                if m:
                    start = int(m.group(1), 16)
                    end = int(m.group(2), 16)
                    regions.append((start, end))
    return regions

def scan_memory(pid, regions, target_value, previous_hits=None):
    hits = []
    value_bytes = struct.pack("<i", target_value)  # int32 little-endian
    with open(f"/proc/{pid}/mem", "rb", 0) as mem_file:
        for start, end in regions:
            size = end - start
            try:
                mem_file.seek(start)
                chunk = mem_file.read(size)
            except:
                continue  # Kann passieren bei geschützten Bereichen

            for offset in range(0, len(chunk) - 4, 4):  # int32 Schritte
                addr = start + offset
                if previous_hits and addr not in previous_hits:
                    continue
                if chunk[offset:offset+4] == value_bytes:
                    hits.append(addr)
    return hits

def main():
    process_name = "retroarch"
    pid = find_pid_by_name(process_name)
    if pid is None:
        print("Prozess nicht gefunden.")
        return

    print(f"Zielprozess '{process_name}' hat PID {pid}")
    regions = get_memory_regions(pid)
    print(f"{len(regions)} speicherbare Speicherregionen gefunden.")

    hits = None

    while True:
        val = input("Suche nach Wert (int32), oder ENTER zum Beenden: ")
        if not val.strip():
            break
        try:
            search_value = int(val)
        except ValueError:
            print("Bitte eine gültige Ganzzahl eingeben.")
            continue

        hits = scan_memory(pid, regions, search_value, hits)
        print(f"{len(hits)} Adressen mit Wert {search_value} gefunden.")

        for addr in hits[:10]:  # Nur erste 10 anzeigen
            print(f"  0x{addr:X}")
        if len(hits) > 10:
            print("  ...")

        if len(hits) == 1:
            print(f"Zieladresse gefunden: 0x{hits[0]:X}")
            break
        elif len(hits) == 0:
            print("Keine passenden Adressen mehr gefunden.")
            break

if __name__ == "__main__":
    main()
