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

def is_trap(tiles: list) -> bool:
    if sum(tiles) == 1 and (tiles[0] or tiles[-1]):
        return True
    if sum(tiles) == 2 and (not tiles[-1] or not tiles[0]):
        return True
    return False

def get_traps(tiles: list) -> list:
    next_tiles = list()
    for i in range(len(tiles)):
        if i == 0:
            sub_tiles = [False] + tiles[:2]
        elif i == len(tiles) - 1:
            sub_tiles = tiles[-2:] + [False]
        else:
            sub_tiles = tiles[i - 1: i + 2]
        next_tiles.append(is_trap(sub_tiles))
    return next_tiles

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        FIRST_ROW = file.read().strip()
    if args.part == 1:
        ROW_COUNT = 40
    else:
        ROW_COUNT = 400000
    data = [[char == "^" for char in FIRST_ROW]]
    for row in range(1, ROW_COUNT):
        data.append(get_traps(data[row - 1]))
    # I found it easier to think in terms of traps, so I have to adapt to find safe tiles count.
    print(ROW_COUNT * len(FIRST_ROW) - sum([sum(row) for row in data]))
