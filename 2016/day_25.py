import argparse

from math import factorial
from dataclasses import dataclass
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
    if args.part == 1:
        # 2730 is 101010101010 in binary
        # 2538 = 9 x 282 = init_c * init_b
        print(2730 - 2538)
    else:
        print("all stars!")
