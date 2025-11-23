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
        data[complex(r, -i)] = int(char)
        if not int(char):
            starts.add(complex(r, -i))

def next_steps(position: complex, h: int) -> set:
    return {
        position + d
        for d in (1j, -1j, 1, -1)
        if data.get(position + d) is not None and data.get(position + d) == h
    }

def hike_from(start: complex, *, is_part_two: bool = False) -> int:
    paths = [start] if is_part_two else {start}
    height = 0
    while height < 9:
        height += 1
        new_paths = [] if is_part_two else set()
        for position in paths:
            if is_part_two:
                new_paths += list(next_steps(position, height))
            else:
                new_paths |= next_steps(position, height)
        paths = new_paths
    return len(paths)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    starts = set()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        i = 0
        while line := file.readline():
            parse_input(line.strip(), i)
            i += 1
    print(sum(hike_from(s, is_part_two=args.part == 2) for s in starts))
    print(time() - t)
