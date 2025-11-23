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

NUM_MAP = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}

def digitize(value: str, *, is_part_two: bool = False) -> int:
    if is_part_two:
        for k,v in NUM_MAP.items():
            value = value.replace(k, v)
    digits = [x for x in value if x.isdigit()]
    return int(digits[0] + digits[-1])

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    calibrations_values = [digitize(value, is_part_two=args.part == 2) for value in data]
    print(sum(calibrations_values))

    print(time() - t)
