from pathlib import Path

INT_TO_DIR = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}
DIRECTION_DELTA = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}

def format_input(entry: str) -> tuple:
    values = entry.split(" ")
    return (INT_TO_DIR[values[2][-2]], int(values[2][2:-2], base=16))

def get_position(last: tuple, direction: str, factor: int) -> tuple:
    return last[0] + factor * DIRECTION_DELTA[direction][0], last[1] + factor * DIRECTION_DELTA[direction][1]

def build_corners(instruction: tuple, last: tuple, corners: list) -> tuple:
    direction, steps = instruction
    i, j = get_position(last, direction, steps)
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

if __name__ == "__main__":
    with Path("day_18/input.txt").open("r") as file:
        data = [format_input(row) for row in file.read().splitlines()]
    start = (0, 0)
    corners = [start]
    last_corner = start
    total_walls = 0
    for instruction in data:
        last_corner = build_corners(instruction, last_corner, corners)
        total_walls += instruction[1]  # steps
    print( area(corners) + total_walls // 2 + 1)
