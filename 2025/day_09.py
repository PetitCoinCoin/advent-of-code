from itertools import combinations, pairwise
from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def area(pos1: tuple, pos2: tuple) -> int:
    return (abs(pos1[0] - pos2[0]) + 1) * (abs(pos1[1] - pos2[1]) + 1)

def get_tiles() -> None:
    for t1, t2 in pairwise(data + [data[0]]):
        if t1[0] == t2[0]:
            columns[t1[0]] = columns.get(t1[0], []) + [range(min(t1[1], t2[1]), max(t1[1], t2[1]) + 1)]
        else:
            rows[t1[1]] = rows.get(t1[1], []) + [range(min(t1[0], t2[0]), max(t1[0], t2[0]) + 1)]

def rg_area(pos1: tuple, pos2: tuple) -> int:
    opposite1 = (pos1[0], pos2[1])
    opposite2 = (pos2[0], pos1[1])
    for opposite in (opposite1, opposite2):
        if opposite in cache_in:
            continue
        if opposite in cache_out:
            return 0
        x, y = opposite
        top, right, left, bottom = 0, 0, 0, 0
        for ry, yrows in rows.items():
            if ry == y:
                if any((x in row for row in yrows)):
                    break
                right -= 2 * len([row for row in yrows if row[0] > x])
                left -= 2 * len([row for row in yrows if row[-1] < x])
            if ry < y:
                if any((x in row for row in yrows)):
                    top += 1
            else:
                if any((x in row for row in yrows)):
                    bottom += 1
        else:
            for cx, xcols in columns.items():
                if cx == x:
                    if any((y in col for col in xcols)):
                        break
                    top -= 2 * len([col for col in xcols if col[-1] < y])
                    bottom -= 2 * len([col for col in xcols if col[0] > y])
                if cx < x:
                    if any((y in col for col in xcols)):
                        left += 1
                else:
                    if any((y in col for col in xcols)):
                        right += 1
            else:
                if not (top % 2 and bottom % 2) and not (right % 2 and left % 2):
                    cache_out.add(opposite)
                    return 0
        cache_in.add(opposite)
    if not is_possible([pos1, opposite1, pos2, opposite2]):
        return 0
    return area(pos1, pos2)

def is_possible(corners: list) -> bool:
    # Not a general case
    for c1, c2 in pairwise(corners + [corners[0]]):
        if c1[0] == c2[0]:  # same column
            for y in range(min(c1[1], c2[1]) + 1, max(c1[1], c2[1])):
                if any((c1[0] in row for row in rows.get(y, []))):
                    return False
        else:  # same row
            for x in range(min(c1[0], c2[0]) + 1, max(c1[0], c2[0])):
                if any((c1[1] in column for column in columns.get(x, []))):
                    return False
    return True

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [tuple(map(int, line.split(","))) for line in file.read().strip().split("\n")]
    if args.part == 1:
        print(max(
            area(p1, p2)
            for p1, p2 in combinations(data, 2)
        ))
    else:
        columns = {}
        rows = {}
        cache_in = set(data)
        cache_out = set()
        get_tiles()
        print(max(
            rg_area(p1, p2)
            for p1, p2 in combinations(data, 2)
        ))
    print(time() - t)
