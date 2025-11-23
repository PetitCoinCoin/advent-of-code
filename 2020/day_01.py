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

def check_two_expenses(target: int = 2020) -> tuple:
    return tuple(x for x in data if (target - x) in data)

def check_three_expenses() -> int:
    for x in data:
        t = check_two_expenses(2020 - x)
        if t:
            y, z = t
            return x * y * z

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = {int(x) for x in file.read().strip().split("\n")}
    if args.part == 1:
        suspicious_1, suspicious_2 = check_two_expenses()
        print(suspicious_1 * suspicious_2)
    else:
        print(check_three_expenses())
    print(time() - t)
