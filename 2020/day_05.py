import argparse

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

def seat_id(raw: str) -> int:
    return int(
        raw.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"),
        2,
    )

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    seat_ids = {seat_id(seat) for seat in data}
    if args.part == 1:
        print(max(seat_ids))
    else:
        missing_ids = set(range(1024)) - seat_ids
        for seat in missing_ids:
            if seat + 8 in seat_ids and seat - 8 in seat_ids:
                print(seat)
                break
    print(time() - t)
