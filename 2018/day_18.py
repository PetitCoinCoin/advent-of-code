import argparse

from copy import deepcopy
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

# x, y, z = open, tree, lumberyard
UPDATE_MAP = {
    ".": lambda _x, y, _z: "|" if y >= 3 else ".",
    "|": lambda _x, _y, z: "#" if z >= 3 else "|",
    "#": lambda _x, y, z: "#" if y >= 1 and z >= 1 else ".",
}

def get_neighbours(position: tuple) -> tuple:
    r, c = position
    opens, trees, lumberyards = 0, 0, 0
    for delta in ((-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)):
        dr, dc = delta
        acre = data.get((r + dr, c + dc), "")
        if acre == ".":
            opens += 1
        elif acre == "|":
            trees += 1
        elif acre == "#":
            lumberyards += 1
    # print(position, opens, trees, lumberyards)
    return opens, trees, lumberyards

def update_acres(acres: dict) -> dict:
    result = deepcopy(acres)
    for key in result.keys():
        result[key] = UPDATE_MAP[acres[key]](*get_neighbours(key))
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        for r, line in enumerate(file.read().split("\n")):
            for c, char in enumerate(line):
                data[(r, c)] = char
    if args.part == 1:
        for _ in range(10):
            data = update_acres(data)
        print(len([k for k, v in data.items() if v == "#"]) * len([k for k, v in data.items() if v == "|"]))
    else:
        # A pattern appears from loop 503, and period is 28min
        cache = {}
        pattern_start = 502
        period = 28
        for i in range(530):
            data = update_acres(data)
            cache[i] = len([k for k, v in data.items() if v == "#"]) * len([k for k, v in data.items() if v == "|"])
        print(cache[((1000000000 - 1 - pattern_start) % period) + pattern_start])
    print(time() - t)
