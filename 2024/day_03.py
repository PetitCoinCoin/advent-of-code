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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read()
    if args.part == 1:
        pattern = r"mul\(([\d]{1,3},[\d]{1,3})\)"
        print(sum(int(item.split(",")[0]) * int(item.split(",")[1]) for item in re.findall(pattern, data)))
    else:
        pattern = r"mul\(([\d]{1,3},[\d]{1,3})\)|(do\(\))|(don't\(\))"
        result = 0
        can_sum = True
        for item in re.findall(pattern, data):
            if item[1]:
                can_sum = True
            elif item[2]:
                can_sum = False
            else:
                result += int(item[0].split(",")[0]) * int(item[0].split(",")[1]) * can_sum
        print(result)
    print(time() - t)
