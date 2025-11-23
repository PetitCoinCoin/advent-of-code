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

def blink(stones: dict) -> dict:
    result = {}
    for value, mul in stones.items():
        if not value:
            result[1] = result.get(1, 0) + mul
        elif not len(str(value)) % 2:
            val = str(value)
            val_1 = int(val[len(val) // 2:])
            val_2 = int(val[:len(val) // 2])
            result[val_1] = result.get(val_1, 0) + mul
            result[val_2] = result.get(val_2, 0) + mul
        else:
            result[value * 2024] = result.get(value * 2024, 0) + mul
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        for x in file.read().split():
            data[int(x)] = 1
    loops = 25 if args.part == 1 else 75
    for _ in range(loops):
        data = blink(data)
    print(sum(data.values()))
    print(time() - t)
