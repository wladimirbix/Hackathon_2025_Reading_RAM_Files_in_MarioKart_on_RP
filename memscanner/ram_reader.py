import sys
import struct
import subprocess

def get_pid(process_name: str) -> int:
    try:
        pid = int(subprocess.check_output(["pgrep", "-n", process_name]).strip())
        return pid
    except subprocess.CalledProcessError:
        print(f"Prozess '{process_name}' nicht gefunden.")
        sys.exit(1)

def search_value_in_memory(pid: int, value: int):
    packed = struct.pack('<B', value)
    matches = []

    try:
        with open(f"/proc/{pid}/mem", "rb", 0) as mem, open(f"/proc/{pid}/maps") as maps:
            for line in maps:
                parts = line.split()
                addr_range = parts[0]
                perms = parts[1]

                if 'r' not in perms:
                    continue

                start, end = (int(x, 16) for x in addr_range.split('-'))
                mem.seek(start)
                try:
                    chunk = mem.read(end - start)
                except (OSError, IOError):
                    continue

                offset = 0
                while True:
                    idx = chunk.find(packed, offset)
                    if idx == -1:
                        break
                    matches.append(start + idx)
                    offset = idx + 1
    except Exception as e:
        print(f"Fehler beim Scannen: {e}")
        sys.exit(1)

    return matches

def main():
    if len(sys.argv) < 3:
        print("Usage: sudo python3 ram_reader.py <Prozessname> <Wert>")
        sys.exit(1)

    proc_name = sys.argv[1]
    value = int(sys.argv[2])

    pid = get_pid(proc_name)
    print(f"[+] PID gefunden: {pid}")

    addresses = search_value_in_memory(pid, value)

    if addresses:
        for addr in addresses:
            print(f"Gefunden bei Adresse: 0x{addr:08X}")
    else:
        print("Wert nicht im Speicher gefunden.")

if __name__ == "__main__":
    main()
