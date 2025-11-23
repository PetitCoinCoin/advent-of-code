import argparse

from collections import deque
from functools import cache
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

def is_valid(pattern: str) -> bool:
    queue = deque()
    queue.append("")
    while queue:
        current = queue.pop()
        if current == pattern:
            return True
        for tow in towels:
            if pattern[len(current):].startswith(tow):
                queue.append(current + tow)
    return False

@cache
def count_arrangements(pattern: str, done: str = "") -> int:
    if done == pattern:
        return 1
    count = 0
    for tow in towels:
        limit = len(pattern) - len(done)
        if pattern[:limit].endswith(tow):
            count += count_arrangements(pattern, tow + done)
    return count

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        tow, pat = file.read().strip().split("\n\n")
    towels = [x.strip() for x in tow.split(", ")]
    towels.sort()
    patterns = pat.split("\n")
    if args.part == 1:
        print(sum(is_valid(pattern) for pattern in patterns))
    else:
        print(sum(count_arrangements(pattern) for pattern in patterns if is_valid(pattern)))
    print(time() - t)
