from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def parse_input(blocks: list[str]) -> tuple:
    fresh = [
        (int(line.split("-")[0]), int(line.split("-")[1]))
        for line in blocks[0].split("\n")
    ]
    ids = [int(x) for x in blocks[1].split("\n")]
    return fresh, ids

def concat_ranges(items: list) -> int:
    items.sort()
    indep = [items[0]]
    for item in items[1:]:
        for i, concat_item in enumerate(indep):
            if concat_item[0] <= item[0] <= concat_item[1]:
                indep[i] = (concat_item[0], max(concat_item[1], item[1]))
                break
        else:
            indep.append(item)
    return sum(item[1] - item[0] + 1 for item in indep)


if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data, ingredients = parse_input(file.read().strip().split("\n\n"))
    if args.part == 1:
        print(sum(
            any(ingredient in range(fresh_range[0], fresh_range[1] + 1) for fresh_range in data)
            for ingredient in ingredients
        ))
    else:
        print(concat_ranges(data))
    print(time() - t)
