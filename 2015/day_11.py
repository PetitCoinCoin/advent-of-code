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

CHAR = "abcdefghjkmnpqrstuvwxyz"

def next_char(char: str) -> str:
    idx = CHAR.find(char)
    return CHAR[(idx + 1) % len(CHAR)]

def increment(pwd: str) -> str:
    idx = len(pwd) - 1
    pwd = pwd[:idx] + next_char(pwd[idx]) + pwd[idx + 1:]
    while pwd[idx] == "a":
        idx -= 1
        pwd = pwd[:idx] + next_char(pwd[idx]) + pwd[idx + 1:]
    return pwd

def is_valid(pwd: str) -> bool:
    for i in range(len(pwd) - 2):
        if pwd[i:i + 3] in CHAR:
            break
    else:
        return False
    double = 0
    i = 0
    while i < len(pwd) - 1:
        if pwd[i] == pwd[i + 1]:
            double += 1
            i += 2
        else:
            i+= 1
        if double == 2:
            return True
    return False

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip()
    while not is_valid(data):
        data = increment(data)
    if args.part == 1:
        print(data)
    else:
        data = increment(data)
        while not is_valid(data):
            data = increment(data)
        print(data)
