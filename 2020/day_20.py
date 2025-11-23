import argparse
import math

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

MAP_SIDES = {
    "top": {
        "reverse_top": (2, 0, -1, 0),  # nb rotation right, nb flip, dy, dx
        "reverse_right": (1, 0, -1, 0),
        "bottom": (0, 0, -1, 0),
        "left": (3, 0, -1, 0),
        "top": (0, 1, -1, 0),
        "right": (1, 1, -1, 0),
        "reverse_bottom": (2, 1, -1, 0),
        "reverse_left": (3, 1, -1, 0),
    },
    "right": {
        "reverse_top": (3, 0, 0, 1),
        "reverse_right": (2, 0, 0, 1),
        "bottom": (1, 0, 0, 1),
        "left": (0, 0, 0, 1),
        "top": (1, 1, 0, 1),
        "right": (2, 1, 0, 1),
        "reverse_bottom": (3, 1, 0, 1),
        "reverse_left": (0, 1, 0, 1),
    },
    "bottom": {
        "top": (0, 0, 1, 0),
        "right": (3, 0, 1, 0),
        "reverse_bottom": (2, 0, 1, 0),
        "reverse_left": (1, 0, 1, 0),
        "reverse_top": (2, 1, 1, 0),
        "reverse_right": (3, 1, 1, 0),
        "bottom": (0, 1, 1, 0),
        "left": (1, 1, 1, 0),
    },
    "left": {
        "top": (1, 0, 0, -1),
        "right": (0, 0, 0, -1),
        "reverse_bottom": (3, 0, 0, -1),
        "reverse_left": (2, 0, 0, -1),
        "reverse_top": (3, 1, 0, -1),
        "reverse_right": (0, 1, 0, -1),
        "bottom": (1, 1, 0, -1),
        "left": (2, 1, 0, -1),
    },
}

MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

def parse_tile(raw: str) -> dict:
    tile = {}
    lines = raw.split("\n")
    tile["id"] = int(lines[0].split(" ")[-1][:-1])  # eww
    tile["grid"] = lines[1:]
    # left to right
    tile["top"] = lines[1]
    tile["bottom"] = lines[-1]
    # top to bottom
    tile["right"] = "".join(line[-1] for line in lines[1:])
    tile["left"] = "".join(line[0] for line in lines[1:])
    return tile

def rotated_once_to_right(tile: dict) -> dict:
    rotated_tile = {}
    rotated_tile["right"] = tile["top"]
    rotated_tile["left"] = tile["bottom"]
    rotated_tile["top"] = tile["left"][::-1]
    rotated_tile["bottom"] = tile["right"][::-1]
    return rotated_tile

def get_corners(early_return: bool = False) -> list:
    """
        No need to have something too generic.
        It looks like there is only one possible neighbour on each side of a tile.
    """
    corners = []
    for tile in data:
        doubles = 0
        for key, val in tile.items():
            if key != "id":
                doubles += sum(
                    1 if d[side] == val else 0
                    for d in data
                    for side in ("top", "bottom", "right", "left")
                ) + sum(
                    1 if d[side] == val[::-1] else 0
                    for d in data
                    for side in ("top", "bottom", "right", "left")
                )
        if doubles == 6:  # self = 4 + only 2 neighbours in corners
            if early_return:
                return [tile]
            corners.append(tile)
    return corners

def rotate_tile_right(tile: dict, nb: int) -> dict:
    if not nb:
        return tile
    rotated = {"id": tile["id"]}
    new_grid = []
    for i in range(len(tile["grid"][0])):
        new_grid.append("".join(row[i] for row in tile["grid"][::-1]))
    rotated["grid"] = new_grid
    rotated["top"] = new_grid[0]
    rotated["bottom"] = new_grid[-1]
    rotated["right"] = "".join(line[-1] for line in new_grid)
    rotated["left"] = "".join(line[0] for line in new_grid)
    return rotate_tile_right(rotated, nb - 1)

def flip_tile(tile: dict, flip: int) -> dict:
    if not flip:
        return tile
    flipped = {"id": tile["id"]}
    flipped["grid"] = tile["grid"][::-1]
    flipped["top"] = flipped["grid"][0]
    flipped["bottom"] = flipped["grid"][-1]
    flipped["right"] = "".join(line[-1] for line in flipped["grid"])
    flipped["left"] = "".join(line[0] for line in flipped["grid"])
    return flipped

def build_base_grid() -> list:
    corner = get_corners(True)[0]
    dict_grid = {(0, 0): corner}
    queue = {(0, 0)}
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    while len(dict_grid) != len(data):
        x, y = queue.pop()
        current_tile = dict_grid[(x, y)]
        for tile in data:
            if tile["id"] == current_tile["id"]:
                continue
            for side in ("top", "bottom", "right", "left"):
                for other_side in ("top", "bottom", "right", "left"):
                    if current_tile[side] == tile[other_side]:
                        r, f, dy, dx = MAP_SIDES[side][other_side]
                        if (x + dx, y + dy) not in dict_grid:
                            queue.add((x + dx, y + dy))
                        dict_grid[(x + dx, y + dy)] = rotate_tile_right(flip_tile(tile, f), r)
                        min_x = min(min_x, x + dx)
                        max_x = max(max_x, x + dx)
                        min_y = min(min_y, y + dy)
                        max_y = max(max_y, y + dy)
                    if current_tile[side] == tile[other_side][::-1]:
                        r, f, dy, dx = MAP_SIDES[side][f"reverse_{other_side}"]
                        if (x + dx, y + dy) not in dict_grid:
                            queue.add((x + dx, y + dy))
                        dict_grid[(x + dx, y + dy)] = rotate_tile_right(flip_tile(tile, f), r)
                        min_x = min(min_x, x + dx)
                        max_x = max(max_x, x + dx)
                        min_y = min(min_y, y + dy)
                        max_y = max(max_y, y + dy)
    base_grid = []
    for y in range(min_y, max_y + 1):
        current_len = len(base_grid)
        base_grid += [line[1: -1] for line in dict_grid[(min_x, y)]["grid"][1: -1]]  # + [""]
        for x in range(min_x + 1, max_x + 1):
            for i, line in enumerate(dict_grid[(x, y)]["grid"][1: -1]):
                base_grid[current_len + i] += line[1: -1]
    return base_grid

def search_monster(sea: list) -> int:
    """Assuming the sea monsters do not overlap"""
    found = 0
    width = len(sea[0])
    for r in range(len(sea) - 2):
        for c in range(width - 19):  # sea monster width = 20
            for dr, dc in sea_monster:
                if sea[r + dr][c + dc] != "#":
                    break
            else:
                found += 1
    return found


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_tile(tile_input) for tile_input in file.read().strip().split("\n\n")]
    if args.part == 1:
        print(math.prod(tile["id"] for tile in get_corners()))
    else:
        sea_monster = set(
            (r, c)
            for r, line in enumerate(MONSTER.split("\n"))
            for c, char in enumerate(line)
            if char == "#"
        )
        base_grid = build_base_grid()
        monster_count = search_monster(base_grid)
        rotated = 0
        while not monster_count:
            if rotated == 4:
                base_grid = flip_tile({"id": "main", "grid": base_grid}, 1)["grid"]
                rotated = 0
                monster_count = search_monster(base_grid)
                continue
            base_grid = rotate_tile_right({"id": "main", "grid": base_grid}, 1)["grid"]
            rotated += 1
            monster_count = search_monster(base_grid)
        print(sum(1 for line in base_grid for char in line if char == "#") - monster_count * len(sea_monster))
    print(time() - t)
