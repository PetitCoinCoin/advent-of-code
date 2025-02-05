import argparse
import re

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
class Machine:
    xa: int = 0
    ya: int = 0
    xb: int = 0
    yb: int = 0
    xp: int = 0
    yp: int = 0

def parse_input(raw: str, *, is_part_two: bool) -> Machine:
    digits = re.findall(r"(\d+)", raw)
    m = Machine(
        xa=int(digits[0]),
        ya=int(digits[1]),
        xb=int(digits[2]),
        yb=int(digits[3]),
        xp=int(digits[4]),
        yp=int(digits[5]),
    )
    if is_part_two:
        m.xp += 10000000000000
        m.yp += 10000000000000
    return m

def solve(m: Machine, *, is_part_two: bool) -> int:
    """
        Just solve:
        a * m.xa + b * m.xb = m.xp
        a * m.ya + b * m.yb = m.yp
    """
    b = (m.xp * m.ya - m.yp * m.xa) / (m.xb * m.ya - m.xa * m.yb)
    a = (m.xp - b * m.xb) / m.xa
    if b < 0 or a < 0 or not float(a).is_integer() or not float(b).is_integer():
        return 0
    if not is_part_two and (b > 100 or a > 100):
        return 0
    return 3 * int(a) + int(b)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(lines, is_part_two=args.part == 2) for lines in file.read().split("\n\n")]
    print(sum(solve(m, is_part_two= args.part == 2) for m in data))
    print(time() - t)
