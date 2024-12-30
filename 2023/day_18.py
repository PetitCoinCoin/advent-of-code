import argparse

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
class Cubicle:
    i: int
    j: int
    value: str
    color: str

DIRECTION_DELTA = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}

INT_TO_DIR = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}

def format_input(entry: str) -> tuple:
    values = entry.split(" ")
    return (values[0], int(values[1]), values[2][1:-1])

def format_input_2(entry: str) -> tuple:
    values = entry.split(" ")
    return (INT_TO_DIR[values[2][-2]], int(values[2][2:-2], base=16))

def get_position(last: Cubicle, direction: str) -> tuple:
    return last.i + DIRECTION_DELTA[direction][0], last.j + DIRECTION_DELTA[direction][1]

def get_position_2(last: tuple, direction: str, factor: int) -> tuple:
    return last[0] + factor * DIRECTION_DELTA[direction][0], last[1] + factor * DIRECTION_DELTA[direction][1]

def build_walls(instruction: tuple, last: Cubicle, walls: dict) -> Cubicle:
    direction, steps, color = instruction
    cubicle = last
    k = 0
    while k < steps:
        i, j = get_position(cubicle, direction)
        cubicle = Cubicle(i, j, "#", color)
        walls[(i, j)] = cubicle
        k += 1
    return cubicle

def build_corners(instruction: tuple, last: tuple, corners: list) -> tuple:
    direction, steps = instruction
    i, j = get_position_2(last, direction, steps)
    if (i, j) != (0, 0):
        corners.append((i, j))
    return i, j

def area(corners: list) -> int:
    area = 0
    for i in range(len(corners)):
        j = (i + 1) % len(corners)
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    return abs(area) // 2

def populate_cubicles(walls: dict, min_i: int, max_i: int, min_j: int, max_j: int) -> list:
    result = []
    for i in range(max_i - min_i + 1):
        result.append([])
        inside = False
        for j in range(max_j - min_j + 1):
            if walls.get((i + min_i, j + min_j)):
                result[i].append("#")
                if i > 0 and walls.get((i + min_i - 1, j + min_j)):
                    inside = not inside
            else:
                result[i].append("#" if inside else ".")
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    func = format_input if args.part == 1 else format_input_2
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [func(row) for row in file.read().splitlines()]
    if args.part == 1:
        start = Cubicle(0, 0, "#", "")
        walls = {(0, 0): start}
        last_wall = start
        for instruction in data:
            last_wall = build_walls(instruction, last_wall, walls)
        min_i = min((wall[0] for wall in walls.keys()))
        max_i = max((wall[0] for wall in walls.keys()))
        min_j = min((wall[1] for wall in walls.keys()))
        max_j = max((wall[1] for wall in walls.keys()))
        print(len([
            x for row in populate_cubicles(walls, min_i, max_i, min_j, max_j)
            for x in row
            if x == "#"
        ]))
    else:
        start = (0, 0)
        corners = [start]
        last_corner = start
        total_walls = 0
        for instruction in data:
            last_corner = build_corners(instruction, last_corner, corners)
            total_walls += instruction[1]  # steps
        print( area(corners) + total_walls // 2 + 1)
    print(time() - t)

