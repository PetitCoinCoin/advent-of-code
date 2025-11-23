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

def is_safe(report: list) -> bool:
    prev_d = None
    for i in range(1, len(report)):
        d = report[i] - report[i-1]
        if not d or abs(d) > 3:
            return False
        if prev_d and prev_d * d < 0:
            return False
        prev_d = d
    return True

def is_really_safe(report: list) -> bool:
    if is_safe(report):
        return True
    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1:]):
            return True
    return False

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [[int(x) for x in line.split(" ")] for line in file.read().split("\n")]
    if args.part == 1:
        print(sum(is_safe(report) for report in data))
    else:
        print(sum(is_really_safe(report) for report in data))
    print(time() - t)
