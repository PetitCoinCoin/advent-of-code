import argparse

from collections import deque
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

def collapse(raw: str) -> str:
    i = 1
    de = deque(raw[0])
    while i < len(raw):
        if not len(de):
            de.append(raw[i])
        else:
            previous = de.pop()
            if raw[i].lower() == previous.lower() and raw[i] != previous:
                pass
            else:
                de.append(previous)
                de.append(raw[i])
        i += 1
    return "".join(de)

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read()
    first_reaction = collapse(data)
    if args.part == 1:
        print(len(first_reaction))
    else:
        min_polymer = 50000
        for unit in "abcdefghijklmnopqrstuvwxyz":
            final = collapse("".join(x for x in first_reaction if x.lower() != unit))
            if len(final) < min_polymer:
                min_polymer = len(final)
        print(min_polymer)
