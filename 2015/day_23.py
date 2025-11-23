import argparse
import re

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

INSTRUCTIONS = {
    "inc": lambda x: x + 1,
    "tpl": lambda x: x * 3,
    "hlf": lambda x: x // 2,
}

def process(raw: str, a: int, b: int, i:int) -> tuple:
    if raw[:3] in INSTRUCTIONS.keys():
        if raw[-1] == "a":
            return INSTRUCTIONS[raw[:3]](a), b, i + 1
        return a, INSTRUCTIONS[raw[:3]](b), i + 1
    if raw[:3] == "jmp":
        return a, b, i + int(raw.split(" ")[-1])
    raw_split = raw.split(" ")
    if raw.startswith("jie") and not eval(raw_split[1][:-1]) % 2:
        return a, b, i + int(raw_split[-1])
    if raw.startswith("jio") and eval(raw_split[1][:-1]) == 1:
        return a, b, i + int(raw_split[-1])
    return a, b, i + 1

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    a = b = i = 0
    if args.part == 2:
        a = 1
    while -1 < i < len(data):
        a, b, i = process(data[i], a, b, i)
    print(a, b)
