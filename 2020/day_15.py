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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split(",")]
    numbers = {val: i + 1 for i, val in enumerate(data)}
    total_round = 2020 if args.part == 1 else 30000000
    round_nb = len(data) + 1
    spoken = data[-1]
    prev_spoken_round = len(data)
    while round_nb <= total_round:
        spoken = round_nb - 1 - prev_spoken_round
        data.append(spoken)
        prev_spoken_round = numbers.get(spoken, round_nb)
        numbers[spoken] = round_nb
        round_nb += 1
    print(spoken)
    print(time() - t)
