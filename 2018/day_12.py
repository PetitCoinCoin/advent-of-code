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

def get_neighbours(data: dict) -> None:
    for k, v in data.items():
        data[k] = (v[0], "".join([data.get(k + d, (".", ""))[0] for d in range(-2, 3)]))

def add_edges(data: dict) -> None:
    min_k = 1000000
    max_k = -1000000
    to_add = []
    for k, v in data.items():
        if k < min_k and v[0] == "#":
            min_k = k
            for delta in (1, 2):
                if not data.get(k - delta):
                    to_add.append(k - delta)
        if k > max_k and v[0] == "#":
            max_k = k
            for delta in (1, 2):
                if not data.get(k + delta):
                    to_add.append(k + delta)
    for key in to_add:
        data[key] = (".", "")

def parse_input(data: str) -> tuple:
    pots_input, instructions_input = data.split("\n\n")
    pots_input = pots_input.split(": ")[-1].strip()
    pots = {i: (char, "") for i, char in enumerate(pots_input)}
    add_edges(pots)
    get_neighbours(pots)
    instructions_input = instructions_input.split("\n")
    instructions = {
        inst.split(" => ")[0]
        for inst in instructions_input
        if inst and inst.split(" => ")[1] == "#"
    }
    return pots, instructions

def generation() -> None:
    for k, v in pots.items():
        pots[k] = ("#", "") if v[1] in instructions else "."
    add_edges(pots)
    get_neighbours(pots)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        pots, instructions = parse_input(file.read())
    if args.part == 1:
        for _ in range(20):
            generation()
        print(sum(k for k, v in pots.items() if v[0] == "#"))
    else:
        # Looking at the first ~200 iterations, we can find a pattern and deduce answer
        # At 118th iteration, first plant is at index 30
        # Afterwards, the pattern shifts one to the right at each iteration
        pattern = "#..##.#..##.#..##.#..##.#......#....#..##.#....#.......#....#.......#....#......#....#..##.#..##.#..##.#......#..##.#..##.#.......#.......#....#....#......#....#..##.#.......#..##.#......#.."
        pattern_sum = sum(i for i, char in enumerate(pattern) if char == "#")
        pattern_len = len([char for char in pattern if char == "#"])
        print(pattern_sum + pattern_len * (30 + 50000000000 - 118))
    print(time() - t)
