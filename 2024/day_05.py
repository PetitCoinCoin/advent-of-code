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

def is_valid(inp: list) -> bool:
    seen = set()
    for item in inp:
        if seen and rules.get(item) and len(rules[item].intersection(seen)):
            return False
        seen.add(item)
    return True

def reorder(inp: list) -> list:
    seen = inp
    previous = []
    while seen != previous:
        previous = seen
        seen = []
        for item in previous:
            if seen and rules.get(item) and len(rules[item].intersection(set(seen))):
                to_move = rules[item].intersection(set(seen)).pop()
                idx = seen.index(to_move)
                seen.insert(idx, item)
            else:
                seen.append(item)
    return seen

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    rules = {}
    data = []
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        is_rule = True
        while line := file.readline():
            if line == "\n":
                is_rule = False
                continue
            if is_rule:
                key, val = tuple(line.strip().split("|"))
                rules[int(key)] = rules.get(int(key), set()) | set([int(val)])
            else:
                data.append([int(x) for x in line.strip().split(",")])
    if args.part == 1:
        print(sum(
            item[len(item) // 2]
            for item in data
            if is_valid(item)
        ))
    else:
        data = [reorder(item) for item in data if not is_valid(item)]
        print(sum(
            item[len(item) // 2]
            for item in data
        ))
    print(time() - t)
