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

PREAMBLE = 25

def is_sum_of_two(val: int, previous: int) -> bool:
    for i, v1 in enumerate(previous[:-1]):
        for v2 in previous[i + 1:]:
            if v1 + v2 == val:
                return True
    return False

def find_set() -> int:
    for i in range(len(data) - 1):
        contiguous_sum = data[i]
        for j in range(1, len(data) - i):
            contiguous_sum += data[i + j]
            if contiguous_sum == invalid:
                return min(data[i:i + j +1]) + max(data[i:i + j +1])
            if contiguous_sum > invalid:
                break
    print("WTF")
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split("\n")]
    invalid = 0
    for i in range(PREAMBLE, len(data)):
        if not is_sum_of_two(data[i], data[i - PREAMBLE: i]):
            invalid = data[i]
            data = data[:i]
            break
    if args.part == 1:
        print(invalid)
    else:
        print(find_set())
    print(time() - t)
