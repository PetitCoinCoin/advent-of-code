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

DIRECTIONS_MAP = {
    "up": 1j,
    "down": -1j,
    "right": 1,
    "left": -1,
    "stop": 0,
}

def parse_input(steps: dict, raw: str, i: int) -> complex | None:
    for j, char in enumerate(raw):
        if char != " ":
            steps[complex(j, -i)] = char
            if not i:
                return complex(j, -i)
    return None

def get_next_step(steps: dict, current: complex, direction: str) -> tuple:
    if steps[current] in "|-":
        return direction, current + DIRECTIONS_MAP.get(direction, 0)
    if steps[current] == "+":
        if direction in ("up", "down"):
            if steps.get(current + DIRECTIONS_MAP["right"]):
                new_dir = "right" 
            elif steps.get(current + DIRECTIONS_MAP["left"]):
                new_dir ="left"
            else:
                new_dir = "stop"
        if direction in ("right", "left"):
            if steps.get(current + DIRECTIONS_MAP["up"]):
                new_dir = "up" 
            elif steps.get(current + DIRECTIONS_MAP["down"]):
                new_dir ="down"
            else:
                new_dir = "stop"
        return new_dir, current + DIRECTIONS_MAP[new_dir]
    # letter
    if steps.get(current + DIRECTIONS_MAP[direction]):
        return direction, current + DIRECTIONS_MAP.get(direction, 0)
    # letter in corner
    if direction in ("up", "down"):
        if steps.get(current + DIRECTIONS_MAP["right"]):
            new_dir = "right" 
        elif steps.get(current + DIRECTIONS_MAP["left"]):
            new_dir ="left"
        else:
            new_dir = "stop"
    if direction in ("right", "left"):
        if steps.get(current + DIRECTIONS_MAP["up"]):
            new_dir = "up" 
        elif steps.get(current + DIRECTIONS_MAP["down"]):
            new_dir ="down"
        else:
            new_dir = "stop"
    return new_dir, current + DIRECTIONS_MAP[new_dir]

def follow_path(steps: dict, start: complex) -> tuple:
    word = ""
    step = start
    count = 1
    direction, next_step = get_next_step(steps, step, "down")
    while next_step != step:
        # print(step, steps[step], next_step, steps[next_step])
        step = next_step
        count += 1
        if steps[step] not in "|-+":
            word += steps[step]
        direction, next_step = get_next_step(steps, step, direction)
    return count, word

if __name__ == "__main__":
    args = _parse_args()
    data = {}
    start = None
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        i = 0
        while line := file.readline():
            value = parse_input(data, line, i)
            if not i:
                start = value
            i += 1
    count, word = follow_path(data, start)
    if args.part == 1:
        print(word)
    else:
        print(count)
