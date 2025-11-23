import argparse
import math

from heapq import heappop, heappush
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

DIR_TO_COMPLEX = {
    "E": 1,
    "N": 1j,
    "W": -1,
    "S": -1j,
}

DIR_TO_NEXT = {
    "E": ("N", "S"),
    "N": ("W", "E"),
    "W": ("S", "N"),
    "S": ("E", "W"),
}

def parse_input(raw: str, i: int) -> None | complex:
    start = None
    for r, char in enumerate(raw):
        data[complex(r, -i)] = char
        if char == "S":
            start = complex(r, -i)
    return start

def maze(*, is_part_two: bool) -> int:
    best_path = math.inf
    seats = []
    seen = {}
    direction = "E"
    queue = []
    heappush(queue, (0, start.real, start.imag, direction, []))
    while queue:
        # path saving considerably slows down part 1, but meh.
        dist, r, i, d_str, path = heappop(queue)
        if dist > best_path:
            return len(set(seats)) + 1
        d = DIR_TO_COMPLEX[d_str]
        pos = complex(r, i)
        if data[pos] == "E":
            if not is_part_two:
                return dist
            best_path = dist
            seats.extend(path)
            continue
        seen[(d_str, pos)] = True
        new_path = path + [(r, i)]
        # forward
        forward = pos + d
        if data[forward] != "#" and (d_str, forward) not in seen:
            heappush(queue, (dist + 1, forward.real, forward.imag, d_str, new_path))
        # right and left
        for rot_str in DIR_TO_NEXT[d_str]:
            rot = DIR_TO_COMPLEX[rot_str]
            rotated = pos + rot
            if data[rotated] != "#" and (d_str, rotated) not in seen:
                    heappush(queue, (dist + 1001, rotated.real, rotated.imag, rot_str, new_path))
    return 0  


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    start = None
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        i = 0
        while line := file.readline():
            s = parse_input(line.strip(), i)
            start = start or s
            i += 1
    print(maze(is_part_two=args.part == 2))
    print(time() - t)
