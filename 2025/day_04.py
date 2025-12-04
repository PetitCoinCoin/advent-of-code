from pathlib import Path
from time import time

from py_utils.grids import get_next
from py_utils.parsers import parse_args, parse_grid_of_char

def get_accessed_rolls() -> set:
    accessed = set()
    for roll in data:
        if sum(
            next_roll in data
            for next_roll in get_next(roll, with_diagonals=True)
        ) < 4:
            accessed.add(roll)
    return accessed

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data, _, _ = parse_grid_of_char(file.read().strip().split("\n"), "@", as_set=True)
    if args.part == 1:
        print(len(get_accessed_rolls()))
    else:
        init_rolls = len(data)
        while True:
            to_remove = get_accessed_rolls()
            if not to_remove:
                break
            data -= to_remove
        print(init_rolls - len(data))   
    print(time() - t)
