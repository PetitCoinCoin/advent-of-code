import argparse

from pathlib import Path

DIRECTIONS_MAP = {
    "^": 1j,
    ">": 1,
    "v": -1j,
    "<": -1,
}

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

def get_next_house(current: complex, direction: str) -> complex:
    return current + DIRECTIONS_MAP[direction]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read()
    if args.part == 1:
        current = 0 + 0j
        houses = [current]
        for direction in data:
            current = get_next_house(current, direction)
            houses.append(current)
        print(len(set(houses)))
    else:
        santa_current = 0 + 0j
        robo_current = 0 + 0j
        houses = [0 + 0j]
        for step, direction in enumerate(data):
            if step % 2:
                robo_current = get_next_house(robo_current, direction)
                houses.append(robo_current)
            else:
                santa_current = get_next_house(santa_current, direction)
                houses.append(santa_current)
        print(len(set(houses)))
