from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def dial(*, with_new_method: bool = False) -> int:
    is_zero = 0
    position = 50
    for direction in data:
        prev_position = position
        dist = int(direction[1:])
        if direction[0] == "R":
            position += dist
            if with_new_method and position > 100:
                is_zero += position // 100 + (0 if position % 100 else -1)
        else:
            position -= dist
            if with_new_method and position < 0:
                is_zero -= position // 100 + (0 if prev_position else 1)
        position %= 100
        if not position:
            is_zero += 1
    return is_zero

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    print(dial(with_new_method=args.part == 2))
    print(time() - t)
