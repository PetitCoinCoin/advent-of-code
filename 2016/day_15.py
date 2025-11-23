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
    digits = [int(x) for x in re.findall(r"\d+", raw) if int(x)]
    position = (digits[-1] + digits[0]) % digits[1] 
    return position, digits[1]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(raw) for raw in file.readlines()]
    if args.part == 2:
        data.append(parse_input("Disc #7 has 11 positions; at time=0, it is at position 0."))
    start = 1
    while True:
        for position, count in data:
            if (position + start) % count:
                break
        else:
            print(start)
            break
        start += 1
