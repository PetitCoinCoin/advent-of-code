import argparse

from ast import literal_eval
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

def diff_memory(string: str) -> int:
    return len(string) - len(literal_eval(string))

def diff_encoded(string: str) -> int:
    count = Counter(string)
    return 2 + count['"'] + count["\\"]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        print(sum([diff_memory(d) for d in data]))
    else:
        print(sum([diff_encoded(d) for d in data]))
