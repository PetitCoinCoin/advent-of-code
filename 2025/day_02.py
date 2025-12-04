from itertools import batched
from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def parse_input(item: str) -> range:
    digits = list(map(int, item.split("-")))
    return range(digits[0], digits[-1] + 1)

def get_all_valid(item: range, *, part_two: bool = False) -> int:
    invalid_ids = set()
    for _id in item:
        str_id = str(_id)
        len_id = len(str_id)
        for i in range(len_id // 2, 0, -1) if part_two else (len_id // 2,):
            if (part_two and len_id % i) or (not part_two and len_id %  2):
                continue
            if len(set(batched(str_id, i))) == 1:
                invalid_ids.add(_id)
                break
    return sum(invalid_ids)

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(item) for item in file.read().strip().split(",")]
    print(sum(
        get_all_valid(item, part_two=args.part == 2)
        for item in data
    ))
    print(time() - t)
