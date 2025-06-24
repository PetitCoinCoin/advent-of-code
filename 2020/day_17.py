import argparse

from copy import deepcopy
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

class Grid:
    def __init__(self, raw: str, part: int) -> None:
        self.active = {}
        self.is_4d = part == 2
        for r, row in enumerate(raw.split("\n")):
            for c, char in enumerate(row):
                if char == "#":
                    self.active[(r, c, 0, 0)] = True
        self.previous_active = {}
        self.min_x = 0
        self.max_x = len(raw.split("\n"))
        self.min_y = 0
        self.max_y = len(raw.split("\n")[0])
        self.min_z = 0
        self.max_z = 0
        self.min_w = 0
        self.max_w = 0
    
    def cycle(self) -> None:
        self.previous_active = deepcopy(self.active)
        min_w = self.min_w - 1 if self.is_4d else self.min_w
        max_w = self.max_w + 1 if self.is_4d else self.max_w
        for w in range(min_w, max_w + 1):
            self.sub_3d_cycle(w)

    def sub_3d_cycle(self, w: int = 0) -> None:
        for x in range(self.min_x - 1, self.max_x + 2):
            for y in range(self.min_y - 1, self.max_y + 2):
                for z in range(self.min_z - 1, self.max_z + 2):
                    position = (x, y, z, w)
                    state = self.previous_active.get(position, False)
                    active_neighbours = sum(
                        self.previous_active.get(neighbour, False)
                        for neighbour in self.__get_neighbours(position)
                    )
                    if state and active_neighbours != 2 and active_neighbours != 3:
                         self.active[position] = False
                    elif not state and active_neighbours == 3:
                        self.active[position] = True
                        self.min_x = min(self.min_x, x)
                        self.max_x = max(self.max_x, x)
                        self.min_y = min(self.min_y, y)
                        self.max_y = max(self.max_y, y)
                        self.min_z = min(self.min_z, z)
                        self.max_z = max(self.max_z, z)
                        self.min_w = min(self.min_w, w)
                        self.max_w = max(self.max_w, w)

    @property
    def active_number(self) -> int:
        return sum(self.active.values())

    def __get_neighbours(self, position: tuple) -> list:
        x, y, z, w = position
        if self.is_4d:
            return [
                (x + dx, y + dy, z + dz, w + dw)
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                for dz in (-1, 0, 1)
                for dw in (-1, 0, 1)
                if dx or dy or dz or dw
            ]
        return [
            (x + dx, y + dy, z + dz, w)
            for dx in (-1, 0, 1)
            for dy in (-1, 0, 1)
            for dz in (-1, 0, 1)
            if dx or dy or dz
        ]

    def pprint(self):
        """For part 1 3D debug"""
        for z in range(self.min_z, self.max_z + 1):
            print(f"z={z}")
            for x in range(self.min_x, self.max_x + 1):
                print("".join([
                    "#" if self.active.get((x, y, z), False) else "."
                    for y in range(self.min_y, self.max_y + 1)
                ]))
            print()

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = Grid(file.read().strip(), args.part)
    for _ in range(6):
        data.cycle()
    print(data.active_number)
    print(time() - t)
