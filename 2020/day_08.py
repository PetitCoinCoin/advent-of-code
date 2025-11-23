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

def execute() -> tuple:
    i = 0
    acc = 0
    seen = {}
    while i < len(data):
        if i in seen:
            return acc, False
        seen[i] = True
        instruction, delta = data[i]
        if instruction == "acc":
            acc += delta
            i += 1
        elif instruction == "jmp":
            i += delta
        else:
            i += 1
    return acc, True

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [
            (row.split(" ")[0], int(row.split(" ")[1]))
            for row in file.read().strip().split("\n")
        ]
    if args.part == 1:
        print(execute()[0])
    else:
        for i, item in enumerate(data):
            if item[0] == "nop":
                data[i] = ("jmp", item[1])
            elif item[0] == "jmp":
                data[i] = ("nop", item[1])
            else:
                continue
            # print(i, data)
            acc, fixed = execute()
            if fixed:
                break
            if item[0] == "nop":
                data[i] = ("nop", item[1])
            elif item[0] == "jmp":
                data[i] = ("jmp", item[1])
        print(acc)        
    print(time() - t)
