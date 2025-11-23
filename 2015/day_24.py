import argparse

from heapq import heappop, heappush
from itertools import combinations
from math import prod
from pathlib import Path

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

def find_groups(data: set, weight: int, groups: int) -> bool:
    for n in range(1, len(data) // groups + 1):
        combi = combinations(data, n)
        for c in combi:
            if sum(c) == weight and sum(data) - sum(c) == weight * (groups - 1):
                return True
    return False

def process(data: set, groups: int) -> None:
    for n in range(1, len(data) // groups + 1):
        combi = combinations(data, n)
        queue = []
        for c in combi:
            if (groups - 1) * sum(c) != sum(data) - sum(c):
                continue
            heappush(queue, (prod(c), c))
        while len(queue):
            qe, config = heappop(queue)
            check = find_groups(data - set(config), sum(config), groups - 1)
            if check:
                print(qe, config)
                return None
    return None

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = {int(x) for x in file.readlines()}
    if args.part == 1:
        process(data, 3)
    else:
        process(data, 4)
