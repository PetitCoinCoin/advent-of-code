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

SUBJECT_NUMBER = 7
DIVIDER = 20201227

def get_loop_size(pk: int) -> int:
    value = 1
    loop_size = 0
    while value != pk:
        value = (value * SUBJECT_NUMBER) % DIVIDER
        loop_size += 1
    return loop_size

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        card_pk, door_pk = tuple(int(x) for x in file.read().strip().split("\n"))
    if args.part == 1:
        card_loop_size = get_loop_size(card_pk)
        # door_loop_size = get_loop_size(door_pk)
        print(pow(door_pk, card_loop_size, DIVIDER))
        # print(pow(card_pk, door_loop_size, DIVIDER))
    else:
        raise NotImplementedError
    print(time() - t)
