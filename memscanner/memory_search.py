import subprocess
import struct
import sys

def get_pid(process_name: str) -> int:
    try:
        pid = int(subprocess.check_output(["pgrep", "-n", process_name]).strip())
        return pid
    except subprocess.CalledProcessError:
        print(f"Prozess '{process_name}' nicht gefunden.")
        sys.exit(1)

def scan_entire_memory(pid: int, value: int) -> list:
    candidates = []
    packed = struct.pack('<B', value)

    try:
        with open(f"/proc/{pid}/mem", "rb", 0) as mem, open(f"/proc/{pid}/maps") as maps:
            for line in maps:
                parts = line.split()
                addr_range = parts[0]
                perms = parts[1]

                if 'r' not in perms:
                    continue  # Nur lesbare Bereiche

                start, end = (int(x, 16) for x in addr_range.split('-'))
                mem.seek(start)
                try:
                    chunk = mem.read(end - start)
                except (OSError, IOError):
                    continue  # Bereich kann nicht gelesen werden

                offset = 0
                while True:
                    idx = chunk.find(packed, offset)
                    if idx == -1:
                        break
                    candidates.append(start + idx)
                    offset = idx + 1
    except Exception as e:
        print(f"Fehler beim Scannen des Speichers: {e}")
        sys.exit(1)

    return candidates

def filter_candidates(pid: int, candidates: list, new_value: int) -> list:
    packed = struct.pack('<B', new_value)
    new_hits = []

    try:
        with open(f"/proc/{pid}/mem", "rb", 0) as mem:
            for addr in candidates:
                try:
                    mem.seek(addr)
                    data = mem.read(1)
                    if data == packed:
                        new_hits.append(addr)
                except (OSError, IOError):
                    continue
    except Exception as e:
        print(f"Fehler beim Filtern der Adressen: {e}")
        sys.exit(1)

    return new_hits
