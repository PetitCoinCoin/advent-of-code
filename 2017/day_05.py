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

def walk_through(data: list, part_one: bool) -> int:
    steps = 0
    i = 0
    while 0 <= i < len(data):
        val = data[i]
        if part_one or val < 3:
            data[i]= data[i] + 1
        else:
            data[i]= data[i] - 1
        i += val
        steps += 1
    return steps


if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(val) for val in file.readlines()]
    print(walk_through(data, args.part == 1))
