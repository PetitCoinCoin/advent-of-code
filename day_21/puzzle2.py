from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass
class Node:
    r: int
    c: int
    # children: list
    parent: Node | None

    def __hash__(self): 
        return hash(f"{self.r}-{self.c}")

    def __eq__(self, val):
        return val.r == self.r and val.c == self.c

    def __repr__(self):
        return f"r: {self.r}, c: {self.c}, parent: ({self.parent})"

def next_plots(parent: Node, data: list) -> set:
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

if __name__ == "__main__":
    with Path("day_21/input.txt").open("r") as file:
        data = [[x for x in row]for row in file.read().splitlines()]
    sr, sc = get_start(data)
    start = Node(r=sr, c=sc, parent=None)
    print(start)
    side = len(data)
    half = side // 2
    steps = {
        0: {start},
        1: next_plots(start, data)
    }
    count = [len(steps[0]), len(steps[1])]
    for step in range(2, half + 2*side + 1):
        new_plots = set()
        for plot in steps[step - 1]:
            new_plots |= next_plots(plot, data)
        steps[step] = {plot for plot in new_plots if plot not in steps[step - 2]}
        count.append(count[step - 2] + len(steps[step]))

    print(quadratic(count[half], count[half + side], count[half + 2 * side], 26501365 // side))
