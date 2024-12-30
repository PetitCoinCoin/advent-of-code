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

def energize(start: tuple, direction: str, records: dict, floor: list) -> None:
    if direction in records.get(start, []):
        return None
    records[start] = records.get(start, []) + [direction]
    i, j = start
    if direction == "right":
        if j == len(floor[i]) - 1:
            return None
        k = 1
        while j + k < len(floor[i]) and floor[i][j + k] in (".", "-"):
            records[(i, j + k)] = records.get((i, j + k), []) + [direction]
            k += 1
        if j + k == len(floor[i]):
            return None
        if floor[i][j + k] in "|/":
            energize((i, j + k), "up", records, floor)
        if floor[i][j + k] in "|\\":
            energize((i, j + k), "down", records, floor)
    elif direction == "left":
        if j == 0:
            return None
        k = 1
        while j - k >= 0 and floor[i][j - k] in (".", "-"):
            records[(i, j - k)] = records.get((i, j - k), []) + [direction]
            k += 1
        if j - k < 0:
            return None
        if floor[i][j - k] in "|\\":
            energize((i, j - k), "up", records, floor)
        if floor[i][j - k] in "|/":
            energize((i, j - k), "down", records, floor)
    elif direction == "up":
        if i == 0:
            return None
        k = 1
        while i - k >= 0 and floor[i - k][j] in (".", "|"):
            records[(i - k, j)] = records.get((i - k, j), []) + [direction]
            k += 1
        if i - k < 0:
            return None
        if floor[i - k][j] in "-\\":
            energize((i - k, j), "left", records, floor)
        if floor[i - k][j] in "-/":
            energize((i - k, j), "right", records, floor)
    else:  # down
        if i == len(floor) - 1:
            return None
        k = 1
        while i + k < len(floor) and floor[i + k][j] in (".", "|"):
            records[(i + k, j)] = records.get((i + k, j), []) + [direction]
            k += 1
        if i + k == len(floor):
            return None
        if floor[i + k][j] in "-\\":
            energize((i + k, j), "right", records, floor)
        if floor[i + k][j] in "-/":
            energize((i + k, j), "left", records, floor)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        energized = {}
        energize((0, 0), "down", energized, data)
        print(len(energized.keys()))
    else:
        # Not proud on this one, but hey, it works and I had
        # other stuff to do on a Saturday!
        from_up = []
        for i, val in enumerate(data[0]):
            energized = {}
            if val in ".|":
                directions = ["down"]
            elif val == "\\":
                directions = ["right"]
            elif val == "/":
                directions = ["left"]
            else:  # -
                directions = ["right", "left"]
            for direction in directions:
                energize((0, i), direction, energized, data)
            from_up.append(len(energized.keys()))
        from_down = []
        for i, val in enumerate(data[-1]):
            energized = {}
            if val in ".|":
                directions = ["up"]
            elif val == "\\":
                directions = ["left"]
            elif val == "/":
                directions = ["right"]
            else:  # -
                directions = ["right", "left"]
            for direction in directions:
                energize((len(data) - 1, i), direction, energized, data)
            from_down.append(len(energized.keys()))
        from_left = []
        for i, val in enumerate(data):
            energized = {}
            if val[0] in ".-":
                directions = ["right"]
            elif val[0] == "\\":
                directions = ["down"]
            elif val[0] == "/":
                directions = ["up"]
            else:  # -
                directions = ["down", "up"]
            for direction in directions:
                energize((i, 0), direction, energized, data)
            from_left.append(len(energized.keys()))
        from_right = []
        for i, val in enumerate(data):
            energized = {}
            if val[-1] in ".-":
                directions = ["left"]
            elif val[-1] == "\\":
                directions = ["up"]
            elif val[-1] == "/":
                directions = ["down"]
            else:  # -
                directions = ["down", "up"]
            for direction in directions:
                energize((i, len(val) - 1), direction, energized, data)
            from_right.append(len(energized.keys()))
        print(max(
            max(from_right),
            max(from_down),
            max(from_left),
            max(from_up),
        ))
    print(time() - t)

