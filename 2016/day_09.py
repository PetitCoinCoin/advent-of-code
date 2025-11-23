import argparse

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

def parse_marker(raw: str) -> tuple:
    count = int(raw.split("x")[0])
    mult = int(raw.split("x")[1])
    return count, mult

def get_length(raw: str, part_one: bool = True) -> int:
    if "(" not in raw:
        return len(raw)
    result = 0
    i = 0
    while i < len(raw):
        if raw[i] == "(":
            d = 4
            while raw[i + d] != ")":
                d += 1
            count, mult = parse_marker(raw[i + 1: i + d])
            if part_one:
                result += mult * count
            else:
                result += mult * get_length(raw[i + d + 1:i + d + 1 + count], part_one)
            i += d + count + 1
        else:
            result += 1
            i += 1
    return result

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read()
    print(get_length(data, args.part == 1))
