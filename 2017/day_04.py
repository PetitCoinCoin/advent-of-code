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

def is_valid_identical(passphrase: list) -> bool:
    return len(passphrase) == len(set(passphrase))

def is_valid_anagram(passhrase: list) -> bool:
    return len(passhrase) == len(set("".join(sorted(w)) for w in passhrase))

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [row.split(" ") for row in file.read().split("\n")]
    if args.part == 1:
        print(sum(is_valid_identical(phrase) for phrase in data))
    else:
        print(sum(is_valid_anagram(phrase) for phrase in data))
