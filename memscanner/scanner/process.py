import subprocess
import sys
from typing import List, Tuple

def get_pid(process_name: str) -> int:
    try:
        pid = int(subprocess.check_output(["pgrep", "-n", process_name]).strip())
        return pid
    except subprocess.CalledProcessError:
        print(f"Prozess '{process_name}' nicht gefunden.")
        sys.exit(1)

def get_memory_regions(pid: int) -> List[Tuple[int,int]]:
    regions = []
    with open(f"/proc/{pid}/maps", "r") as maps:
        for line in maps:
            parts = line.split()
            addr, perms = parts[0], parts[1]
            if 'r' in perms and 'w' not in perms:
                start, end = (int(x,16) for x in addr.split('-'))
                regions.append((start, end))
    return regions
