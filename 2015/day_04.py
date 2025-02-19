import argparse

from hashlib import md5
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

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip()
    if args.part == 1:
        expected = "00000"
    else:
        expected = "000000"
    result = 0
    while not md5(f"{data}{result}".encode()).hexdigest().startswith(expected):
        result += 1
    print(result)
