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

def intersect_yes(group: list) -> int:
    res = set(group[0])
    for answer in group[1:]:
        res = res.intersection(set(answer))
    return len(res)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [[x for x in group.split("\n")] for group in file.read().strip().split("\n\n")]
    if args.part == 1:
        print(sum(len({char for item in group for char in item}) for group in data))
    else:
        print(sum(intersect_yes(group) for group in data))
    print(time() - t)
