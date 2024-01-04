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

def is_nice(txt: str) -> bool:
    for forbidden in ("ab", "cd", "pq", "xy"):
        if forbidden in txt:
            return False
    count = Counter(txt)
    if sum([val for key, val in count.items() if key in "aeiou"]) < 3:
        return False
    for i, c in enumerate(txt):
        if i != len(txt) - 1 and c == txt[i + 1]:
            return True
    return False

def is_nicer(txt: str) -> bool:
    for i in range(len(txt) - 3):
        if txt[i:i + 2] in txt[i + 2:]:
            break
    else:
        return False
    for i in range(len(txt) - 2):
        if txt[i] == txt[i + 2]:
            return True
    return False

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        print(sum([is_nice(txt) for txt in data]))
    else:
        print(sum([is_nicer(txt) for txt in data]))
