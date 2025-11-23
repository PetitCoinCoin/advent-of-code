import argparse
import math

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

def find_corner(val: int) -> tuple:
    half_dist = 0
    for v in range(val, 0, -1):
        root_square = math.sqrt(v)
        if root_square.is_integer():
            half_dist = math.floor(root_square / 2)
            break
    return int(root_square), half_dist

def find_distance(val: int) -> int:
    root, half_dist = find_corner(val)
    if root % 2:
        position = half_dist + half_dist * -1j
    else:
        position = - (half_dist - 1) + half_dist * 1j
    square = root ** 2
    if square == val:
        return abs(position.real) + abs(position.imag)
    for i in range(1, val - square + 1):
        if root % 2:
            if i == 1:
                position += 1
            elif i <= 1 + root:
                position += 1j
            else:
                position -= 1
        else:
            if i == 1:
                position -= 1
            elif i <= 1 + root:
                position -= 1j
            else:
                position += 1
    return int(abs(position.real) + abs(position.imag))

def walk() -> int:
    values = {
        0 + 0j: 1,
        1 + 0j: 1,
    }
    current = 1 + 0j
    while values[current] < VALUE:
        if values.get(current - 1):
            if values.get(current + 1j):
                delta = 1
            else:
                delta = 1j
        else:
            if values.get(current - 1j):
                delta = -1
            else:
                if values.get(current + 1):
                    delta = -1j
                else:
                    delta = 1
        current += delta
        values[current] = sum([values.get(current + d, 0) for d in [1, 1 + 1j, 1j, -1 + 1j, -1, -1 -1j, -1j, 1 - 1j]])
    return values[current]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        VALUE = int(file.read().strip())
    if args.part == 1:
        print(find_distance(VALUE))
    else:
        print(walk())
