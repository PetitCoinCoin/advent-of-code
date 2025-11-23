import argparse

from collections import Counter
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
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = dict()
        while line := file.readline():
            for i, c in enumerate(line.strip()):
                data[i] = data.get(i, []) + [c]
    print("".join(
        [Counter("".join(value)).most_common()[0 if args.part == 1 else -1][0] for value in data.values()]
    ))
