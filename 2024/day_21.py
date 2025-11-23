import argparse

from functools import cache
from heapq import heappop, heappush
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

NUM_KB= {
    1: "0",
    2: "A",
    1j: "1",
    1 + 1j: "2",
    2 + 1j: "3",
    2j: "4",
    1 + 2j: "5",
    2 + 2j: "6",
    3j: "7",
    1 + 3j: "8",
    2 + 3j: "9",
}

DIR_KB = {
    0: "<",
    1: "v",
    2: ">",
    1 + 1j: "^",
    2 + 1j: "A",
}

DIR_MAP = {
    "<": -1,
    "v": -1j,
    ">": 1,
    "^": 1j,
}

def is_safe(position: complex, path: str, mapping: dict) -> bool:
    for direction in path:
        if mapping.get(position + DIR_MAP[direction]) is None:
            return False
        position += DIR_MAP[direction]
    return True

@cache
def move_to_kb(position: complex, key: str, *, is_directionnal: bool = True) -> tuple:
    mapping = DIR_KB if is_directionnal else NUM_KB
    queue = []
    options = []  # set()
    seen = {}
    heappush(queue, (0, str(position), ""))
    while queue:
        length, str_pos, path = heappop(queue)
        pos = complex(str_pos)
        if mapping[pos] == key:
            opti_path = "".join(sorted(path))
            if is_safe(position, opti_path, mapping):
                options.append(opti_path + "A")
            if opti_path[::-1] != opti_path and is_safe(position, opti_path[::-1], mapping):
                options.append(opti_path[::-1] + "A")
            if not options:
                options.append(path + "A")
            return pos, options
        seen[pos] = True
        for k, d in DIR_MAP.items():
            if mapping.get(pos + d) is not None and pos + d not in seen:
                heappush(queue, (length + 1, str(pos + d), path + k))
    return position, options

@cache
def iterate_moves(code: str, loop: int = 0) -> set:
    is_directionnal = False
    for c in code:
        if c in "<^>v":
            is_directionnal = True
            break
    position = 2 + 1j if is_directionnal else 2
    res = 0
    for c in code:
        position, options = move_to_kb(position, c, is_directionnal=is_directionnal)
        if not loop:
            res += min([len(opt) for opt in options])
        else:
            res += min(iterate_moves(opt, loop - 1) for opt in options)
    return res

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    print(sum(
        int(code[:-1]) * iterate_moves(code, 2 if args.part == 1 else 25)
        for code in data
        )
    )
    print(time() - t)
