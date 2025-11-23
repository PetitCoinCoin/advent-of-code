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

def is_possible(raw: str) -> bool:
    sides = [int(x) for x in re.findall(r"(\d+)\s+(\d+)\s+(\d+)", raw)[0]]
    for i in range(3):
        if sides[i] >= sides[(i + 1) % 3] + sides[(i + 2) % 3]:
            return False
    return True

def is_vertically_possible(rows: list) -> int:
    rows = [row.split(" ") for row in rows]
    raw0 = raw1 = raw2 = ""
    for row in rows:
        row = [r for r in row if r]
        raw0 += f"{row[0]} "
        raw1 += f"{row[1]} "
        raw2 += f"{row[2]} "
    return sum([is_possible(raw) for raw in (raw0, raw1, raw2)])


if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.readlines()
    if args.part == 1:
        print(sum([is_possible(raw) for raw in data]))
    else:
        i = 0
        possible = 0
        while i < len(data):
            possible += is_vertically_possible(data[i: i + 3])
            i += 3
        print(possible)
