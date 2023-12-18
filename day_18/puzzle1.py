from dataclasses import dataclass
from pathlib import Path

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

def format_input(entry: str) -> tuple:
    values = entry.split(" ")
    return (values[0], int(values[1]), values[2][1:-1])

def get_position(last: Cubicle, direction: str) -> tuple:
    return last.i + DIRECTION_DELTA[direction][0], last.j + DIRECTION_DELTA[direction][1]

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
    with Path("day_18/input.txt").open("r") as file:
        data = [format_input(row) for row in file.read().splitlines()]
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
