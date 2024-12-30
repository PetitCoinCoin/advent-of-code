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

def get_next(serie: list) -> int:
    if not any(serie):
        return 0
    diff = []
    for i in range(1, len(serie)):
        diff.append(serie[i] - serie[i - 1])
    return serie[-1] + get_next(diff)

def get_previous(serie: list) -> int:
    if not any(serie):
        return 0
    diff = []
    for i in range(len(serie) - 1, 0, -1):
        diff.insert(0, serie[i] - serie[i - 1])
    return serie[0] - get_previous(diff)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = []
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            data.append([int(x.strip()) for x in line.split(" ")])
    if args.part == 1:
        all_next = [get_next(serie) for serie in data]
        print(sum(all_next))
    else:
        all_previous = [get_previous(serie) for serie in data]
        print(sum(all_previous))
    print(time() - t)

