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

START = [".#.", "..#", "###"]

def x_flip(state: str) -> str:
    return "/".join(row[::-1] for row in state.split("/"))

def y_flip(state: str) -> str:
    return "/".join(state.split("/")[::-1])

def rotate_right(state: str) -> str:
    rows = state.split("/")
    rotate = list()
    n = len(rows)
    for j in range(n):
        new_row = ""
        for i in range(n):
            new_row += rows[n - 1 - i][j]
        rotate.append(new_row)
    return "/".join(rotate)

def get_missing(rules: dict, key: str, value: str) -> None:
    key_x_flip = x_flip(key)
    key_y_flip = y_flip(key)
    key_xy_flip = y_flip(key_x_flip)  # = rotate + rotate
    key_rotate = rotate_right(key)
    key_rotate_x_flip = x_flip(key_rotate)
    key_rotate_y_flip = y_flip(key_rotate)
    key_rotate_xy_flip = y_flip(key_rotate_x_flip)  # = rotate + rotate + rotate
    for additional_key in (
        key_x_flip,
        key_y_flip,
        key_xy_flip,
        key_rotate,
        key_rotate_x_flip,
        key_rotate_y_flip,
        key_rotate_xy_flip,
    ):
        if not rules.get(additional_key):
            rules[additional_key] = value

def generate_art(rules: dict, start: list) -> list:
    pattern = []
    if not len(start) % 2:
        n = 2
    else:
        n = 3
    for i in range(len(start) // n):
        pattern_i = ""
        pattern_i_1 = ""
        pattern_i_2 = ""
        pattern_i_3 = ""
        for j in range(len(start) // n):
            key = "/".join([row[j * n:j * n + n] for row in start[i * n:i * n + n]])
            value = rules[key]
            pattern_i += value.split("/")[0]
            pattern_i_1 += value.split("/")[1]
            pattern_i_2 += value.split("/")[2]
            if n == 3:
                pattern_i_3 += value.split("/")[3]
        pattern += [pattern_i, pattern_i_1, pattern_i_2]
        if n == 3:
            pattern.append(pattern_i_3)
    return pattern

if __name__ == "__main__":
    args = _parse_args()
    data = dict()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            key, value = line.strip().split(" => ")
            data[key] = value
            get_missing(data, key, value)
    iterations = 5 if args.part == 1 else 18
    i = 0
    pattern = START
    while i < iterations:
        pattern = generate_art(data, pattern)
        i += 1
    print(sum(char == "#" for row in pattern for char in row))
