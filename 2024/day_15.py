import argparse

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

DIR_MAP = {
    "^": 1j,
    ">": 1,
    "v": -1j,
    "<": -1,
}

def parse_grid(raw: str,* , is_part_two: bool) -> tuple:
    start = 0
    grid = {}
    for i, row in enumerate(raw.split("\n")):
        for r, char in enumerate(row):
            if is_part_two:
                if char in ".#":
                    grid[complex(2 * r, -i)] = char
                    grid[complex(2 * r + 1, -i)] = char
                elif char == "O":
                    grid[complex(2 * r, -i)] = "["
                    grid[complex(2 * r + 1, -i)] = "]"
                else:
                    grid[complex(2 * r, -i)] = "."
                    grid[complex(2 * r + 1, -i)] = "."
                    start = complex(2 * r, -i)
            else:
                grid[complex(r, -i)] = char
                if char == "@":
                    start = complex(r, -i)
                    grid[start] = "."
    return start, grid

def parse_moves(raw:str) -> list:
    return [DIR_MAP[direction] for direction in raw if direction != "\n"]

def can_move_vertically(pos: complex, direction: complex) -> bool:
    if grid[pos] == "]" :
        delta = -1
    elif grid[pos] == "[":
        delta = 1
    else:
        return grid[pos] == "."
    if grid[pos + direction] == "." and grid[pos + direction + delta] == ".":
        return True
    if grid[pos + direction] == "#" or grid[pos + direction + delta] == "#":
        return False
    return can_move_vertically(pos + direction, direction) and can_move_vertically(pos + direction + delta, direction)

def move_vertically(pos: complex, direction: complex) -> None:
    if grid[pos] == "]":
        delta = -1
    elif grid[pos] == "[":
        delta = 1
    else:
        return None
    while grid[pos + direction] != "." or grid[pos + direction + delta] != ".":
        move_vertically(pos + direction, direction)
        move_vertically(pos + direction + delta, direction)
    grid[pos + direction] = grid[pos]
    grid[pos + direction + delta] = grid[pos + delta]
    grid[pos] = "."
    grid[pos + delta] = "."

def can_move_horizontally(pos: complex, direction: complex) -> bool:
    char = grid[pos + 2 * direction]
    if char == "#":
        return False
    if char == ".":
        return True
    else:
        return can_move_horizontally(pos + 2 * direction, direction)

def move_horizontally(pos: complex, direction: complex) -> None:
    while grid[pos + 2 * direction] != ".":
        move_horizontally(pos + 2 * direction, direction)
    grid[pos + 2 * direction] = grid[pos + direction]
    grid[pos + direction] = grid[pos]
    grid[pos] = "."

def robot_move(robot: complex, *, is_part_two: bool) -> None:
    for move in moves:
        if grid[robot + move] == ".":
            robot += move
        elif grid[robot + move] == "#":
            continue
        else:
            nb = 1
            if not is_part_two:
                while grid[robot + nb * move] not in ".#":
                    nb += 1
                if grid[robot + nb * move] == "#":
                    continue
                else:
                    grid[robot + nb * move] = "O"
                    grid[robot + move] = "."
                    robot += move
            else:
                if move in (1, -1):
                    if not can_move_horizontally(robot + move, move):
                        continue
                    move_horizontally(robot + move, move)
                elif not can_move_vertically(robot + move, move):
                    continue
                else:
                    move_vertically(robot + move, move)
                robot += move

def gps(c: complex) -> int:
    return int(-100 * c.imag + c.real)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        g, m = file.read().split("\n\n")
    robot, grid = parse_grid(g, is_part_two=args.part == 2)
    moves = parse_moves(m)
    robot_move(robot, is_part_two=args.part == 2)
    box = "O" if args.part == 1 else "["
    print(sum(gps(pos) for pos, item in grid.items() if item == box))
    print(time() - t)
