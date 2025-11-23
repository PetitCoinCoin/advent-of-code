import argparse

from itertools import combinations
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

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().splitlines()]
    if args.part == 1:
        permutations = []
        for r in range(1, len(data)):
            permutations += combinations(data, r)
        print(sum([1 if sum(combi) == 150 else 0 for combi in permutations]))
    else:
        for r in range(1, len(data)):
            result = sum([1 if sum(combi) == 150 else 0 for combi in combinations(data, r)])
            if result:
                print(result, r)
                break
