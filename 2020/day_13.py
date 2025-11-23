import argparse
import math

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

def chinese_remainder_theorem() -> int:
    n = 1
    for bus in buses:
        n *= bus
    result = 0
    for r, bus in enumerate([int(x) if x.isdigit() else None for x in data[1].split(",")]):
        if not bus:
            continue
        n_except = int(n / bus)
        mul = 1
        while (mul * n_except) % bus != 1:
            mul += 1
        result += (bus - r) * mul * n_except
    return result % n

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    start = int(data[0])
    buses = [int(x) for x in data[1].split(",") if x.isdigit()]
    if args.part == 1:
        at_departure = False
        timestamp = start
        while not at_departure:
            for bus in buses:
                if not timestamp % bus:
                    print(bus * (timestamp - start))
                    at_departure = True
                    break
            timestamp += 1
    else:
        print(chinese_remainder_theorem())
    print(time() - t)
