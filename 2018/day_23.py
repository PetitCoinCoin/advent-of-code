import argparse
import math
import re

from dataclasses import dataclass
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

@dataclass
class Nano:
    x: int
    y: int
    z: int
    r: int

def distance(n1: Nano, n2: Nano = Nano(0, 0, 0, 0)) -> int:
    return abs(n2.x - n1.x) + abs(n2.y - n1.y) + abs(n2.z - n1.z)

def find_distance() -> int:
    queue = []
    for nano in data:
        heappush(queue, (distance(nano) - nano.r, 1))
        heappush(queue, (distance(nano) + nano.r, -1))
    counter = 0
    min_dist = math.inf
    max_counter = 0
    while queue:
        dist, c = heappop(queue)
        counter += c
        if counter > max_counter:
            max_counter = counter
            min_dist = abs(dist)
        elif counter == max_counter and abs(dist) <= min_dist:
            min_dist = abs(dist)
    return min_dist


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    pattern = r"pos=<(\-?\d+),(\-?\d+),(\-?\d+)>, r=(\-?\d+)"
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [Nano(*map(int, parsed)) for parsed in re.findall(pattern, file.read())]
    if args.part == 1:
        strongest_radius = max(nano.r for nano in data)
        strongest = next((nano for nano in data if nano.r == strongest_radius))
        print(len([nano for nano in data if distance(nano, strongest) <= strongest_radius]))
    else:
        print(find_distance())
    print(time() - t)
