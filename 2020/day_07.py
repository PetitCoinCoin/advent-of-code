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

TARGET = "shiny gold"

def parse_input(raw: str) -> None:
    for row in raw.split("\n"):
        key_data, val_data = tuple(row.split(" contain "))
        key = key_data[:-5]
        if val_data == "no other bags.":
            data[key] = {}
        else:
            matches = re.findall(r"(\d+) ([a-z\s]+) bag", val_data)
            data[key] = {match[1]: int(match[0]) for match in matches}

def find_target(bag: str) -> bool:
    if bag in has_target:
        return has_target[bag]
    if bag == TARGET:
        return False
    if not data[bag]:
        return False 
    if TARGET in data[bag]:
        return True
    return any(find_target(sub)for sub in data[bag].keys())
        
def count_bags(bag:str = TARGET) -> int:
    return sum((count * (1 + count_bags(sub)) for sub, count in data[bag].items()), 0)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        parse_input(file.read().strip())
    if args.part == 1:
        has_target = {}
        for bag in data.keys():
            has_target[bag] = find_target(bag)
        print(sum(has_target.values()))
    else:
        print(count_bags())
    print(time() - t)
