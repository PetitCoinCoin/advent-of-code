import argparse
import math

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

DIRECTIONS_MAP = {
    "L": 0,
    "R": 1,
}

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    directions = ""
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            if len(line) > 1 and len(line.split(" = ")) != 2:
                directions = line.strip()
            elif len(line) > 1:
                key = line.split(" = ")[0]
                value = line.split(" = ")[1].replace("(", "").replace(")\n", "").split(", ") if args.part == 1 else line.split(" = ")[1].replace("(", "").replace(")", "").split(", ")
                data[key] = value if args.part == 1 else [val.strip() for val in value]
    if args.part == 1:
        node = "AAA"
        steps = 0
        while node != "ZZZ":
            node = data[node][DIRECTIONS_MAP[directions[steps % len(directions)]]]
            steps += 1
        print(steps)
    else:
        znodes = [key for key in data.keys() if key[-1] == "Z"]
        zsteps = {}
        for node in znodes:
            zstep = 0
            while node[-1] != "Z" or zstep == 0:
                node = data[node][DIRECTIONS_MAP[directions[zstep % len(directions)]]]
                zstep += 1
            zsteps[node] = zstep

        anodes = [key for key in data.keys() if key[-1] == "A"]
        asteps = {}
        for node in anodes:
            astep = 0
            while node[-1] != "Z":
                node = data[node][DIRECTIONS_MAP[directions[astep % len(directions)]]]
                astep += 1
            asteps[node] = astep

        # We notice that each --Z node loops on itself, and --Z > --> always equals --A > --Z
        print(math.lcm(*asteps.values()))
    print(time() - t)

