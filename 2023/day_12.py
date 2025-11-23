import argparse

from functools import cache
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

def get_arrangements(springs: str, operationals: list) -> int:
    if not operationals:
        return 1 if "#" not in springs else 0
    current, operationals = operationals[0], operationals[1:]
    min_length = current + sum(operationals) + len(operationals) - 1
    delta = len(springs) - min_length
    result = 0
    for i in range(delta):
        if "#" in springs[:i]:
            break
        next_i = i + current
        if next_i <= len(springs) and "." not in springs[i:next_i] and springs[next_i:next_i + 1] != "#":
            result += get_arrangements(springs[next_i + 1:], operationals)
    return result

@cache
def get_arrangements_2(springs: str, operationals: tuple) -> int:
    if not operationals:
        return 1 if "#" not in springs else 0
    current, operationals = operationals[0], operationals[1:]
    min_length = current + sum(operationals) + len(operationals) - 1
    delta = len(springs) - min_length
    result = 0
    for i in range(delta):
        if "#" in springs[:i]:
            break
        next_i = i + current
        if next_i <= len(springs) and "." not in springs[i:next_i] and springs[next_i:next_i + 1] != "#":
            result += get_arrangements_2(springs[next_i + 1:], operationals)
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        arrangements = [get_arrangements(data[i], [int(x) for x in data[i + 1].split(",")]) for i in range(0, len(data), 2)]
    else:
        arrangements = [
            get_arrangements_2(
                "?".join(5 * [data[i]]),
                5 * tuple(int(x) for x in data[i + 1].split(","))
            )
            for i in range(0, len(data), 2)
        ]
    print(sum(arrangements))
    print(time() - t)

