import argparse
import re

from collections import deque
from heapq import heappop, heappush
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

def parse_input(row: str, data: dict) -> None:
    key = row.split(" => ")[0]
    value = row.split(" => ")[1]
    data[key] = data.get(key, []) + [value]

def build_molecule(results: set, input_mol: str, key: str, value: list) -> None:
    for char in re.finditer(key, input_mol):
        kstart, kend = char.span()
        for val in value:
            results.add(input_mol[:kstart] + val + input_mol[kend:])

def reverse_data(data: dict) -> dict:
    reversed_dict = dict()
    for key, value in data.items():
        for val in value:
            reversed_dict[val] = key
    return reversed_dict

def retro_eng(data: dict, step: int,  molecule: str) -> tuple:
    found = []
    for pattern in data.keys():
        d = deque(re.finditer(pattern, molecule), maxlen=1)
        if d:
            last_found = d.pop()
            heappush(found, (tuple(-i for i in last_found.span()), last_found.group(0)))
    inv_span, key = heappop(found)
    return step + 1, molecule[:-inv_span[0]] + data[key] + molecule[-inv_span[1]:]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = dict()
        molecule = None
        while line := file.readline():
            if not line.strip():
                molecule = ""
                continue
            if molecule is None:
                parse_input(line.strip(), data)
            else:
                molecule = line.strip()
    if args.part == 1:
        results = set()
        for key, value in data.items():
            build_molecule(results, molecule, key, value)
        print(len(results))
    else:
        reversed_data = reverse_data(data)
        step = 0
        while molecule != "e":
            step, molecule = retro_eng(reversed_data, step, molecule)
        print(step)
