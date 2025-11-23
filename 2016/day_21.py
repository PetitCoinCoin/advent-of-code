import argparse
import re

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

def rotate_right(password: str, steps: int) -> str:
    return password[-steps:] + password[:-steps]

def rotate_left(password: str, steps: int) -> str:
    return password[steps:] + password[:steps]

def rotate_letter(password: str, letter: str) -> str:
    idx = password.find(letter)
    if idx < 0:
        return password
    steps = (idx + 2) % len(password) if idx >= 4 else (idx + 1) % len(password)
    return rotate_right(password, steps)

def scramble(raw: str, password: str, unscramble: bool = False) -> str:
    if raw.startswith("swap position"):
        indexes = [int(x) for x in re.findall(r"(\d+)", raw)]
        idx1 = min(indexes)
        idx2 = max(indexes)
        return password[:idx1] + password[idx2] + password[idx1 + 1:idx2] + password[idx1] + password[idx2 + 1:]
    if raw.startswith("swap letter"):
        letter1 = raw.split(" with letter ")[0][-1]
        letter2 = raw.split(" with letter ")[1][0]
        return password.replace(letter1, ".").replace(letter2, letter1).replace(".", letter2)
    if raw.startswith("rotate left"):
        steps = int(re.findall(r"(\d+)", raw)[0])
        return rotate_right(password, steps) if unscramble else rotate_left(password, steps)
    if raw.startswith("rotate right"):
        steps = int(re.findall(r"(\d+)", raw)[0])
        return rotate_left(password, steps) if unscramble else rotate_right(password, steps)
    if raw.startswith("rotate based"):
        letter = raw.strip()[-1]
        if unscramble:
            step = 1
            while rotate_letter(rotate_left(password, step), letter) != password:
                step += 1
            return rotate_left(password, step)
        return rotate_letter(password, letter)
    if raw.startswith("move"):
        idx1, idx2 = (int(x) for x in re.findall(r"(\d+)", raw))
        if unscramble:
            idx1, idx2 = idx2, idx1
        if idx1 < idx2:
            return password[:idx1] + password[idx1 + 1:idx2 + 1] + password[idx1] + password[idx2 + 1:]
        return password[:idx2] + password[idx1] + password[idx2:idx1] + password[idx1 + 1:]
    if raw.startswith("reverse"):
        idx1, idx2 = (int(x) for x in re.findall(r"(\d+)", raw))
        return password[:idx1] + password[idx1:idx2 + 1][::-1] + password[idx2 + 1:]
    raise NotImplementedError(raw)

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        instructions = file.readlines()
    if args.part == 1:
        data = "abcdefgh"
        for instruction in instructions:
            data = scramble(instruction, data)
        print(data)
    else:
        data = "fbgdceah"
        for instruction in instructions[::-1]:
            data = scramble(instruction, data, True)
        print(data)
