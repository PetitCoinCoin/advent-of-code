import argparse

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from time import time

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--part", "-p",
        type=int,
        choices={1, 2},
        help="Set puzzle part"
    )
    args = parser.parse_args()
    if not args.part:
        parser.error("Which part are you solving?")
    return args

@dataclass
class Region:
    p: int
    a: int

def parse_input(raw: str, i: int) -> None:
    for r, char in enumerate(raw):
        data[complex(r, -i)] = char

def get_neighbours(pos: complex, char: str) -> tuple:
    different = set()
    identical = set()
    for d in (1, -1, 1j, -1j):
        if data.get(pos + d, ".") == char:
            identical.add(pos + d)
        else:
            different.add((pos + d, d))
    return different, identical

def get_regions(*, is_part_two: bool = False) -> list:
    seen = set()
    regions = []
    for position, plant in data.items():
        if position in seen:
            continue
        region = Region(0, 0)
        region_seen = set()
        region_queue = deque([position])
        fences = set()
        while region_queue:
            pos = region_queue.popleft()
            region_seen.add(pos)
            perimeter, neighbours = get_neighbours(pos, plant)
            if is_part_two:
                for p, d in perimeter:
                    for delta in (1, -1, 1j, -1j):
                        if delta not in (-d, d) and (p + delta, d) in fences:
                            break 
                    else:
                        region.p += 1
                    fences.add((p, d))
            else:
                region.p += len(perimeter)
            region.a += 1
            for n in neighbours:
                if n not in region_seen and n not in region_queue:
                    region_queue.append(n)
        regions.append(region)
        seen |= region_seen
    return regions

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        i = 0
        while line := file.readline():
            parse_input(line.strip(), i)
            i += 1
    print(sum((r.p * r.a) for r in get_regions(is_part_two=args.part == 2)))
    print(time() - t)
