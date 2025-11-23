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

def parse_input(raw: str) -> int:
    items = keys if raw[0] == "." else locks
    item = []
    lines = raw.split("\n")
    for i in range(len(lines[0])):
        item.append(sum(1 if line[i] == "#" else 0 for line in lines) - 1)
    items.append(item)
    return len(lines) - 2
    

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n\n")
    keys = []
    locks = []
    for raw in data:
        available_space = parse_input(raw.strip())
    if args.part == 1:
        matching = 0
        for key in keys:
            for lock in locks:
                for k, l in zip(key, lock):
                    if k + l > available_space:
                        break
                else:
                    matching += 1
        print(matching)
    else:
        raise NotImplementedError
    print(time() - t)
