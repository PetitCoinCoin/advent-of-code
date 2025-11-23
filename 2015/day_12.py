import argparse
import json

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

def find_sum(item: any, ignore_red: bool = False) -> int:
    if isinstance(item, int):
        return item
    if isinstance(item, dict):
        if ignore_red and "red" in item.values():
            return 0
        return sum([find_sum(val, ignore_red) for val in item.values()])
    if isinstance(item, list):
        return sum([find_sum(val, ignore_red) for val in item])
    return 0

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read()
    if args.part == 1:
        print(find_sum(json.loads(data)))
    else:
        print(find_sum(json.loads(data), ignore_red=True))
