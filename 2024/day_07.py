import argparse

from collections import deque
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

OPERATORS = (
    lambda x,y: x + y,
    lambda x,y: x * y,
)

def can_be_made(val: int, eq: deque, *, is_part_two: bool = False) -> bool:
    functions = OPERATORS + (lambda x, y: int(str(x) + str(y)),) if is_part_two else OPERATORS
    res = eq.popleft()
    queue = {res}
    while eq:
        next_val = eq.popleft()
        new_queue = set()
        for r in queue:
            if r > val:
                continue
            for func in functions:
                new_queue.add(func(r, next_val))
        queue = new_queue
    return val in queue

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = []
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            key, val = line.strip().split(":")
            data.append((int(key), deque([int(x.strip()) for x in val.split(" ") if x])))
    print(sum(key for key, value in data if can_be_made(key, value, is_part_two=args.part == 2)))
    print(time() - t)
