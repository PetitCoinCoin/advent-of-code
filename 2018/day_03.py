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

def parse_input(raw: str) -> tuple:
    pattern = r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)"
    elements = [int(x) for x in re.findall(pattern, raw)[0]]
    claims = set()
    for r in range(elements[3]):
        for j in range(elements[4]):
            claims.add(complex(elements[1] + r, -elements[2] - j))
    return elements[0], claims

def count_intersections(claims: dict) -> int:
    count = 0
    seen = dict()
    for area in claims.values():
        for square in area:
            if seen.get(square, 0) > 1:
                continue
            if seen.get(square, 0) == 1:
                seen[square] += 1
                count += 1
                continue
            seen[square] = 1
    return count

def get_non_overlap(claims: dict) -> int:
    max_id = max(claims.keys())
    for i in range(1, max_id + 1):
        for j in range(1, max_id + 1):
            if i != j and len(claims[i].intersection(claims[j])):
                break
        else:
            return i

if __name__ == "__main__":
    args = _parse_args()
    data = dict()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line:= file.readline():
            key, value = parse_input(line)
            data[key] = value
    if args.part == 1:
        print(count_intersections(data))
    else:
        print(get_non_overlap(data))
