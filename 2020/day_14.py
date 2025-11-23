import argparse
import re

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

def parse_input(raw: str) -> list:
    mask = ""
    for line in raw.split("\n"):
        if line.startswith("mask"):
            mask = line.split(" = ")[-1]
            data[mask] = []
            continue
        pattern = r"mem\[(\d+)\] = (\d+)"
        key, val = re.findall(pattern, line)[0]
        data[mask].append((int(key), int(val)))

def get_base_key(mask: str, key: int) -> str:
    key |= int(mask.replace("X", "0"), 2)
    binary_key = bin(key)[2:].zfill(len(mask))
    return "".join(
        binary_key[i] if mask[i] != "X" else "X"
        for i in range(len(mask))
    )

def get_all_keys(key: str) -> list:
    if "X" not in key:
        return [int(key, 2)]
    return get_all_keys(key.replace("X", "1", 1)) + get_all_keys(key.replace("X", "0", 1))

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    mem = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        parse_input(file.read().strip())
    if args.part == 1:
        for mask, instructions in data.items():
            mask_and = int(mask.replace("X", "1"), 2)
            mask_or = int(mask.replace("X", "0"), 2)
            for key, val in instructions:
                mem[key] = (val & mask_and) | mask_or
    else:
        for mask, instructions in data.items():
            for key, val in instructions:
                for new_key in get_all_keys(get_base_key(mask, key)):
                    mem[new_key] = val
    print(sum(mem.values()))
    print(time() - t)
