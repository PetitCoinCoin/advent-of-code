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

PICOSEC = 100

def parse_input(raw: str, i: int) -> tuple:
    start = None
    end = None
    for r, char in enumerate(raw):
        data[complex(r, -i)] = char
        if char == "S":
            start = complex(r, -i)
            data[complex(r, -i)] = "."
        if char == "E":
            end = complex(r, -i)
            data[complex(r, -i)] = "."
    return start, end

def get_race() -> dict:
    race = {}
    previous = None
    position = start
    i = 0
    while position != end:
        race[position] = i
        for d in (1, -1, 1j, -1j):
            if data.get(position + d, "#") == "." and position + d != previous:
                previous = position
                position += d
                break
        i += 1
    race[end] = i
    return race

def reachables(pos: complex, dist: int) -> set:
    reached = set()
    while dist > 1:
        for r in range(dist + 1):
            for d in (
                complex(r, r - dist),
                complex(r, -(r - dist)),
                complex(-r, r - dist),
                complex(-r, -(r - dist))
            ):
                if data.get(pos + d, "#") == ".":
                    reached.add((dist, pos + d))
        dist -= 1
    return reached

def cheat(cheat_move: int) -> int:
    walls = set()
    for position, dist in race.items():
        for moves, cheat_pos in reachables(position, cheat_move):
            if data.get(cheat_pos, "#") == "." and race[cheat_pos] - dist >= PICOSEC + moves:
                walls.add((position, cheat_pos))
    return len(walls)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    start = None
    end = None
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        i = 0
        while line := file.readline():
            s, e = parse_input(line.strip(), i)
            if s:
                start = s
            if e:
                end = e
            i += 1
    race = get_race()
    print(cheat(2 if args.part == 1 else 20))
    print(time() - t)
