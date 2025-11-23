from __future__ import annotations

import argparse

from copy import deepcopy
from dataclasses import dataclass
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

DIRECTION_MAP = {
    "ne": ("ne", 1),
    "se": ("se", 1),
    "e": ("e", 1),
    "nw": ("se", -1),
    "sw": ("ne", -1),
    "w": ("e", -1),
}

@dataclass
class Tile:
    e: int = 0
    ne: int = 0
    se: int = 0
    color: bool = False  # False = white, True = black

    def compact(self) -> None:
        if self.ne * self.se > 0:
            d = min(abs(self.ne), abs(self.se))
            sign = self.ne // abs(self.ne)
            self.ne -= d * sign
            self.se -= d * sign
            self.e += d * sign
        if self.ne * self.e < 0:
            d = min(abs(self.ne), abs(self.e))
            sign = self.e // abs(self.e)
            self.ne += d * sign
            self.e -= d * sign
            self.se += d * sign
        if self.se * self.e < 0:
            d = min(abs(self.se), abs(self.e))
            sign = self.e // abs(self.e)
            self.se += d * sign
            self.e -= d * sign
            self.ne += d * sign

    def flip(self) -> None:
        self.color = not self.color

class Floor:
    def __init__(self, tiles: dict) -> None:
        self.tiles = tiles
        self.previous_tiles = dict()
        self.borders = set(self.tiles.keys())

    def art_update(self) -> None:
        self.previous_tiles = deepcopy(self.tiles)
        self.__get_borders()
        for tile in self.previous_tiles.keys() | self.borders:
            e, ne, se = tile
            bn = self.__get_black_neighbours((e, ne, se))
            if self.previous_tiles.get((e, ne, se), False):
                self.tiles[(e, ne, se)] = bn in (1, 2)
            else:
                self.tiles[(e, ne, se)] = bn == 2
    
    def __get_black_neighbours(self, tile: tuple) -> int:
        e, ne, se = tile
        return sum(
            self.previous_tiles.get(self.__compact((e + de, ne + dne, se + dse)), False)
            for de, dne, dse in (
                (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
            )
        )
    
    def __get_borders(self) -> None:
        new_borders = set()
        for e, ne, se in self.borders:
            for de, dne, dse in (
                (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)
            ):
                neighbour = self.__compact((e + de, ne + dne, se + dse))
                if neighbour not in self.previous_tiles:
                    new_borders.add(neighbour)
        self.borders = new_borders

    @staticmethod
    def __compact(tile: tuple) -> tuple:
        e, ne, se = tile
        if ne * se > 0:
            d = min(abs(ne), abs(se))
            sign = ne // abs(ne)
            ne -= d * sign
            se -= d * sign
            e += d * sign
        if ne * e < 0:
            d = min(abs(ne), abs(e))
            sign = e // abs(e)
            ne += d * sign
            e -= d * sign
            se += d * sign
        if se * e < 0:
            d = min(abs(se), abs(e))
            sign = e // abs(e)
            se += d * sign
            e -= d * sign
            ne += d * sign
        return (e, ne, se)

    @property
    def black(self) -> int:
        return sum(self.tiles.values())

def parse_input(raw: str) -> int:
    i = 0
    tile = Tile()
    while i < len(raw):
        direction = raw[i]
        if direction in "ns":
            i += 1
            direction += raw[i]
        attr, delta = DIRECTION_MAP[direction]
        setattr(tile, attr, getattr(tile, attr) + delta)
        i += 1
    tile.compact()
    if (tile.e, tile.ne, tile.se) in reverse_tiles:
        return reverse_tiles[(tile.e, tile.ne, tile.se)]
    tile_id = len(tiles)
    reverse_tiles[(tile.e, tile.ne, tile.se)] = tile_id
    tiles[tile_id] = tile
    return tile_id

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    reverse_tiles = {}
    tiles: dict[int, Tile] = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().strip().split("\n")]
    for tile_id in data:
        tiles[tile_id].flip()
    if args.part == 1:
        print(sum(tiles[tile_id].color for tile_id in data))
    else:
        floor = Floor({
            (tiles[tile_id].e, tiles[tile_id].ne, tiles[tile_id].se): tiles[tile_id].color
            for tile_id in data
        })
        for _ in range(100):
            floor.art_update()
        print(floor.black)
    print(time() - t)
