import argparse

from collections import defaultdict
from contextlib import suppress
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

def part_1() -> int:
    result = 0
    col = len(data[0])
    row = len(data)
    for i in range(row):
        to_add = False
        str_nb = ""
        for j in range(col):
            if data[i][j].isdigit():
                if not to_add:
                    str_nb += data[i][j]
                    with suppress(IndexError):
                        for y in (i - 1, i, i + 1):
                            for x in (j - 1, j, j + 1):
                               if (x != j or y != i) and x>=0 and y >= 0 and data[y][x] != "." and not data[y][x].isdigit():
                                    to_add = True
                                    break
                            else:
                                continue
                            break
                else:
                    str_nb += data[i][j]
                if to_add and j == len(data[i]) - 1:
                    result += int(str_nb)
                    str_nb = ""
                    to_add = False
            else:
                if to_add:
                    result += int(str_nb)
                str_nb = ""
                to_add = False
    return result

def part_2() -> int:
    col = len(data[0])
    row = len(data)
    gear = defaultdict(lambda: [])
    for i in range(row):
        star = None
        str_nb = ""
        for j in range(col):
            if data[i][j].isdigit():
                if not star:
                    str_nb += data[i][j]
                    with suppress(IndexError):
                        for y in (i -1, i, i + 1):
                            for x in (j - 1, j, j + 1):
                               if data[y][x] == "*":
                                    star = (y, x)
                                    break
                            else:
                                continue
                            break
                else:
                    str_nb += data[i][j]
                if star and j == len(data[i]) - 1:
                    gear[star].append(int(str_nb))
                    str_nb = ""
                    star = None
            else:
                if star:
                    gear[star].append(int(str_nb))
                str_nb = ""
                star = None
    result = 0
    for value in gear.values():
        if len(value) == 2:
            result += value[0] * value[1]
    return result


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        print(part_1())
    else:
        print(part_2())
    print(time() - t)

