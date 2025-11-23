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

GRID = 300

def power_level(x: int, y: int) -> int:
    return (((((x + 10) * y + sn) * (x + 10) // 100)) % 10) - 5

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        sn = int(file.read())
    data = {
        (x, y): power_level(x, y)
        for x in range(1, GRID + 1)
        for y in range(1, GRID + 1)
    }
    partial_sum = {}
    for x in range(1, GRID + 1):
        for y in range(1, GRID + 1):
            partial_sum[(x, y)] = (
                data[(x, y)]
                + partial_sum.get((x - 1, y), 0)
                + partial_sum.get((x, y - 1), 0)
                - partial_sum.get((x - 1, y - 1), 0)
            )
    total_power = {
        (x, y, s): partial_sum[(x, y)]- partial_sum.get((x - s, y), 0) - partial_sum.get((x, y - s), 0) + partial_sum.get((x - s, y - s), 0)
        for s in (range(1, GRID + 1) if args.part == 2 else range(3, 4))
        for x in range(s, GRID + 1)
        for y in range(s, GRID + 1)
    }
    x, y, s = max(total_power, key=lambda key: total_power[key])
    result = f"{x - s + 1},{y - s + 1}"
    if args.part == 2:
        result += f",{s}"
    print(result)
    print(time() - t)
