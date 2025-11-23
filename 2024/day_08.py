import argparse

from itertools import permutations
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

def locate_antinodes(antennas: set, *, is_part_two: bool = False) -> set:
    res = set()
    for a, b in permutations(antennas, 2):
        delta = b - a
        anti = a - delta
        if is_part_two:
            res.add(b)
        while anti.real >= 0 and anti.real < width and anti.imag <= 0 and anti.imag > -height:
            res.add(anti)
            if not is_part_two:
                break
            anti -= delta
    return res

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    i = 0
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            for r, char in enumerate(line.strip()):
                if char != ".":
                    data[char] = data.get(char, set()) | {complex(r, -i)}
                width = r + 1
            i += 1
        height = i
    antinodes = set()
    for antennas in data.values():
        antinodes |= locate_antinodes(antennas, is_part_two=args.part == 2)
    print(len(antinodes))
    print(time() - t)
