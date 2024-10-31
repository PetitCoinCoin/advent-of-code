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

def has_multiple(mul: int, char: str) -> bool:
    count = Counter(char)
    return mul in count.values()

def get_boxes(ids: list) -> str:
    for i in range(len(ids) - 1):
        for j in range(i + 1, len(ids)):
            check = sum(x != y for x,y in zip(ids[i], ids[j]))
            if check == 1:
                return "".join([x for x,y in zip(ids[i], ids[j]) if x == y])
    return ""

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    if args.part == 1:
        has_two = sum(has_multiple(2, item) for item in data)
        has_three = sum(has_multiple(3, item) for item in data)
        print(has_two * has_three)
    else:
        print(get_boxes(data))
