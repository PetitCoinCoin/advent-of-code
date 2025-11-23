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

def parse_input(raw: str, i: int) -> None:
    for r, char in enumerate(raw):
        data[complex(r, -i)] = char

def xmas(position) -> bool:
    expected = "MAS"
    delta = (1j, -1j, 1, -1, -1j -1, -1j + 1, 1j -1, 1j + 1)
    i = 0
    queue = {(d, position + d) for d in delta if expected[i] == data.get(position + d, ".")}
    while queue and i < 2:
        new_queue = set()
        i += 1
        for d, pos in queue:
            if expected[i] == data.get(pos + d, "."):
                    new_queue.add((d, pos + d))
        queue = new_queue
    return len(queue)


def x_mas(position) -> int:
    delta = (-1j -1, -1j + 1, 1j -1, 1j + 1)
    queue = {position + d:  data.get(position + d, ".") for d in delta if data.get(position + d, ".") in "MS"}
    if len(queue) < 4:
        return 0
    return int(queue[position -1j -1] != queue[position + 1j + 1] and queue[position -1j +1] != queue[position + 1j - 1])

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        [parse_input(line, i) for i,line in enumerate(file.read().split("\n"))]
    if args.part == 1:
        pivot = "X"
        func = xmas
    else:
        pivot = "A"
        func = x_mas
    total = 0
    for k, v in data.items():
        if v == pivot:
            total += func(k)
    print(total)
    print(time() - t)
