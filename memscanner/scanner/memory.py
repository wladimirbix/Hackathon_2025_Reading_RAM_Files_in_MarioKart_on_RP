import struct
from typing import List

def scan_region(pid: int, start: int, end: int, value: int, size: int = 1) -> List[int]:
    matches = []
    with open(f"/proc/{pid}/mem", "rb", 0) as mem:
        mem.seek(start)
        length = end - start
        chunk = mem.read(length)
        packed = struct.pack('<I' if size==4 else '<B', value)
        offset = 0
        while True:
            idx = chunk.find(packed, offset)
            if idx == -1:
                break
            matches.append(start + idx)
            offset = idx + 1
    return matches

def initial_scan(pid: int, regions: List[tuple], value: int, size: int = 1) -> List[int]:
    results = []
    for (s, e) in regions:
        results += scan_region(pid, s, e, value, size)
    return results

def filter_scan(pid: int, candidates: List[int], new_value: int, size: int = 1) -> List[int]:
    packed = struct.pack('<I' if size==4 else '<B', new_value)
    new_hits = []
    with open(f"/proc/{pid}/mem", "rb", 0) as mem:
        for addr in candidates:
            mem.seek(addr)
            data = mem.read(size)
            if data == packed:
                new_hits.append(addr)
    return new_hits
