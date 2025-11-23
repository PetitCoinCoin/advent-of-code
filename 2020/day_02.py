import argparse
import re

from collections import Counter
from dataclasses import dataclass
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

@dataclass
class Pwd:
    minp: int
    maxp: int
    charp: str
    pwd: str

    @property
    def is_valid(self) -> bool:
        return self.minp <= Counter(self.pwd)[self.charp] <= self.maxp

    @property
    def is_valid_new(self) -> bool:
        return (self.pwd[self.minp - 1] == self.charp) ^ (self.pwd[self.maxp - 1] == self.charp)

def parse_input(raw) -> Pwd:
    pattern = r"(\d+)-(\d+) ([a-zA-Z]): ([a-zA-Z]+)"
    minp, maxp, charp, pwd = re.findall(pattern, raw)[0]
    return Pwd(int(minp), int(maxp), charp, pwd)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(raw) for raw in file.readlines()]
    if args.part == 1:
        print(len([p for p in data if p.is_valid]))
    else:
        print(len([p for p in data if p.is_valid_new]))
    print(time() - t)
