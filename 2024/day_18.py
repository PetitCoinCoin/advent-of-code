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

GRID = 70
BYTES = 1024

def move() -> int:
    pos = 0
    dist = 0
    seen = {pos: True}
    current = {pos}
    while complex(GRID, -GRID) not in current:
        dist += 1
        new_current = set()
        for pos in current:
            for d in (1, -1, 1j, -1j):
                if pos + d not in seen and grid.get(pos + d, "#") != "#":
                    new_current.add(pos + d)
                    seen[pos + d] = True
        current = new_current
        if not current:
            return 0
    return dist

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [[int(x) for x in line.split(",")] for line in file.readlines()]
    grid = {}
    for item in data[:BYTES]:
        grid[complex(item[0], -item[1])] = "#"
    for r in range(GRID + 1):
        for i in range(GRID + 1):
            if complex(r, -i) not in grid:
                grid[complex(r, -i)] = "."
    if args.part == 1:
        print(move())
    else:
        b = BYTES
        while b < len(data):
            item = data[b]
            grid[complex(item[0], -item[1])] = "#"
            if not move():
                print(",".join([str(x) for x in item]))
                break
            b += 1
    print(time() - t)
