import argparse
import math

from collections import deque
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

DELTAS = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

def walk(regex: str) -> dict:
    positions = deque([(0, 0)])
    doors = {(0, 0): 0}
    x, y = 0, 0
    for char in regex:
        if char == "(":
            positions.append((x, y))
        elif char == ")":
            x, y = positions.pop()
        elif char == "|":
            x, y = positions[-1]
        else:
            prev_x, prev_y = x, y
            dx, dy = DELTAS[char]
            x += dx
            y += dy
            doors[(x, y)] = min(
                doors[(prev_x, prev_y)] + 1,
                doors.get((x, y), math.inf)
            )
    return doors

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip()[1: -1]
    door_count = walk(data)
    if args.part == 1:
        print(max(door_count.values()))
    else:
        print(len([x for x in door_count.values() if x >= 1000]))
    print(time() - t)
