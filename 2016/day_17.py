import argparse

from collections import deque
from hashlib import md5
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

DOORS_DELTA = [("U", (0, -1)),  ("D", (0, 1)), ("L", (-1, 0)), ("R", (1, 0))]

def find_next(position: tuple, passcode: str) -> list:
    doors = [
        DOORS_DELTA[i]
        for i, c in enumerate(md5(passcode.encode()).hexdigest()[:4])
        if c in "bcdef"
    ]
    return [
        (direction, (position[0] + step[0], position[1] + step[1]))
        for direction, step in doors
        if position[0] + step[0] in range(4) and position[1] + step[1] in range(4)
    ]

def bfs(part_one: bool = True) -> str:
    start = (0, 0)
    queue = deque()
    queue.append((PASSCODE, start))
    seen = set(PASSCODE)
    valid = deque()
    while queue:
        passcode, position = queue.popleft()
        for direction, new_position in find_next(position, passcode):
            if new_position == (3, 3):
                if part_one:
                    return passcode + direction
                valid.append(passcode + direction)
            elif passcode + direction not in seen:
                seen.add(passcode + direction)
                queue.append((passcode + direction, new_position))
    return valid.pop()

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        PASSCODE = file.read().strip()
    if args.part == 1:
        print(bfs()[len(PASSCODE):])
    else:
        print(len(bfs(False)) - len(PASSCODE))
