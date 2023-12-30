from copy import deepcopy
from pathlib import Path

def get_brick(row: str) -> tuple:
    """brick as 'start, end': z, y, x"""
    min_range = [int(val) for val in row.split("~")[0].split(",")]
    max_range = [int(val) for val in row.split("~")[1].split(",")]
    return (tuple(min_range[::-1]), tuple(max_range[::-1]))

if __name__ == "__main__":
    with Path("day_22/input.txt").open("r") as file:
        bricks = []
        while line := file.readline():
            bricks.append(get_brick(line))
        bricks.sort()

        tower = set()
        last_position = dict()
        supported_by = dict()
        for i, brick in enumerate(bricks):
            blocks = set()
            (za, ya, xa), (zb, yb, xb) = brick
            for z in range(za, zb + 1):
                for y in range(ya, yb + 1):
                    for x in range(xa, xb + 1):
                        blocks.add((z, y, x))
            falling = True
            last_position[i] = set()
            while falling:
                new_blocks = set()
                check_set = set()
                for block in blocks:
                    z, y, x = block
                    if z - 1 == 0:
                        falling = False
                        break
                    new_blocks.add((z - 1, y, x))
                else:
                    check_set = tower & new_blocks
                    if len(check_set):
                        falling = False
                        break
                    blocks = deepcopy(new_blocks)
            for block in blocks:
                tower.add(block)
                last_position[i].add(block)
            supported_by[i] = set()
            for n in range(i):
                if len(check_set & last_position[n]):
                    supported_by[i].add(n)

        unremovable = {list(support)[0] for support in supported_by.values() if len(support) == 1}
        print(len(bricks) - len(unremovable))
