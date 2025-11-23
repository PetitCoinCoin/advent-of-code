import argparse
import re

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
class Point:
    x: int
    y: int
    vx: int
    vy: int

def parse_input(raw: str) -> Point:
    pattern = r"position=<(\s?\-?\d+,\s+\-?\d+)> velocity=<(\s?\-?\d+,\s+\-?\d+)>"
    position, velocity = re.findall(pattern, raw)[0]
    return Point(
        x=int(position.split(",")[0].strip()),
        y=int(position.split(",")[1].strip()),
        vx=int(velocity.split(",")[0].strip()),
        vy=int(velocity.split(",")[1].strip()),
    )

def delta_x(iteration: int) -> int:
    max_x = max(p.x + iteration * p.vx for p in data)
    min_x = min(p.x + iteration * p.vx for p in data)
    return max_x

def find_delay() -> int:
    min_delta = 10000000000000
    i = 0
    delta = delta_x(i) 
    while delta < min_delta:
        min_delta = delta
        i += 1
        delta = delta_x(i)
    return i - 1

def pretty_print(grid: dict, min_x: int, max_x:int, min_y: int, max_y: int) -> None:
    for y in range(min_y, max_y + 1):
        print("".join(grid.get((x, y), ".") for x in range(min_x, max_x + 1)))

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().split("\n")]
    delay = find_delay()
    if args.part == 1:
        max_x = max(p.x + delay * p.vx for p in data) + 1
        min_x = min(p.x + delay * p.vx for p in data) - 1
        max_y = max(p.y + delay * p.vy for p in data) + 1
        min_y = min(p.y + delay * p.vy for p in data) - 1
        points = {}
        for p in data:
            points[(p.x + delay * p.vx, p.y + delay * p.vy)] = "#"
        pretty_print(points, min_x, max_x, min_y, max_y)
    else:
        print(delay)
    print(time() - t)
