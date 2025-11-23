import argparse

from collections import Counter
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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    left = [int(row.split("   ")[0]) for row in data]
    right = [int(row.split("   ")[1]) for row in data ]
    if args.part == 1:
        left.sort()
        right.sort()
        print(sum([abs(l - r) for l, r in zip(left, right)]))
    else:
        right_count = Counter(right)
        similarity = 0
        for l in left:
            similarity += l * right_count.get(l, 0)
        print(similarity)
    print(time() - t)
