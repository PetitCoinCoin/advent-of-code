import argparse
import math

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

def count_trees(right: int, down: int) -> int:
    return sum(
        1
        for i in range(0, len(data), down)
        if data[i][(start + right * i) % width] == "#"
    )

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    start = 0
    width = len(data[0])
    if args.part == 1:
        print(count_trees(3, 1))
    else:
        print(math.prod(count_trees(right, 1) for right in (1, 3, 5, 7)) * count_trees(1, 2))
    print(time() - t)
