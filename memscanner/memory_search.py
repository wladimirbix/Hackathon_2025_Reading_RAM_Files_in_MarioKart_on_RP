import struct
import subprocess
import sys
from typing import List, Tuple

# Holen der Prozess-ID (PID) eines Prozesses anhand des Namens
def get_pid(process_name: str) -> int:
    try:
        pid = int(subprocess.check_output(["pgrep", "-n", process_name]).strip())
        return pid
    except subprocess.CalledProcessError:
        print(f"Prozess '{process_name}' nicht gefunden.")
        sys.exit(1)

# Holen der Speicherbereiche des Prozesses
def get_memory_regions(pid: int) -> List[Tuple[int, int]]:
    regions = []
    with open(f"/proc/{pid}/maps", "r") as maps:
        for line in maps:
            parts = line.split()
            addr, perms = parts[0], parts[1]
            if 'r' in perms and 'w' not in perms:  # Nur lesbare Bereiche ohne Schreibrechte
                start, end = (int(x, 16) for x in addr.split('-'))
                regions.append((start, end))
    return regions

# Durchsuchen eines Speicherbereichs nach einem bestimmten Wert
def scan_region(pid: int, start: int, end: int, value: int, size: int = 1) -> List[int]:
    matches = []
    with open(f"/proc/{pid}/mem", "rb", 0) as mem:
        mem.seek(start)
        length = end - start
        chunk = mem.read(length)
        packed = struct.pack('<I' if size == 4 else '<B', value)
        for i in range(len(chunk) - size + 1):  # Durchsuche den gesamten Chunk
            if chunk[i:i + size] == packed:  # Exakte Übereinstimmung
                matches.append(start + i)
    return matches

# Initialer Scan aller Speicherregionen nach einem Wert
def initial_scan(pid: int, regions: List[Tuple[int, int]], value: int) -> List[int]:
    size = 4 if value > 255 else 1  # Automatische Entscheidung (Byte für <= 255, Word für > 255)
    results = []
    for (s, e) in regions:
        results += scan_region(pid, s, e, value, size)
    return results

# Filtere die Kandidaten nach einem neuen Wert
def filter_scan(pid: int, candidates: List[int], new_value: int) -> List[int]:
    size = 4 if new_value > 255 else 1  # Automatische Entscheidung (Byte für <= 255, Word für > 255)
    packed = struct.pack('<I' if size == 4 else '<B', new_value)
    new_hits = []
    with open(f"/proc/{pid}/mem", "rb", 0) as mem:
        for addr in candidates:
            mem.seek(addr)
            data = mem.read(size)
            if data == packed:
                new_hits.append(addr)
    return new_hits
