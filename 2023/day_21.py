from __future__ import annotations
import argparse

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

@dataclass
class Node:
    r: int
    c: int
    parent: Node | None

    def __hash__(self): 
        return hash(f"{self.r}-{self.c}")

    def __eq__(self, val):
        return val.r == self.r and val.c == self.c

    def __repr__(self):
        return f"r: {self.r}, c: {self.c}, parent: ({self.parent})"

def next_plots_2(parent: Node, data: list) -> set:
    return {
        Node(r, c, parent)
        for r, c in [
            (parent.r - 1, parent.c),
            (parent.r + 1, parent.c),
            (parent.r, parent.c - 1),
            (parent.r, parent.c + 1)
        ]
        if data[r % len(data)][c % len(data[0])] != "#" and (not parent.parent or not (r == parent.parent.r and c == parent.parent.c))
    }

def get_start(data: list) -> tuple:
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val == "S":
                return (r, c)

def quadratic(n0: int, n1: int, n2:int, x:int) -> int:
    a = n0
    b = n1 - n0
    c = n2 - n1
    return a + b * x + (x * (x - 1) // 2) * (c - b)

def next_plots(r: int, c: int, data: list) -> set:
    return {
        (i, j)
        for i, j in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        if len(data) > i >= 0 and len(data[0]) > j >= 0 and data[i][j] != "#"
    }

def build_plots(data: list) -> tuple:
    plots = {}
    start = None
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val != "#":
                plots[(r, c)] = next_plots(r, c, data)
                if val == "S":
                    start = (r, c)
    return start, plots

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    if args.part == 1:
        with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
            data = file.read().split()
        start, plots = build_plots(data)
        i = 1
        children = plots[start]
        while i < 64:
            new_children = set()
            for child in children:
                new_children |= plots[child]
            children = new_children
            i += 1
        print(len(children))
    else:
        with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
            data = [[x for x in row]for row in file.read().splitlines()]
        sr, sc = get_start(data)
        start = Node(r=sr, c=sc, parent=None)
        side = len(data)
        half = side // 2
        steps = {
            0: {start},
            1: next_plots_2(start, data)
        }
        count = [len(steps[0]), len(steps[1])]
        for step in range(2, half + 2*side + 1):
            new_plots = set()
            for plot in steps[step - 1]:
                new_plots |= next_plots_2(plot, data)
            steps[step] = {plot for plot in new_plots if plot not in steps[step - 2]}
            count.append(count[step - 2] + len(steps[step]))

        print(quadratic(count[half], count[half + side], count[half + 2 * side], 26501365 // side))
    print(time() - t)

