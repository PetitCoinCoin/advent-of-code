import argparse

from heapq import heapify, heappop
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

def get_paper(row: str) -> int:
    dimensions = [int(x) for x in row.split("x")]
    a1 = dimensions[0] * dimensions[1]
    a2 = dimensions[0] * dimensions[2]
    a3 = dimensions[1] * dimensions[2]
    min_area = min(a1, a2, a3)
    return min_area + 2 * a1 + 2 * a2 + 2* a3

def get_ribbon(row: str) -> int:
    dimensions = [int(x) for x in row.split("x")]
    volume = dimensions[0] * dimensions[1] * dimensions[2]
    heapify(dimensions)
    min_dim1 = heappop(dimensions)
    min_dim2 = heappop(dimensions)
    return volume + 2 * (min_dim1 + min_dim2)

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        print(sum([get_paper(row) for row in data]))
    else:
        print(sum([get_ribbon(row) for row in data]))
