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

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().split("\n")]
    if args.part == 1:
        print(sum(data))
    else:
        seen = dict()
        frequency = 0
        i = 0
        while not seen.get(frequency):
            seen[frequency] = True
            frequency += data[i]
            i = (i + 1) % len(data)
        print(frequency)
