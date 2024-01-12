import argparse

from copy import deepcopy
from itertools import combinations
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

def parse_input(row: str, r: int, data: dict) -> None:
    for c, light in enumerate(row):
        data[complex(r, c)] = True if light == "#" else False

def flash(state: dict, corners_on: bool = False) -> dict:
    next_state = deepcopy(state)
    for key, value in state.items():
        neighbors = [
            state.get(key + complex(r, i), False)
            for r, i in set(combinations([-1, 0, 1] * 2, 2))
            if r != 0 or i != 0
        ]
        next_state[key] = (value and sum(neighbors) in (2, 3)) or (not value and sum(neighbors) == 3)
    if corners_on:
        for corner in (0j, 99j, 99 + 0j, 99 + 99j):
            next_state[corner] = True
    return next_state

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = dict()
        r = 0
        while line := file.readline():
            parse_input(line.strip(), r, data)
            r += 1
    if args.part == 1:
        for _ in range(100):
            data = flash(data)
        print(sum(data.values()))
    else:
        for corner in (0j, 99j, 99 + 0j, 99 + 99j):
            data[corner] = True
        for _ in range(100):
            data = flash(data, True)
        print(sum(data.values()))
