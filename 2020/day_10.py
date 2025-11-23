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

JOLTS = (1, 2, 3)

def identify_sub_chains(chain: list) -> list:
    result = []
    start = 0
    i = 0
    for i in range(len(chain) - 1):
        if chain[i + 1] - chain[i] == 1:
            continue
        result.append(chain[i] + 1 - start)
        start = chain[i + 1]
    result.append(chain[-1] + 1 - start)
    return result

def count_chains(steps: int) -> int:
    if steps == 0:
        return 1
    if steps < 0:
        return 0
    return sum(count_chains(steps - jolt) for jolt in JOLTS)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split("\n")]
    data.append(0)  # charging outlet
    diff = {
        1: [],
        2: [],
        3: [len(data) - 1],  # device's built-in adapter
    }
    data = sorted(data)
    for i in range(len(data) - 1):
        delta = data[i + 1] - data[i]
        diff[delta].append(i)
    if args.part == 1:
        print(len(diff[1]) * len(diff[3]))
    else:
        print(math.prod(count_chains(sub) for sub in identify_sub_chains(diff[1])))
    print(time() - t)
