import argparse

from collections import deque
from dataclasses import dataclass
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

@dataclass
class Node:
    nb_children: int
    nb_meta: int
    children: list
    meta: int

def get_metadata(notes: deque, *, is_part_two: bool = False) -> int:
    nb_children = notes.popleft()
    nb_meta = notes.popleft()
    if not nb_children:
        cpt = 0
        val = 0
        while cpt < nb_meta:
            val += notes.popleft()
            cpt += 1
        return val
    children = {}
    val = 0
    for i in range(nb_children):
        if is_part_two:
            children[i + 1] = get_metadata(notes, is_part_two=True)
        else:
            val += get_metadata(notes)
    cpt = 0
    while cpt < nb_meta:
        idx = notes.popleft()
        val += children.get(idx, 0) if is_part_two else idx
        cpt += 1
    return val

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = deque(int(x) for x in file.read().split(" "))
    print(get_metadata(data, is_part_two=args.part == 2))
    print(time() - t)
