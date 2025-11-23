import argparse
import re

from copy import deepcopy
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

C_SIZE = 50
R_SIZE = 6

def operate(raw: str, data: dict) -> dict:
    updated_data = deepcopy(data)
    digits = [int(x) for x in re.findall(r"\d+", raw)]
    if "rect" in raw:
        for c in range(digits[0]):
            for r in range(digits[1]):
                updated_data[(r, c)] = True
    elif "column" in raw:
        for r in range(R_SIZE):
            updated_data[((r + digits[1]) % R_SIZE, digits[0])] = data[(r, digits[0])]
    else:  # row
        for c in range(C_SIZE):
            updated_data[(digits[0], (c + digits[1]) % C_SIZE)] = data[(digits[0], c)]
    return updated_data

def prettier(data: dict) -> str:
    result = []
    for r in range(R_SIZE):
        result.append(
            "".join([
                "#" if data[(r, c)]
                else " "
                for c in range(C_SIZE)
            ])
        )
    return "\n".join(result)

if __name__ == "__main__":
    args = _parse_args()
    data = dict()
    for r in range(R_SIZE):
        for c in range(C_SIZE):
            data[(r, c)] = False
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            data = operate(line, data)
    if args.part == 1:
        print(sum(data.values()))
    else:
        print(prettier(data))
