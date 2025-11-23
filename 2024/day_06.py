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

def parse_input(raw: str, i) -> None:
    for r, char in enumerate(raw):
        data[complex(r, -i)] = char

def guard_move(is_part_two: bool = False) -> list | int:
    position = start
    seen = {start}
    d = 1j
    while True:
        next_char = data.get(position + d, "")
        if not next_char:
            return seen if is_part_two else len(seen)
        while next_char == "#":
            d *= -1j
            next_char = data.get(position + d, "")
        position += d
        seen.add(position)

def guard_loop() -> int:
    position = start
    seen = set()
    d = 1j
    while True :
        if (position, d) in seen:
            return 1
        next_char = data.get(position + d, "")
        if not next_char:
            return 0
        if next_char == ".":
            position += d
            continue
        while next_char == "#":
            seen.add((position, d))
            d *= -1j
            next_char = data.get(position + d, "")
        position += d

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        i = 0
        while line := file.readline():
            parse_input(line.strip(), i)
            i += 1
    for k, v in data.items():
        if v == "^":
            start = k
            data[k] = "."
            break
    if args.part == 1:
        print(guard_move())
    else:
        path = guard_move(True)
        set_path = set(path)
        set_path.remove(start)
        obstacles = 0
        for position in set_path:
            data[position] = "#"
            obstacles += guard_loop()
            data[position] = "."
        print(obstacles)
    print(time() - t)
