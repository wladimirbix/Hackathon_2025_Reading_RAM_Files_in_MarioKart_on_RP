import sys
import struct

def read_memory(pid: int, address: int, size: int = 1) -> int:
    try:
        with open(f"/proc/{pid}/mem", "rb", 0) as mem:
            mem.seek(address)
            data = mem.read(size)
            if size == 1:
                return struct.unpack('<B', data)[0]
            elif size == 4:
                return struct.unpack('<I', data)[0]
            else:
                raise ValueError("Unsupported size. Only 1 or 4 bytes supported.")
    except (OSError, IOError) as e:
        print(f"Fehler beim Lesen der Adresse 0x{address:08X}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: sudo python3 ram_reader.py <PID> <Adresse> [byte|word]")
        sys.exit(1)

    pid = int(sys.argv[1])
    address = int(sys.argv[2], 16)  # Adresse als Hexadezimal eingeben
    mode = sys.argv[3].lower() if len(sys.argv) > 3 else 'byte'
    size = 1 if mode == 'byte' else 4

    value = read_memory(pid, address, size)
    print(f"Wert an Adresse 0x{address:08X}: {value}")

if __name__ == "__main__":
    main()
