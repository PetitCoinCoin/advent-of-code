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
        ELVES = int(file.read().strip())
    if args.part == 1:
        # result is ELVES - bitwise NOT of bin(ELVES)
        print(ELVES - (ELVES ^ ((1 << ELVES.bit_length()) - 1)))
    else:
        # used naive implementation to get first result and detect pattern
        last_cubic = 1
        while last_cubic * 3 < ELVES:
            last_cubic *= 3
        if ELVES <= 2 * last_cubic:
            print(ELVES - last_cubic)
        else:
            print(2 * ELVES - 3 * last_cubic)
