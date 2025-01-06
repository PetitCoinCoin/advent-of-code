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

CART_DELTA = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}

NEXT_CHAR = {
    ">": {
        "|": "",
        "-": ">",
        "/": "^",
        "\\": "v",
    },
    "v": {
        "|": "v",
        "-": "",
        "/": "<",
        "\\": ">",
    },
    "<": {
        "|": "",
        "-": "<",
        "/": "v",
        "\\": "^",
    },
    "^": {
        "|": "^",
        "-": "",
        "/": ">",
        "\\": "<",
    },
}

NEXT_CHAR_INTERSECTION = {
    ">": {
        "<": "^",
        "=": ">",
        ">": "v",
    },
    "v": {
        "<": ">",
        "=": "v",
        ">": "<",
    },
    "<": {
        "<": "v",
        "=": "<",
        ">": "^",
    },
    "^": {
        "<": "<",
        "=": "^",
        ">": ">",
    },
}

INTERSECTIONS = "<=>"

@dataclass
class Cart:
    x: int
    y: int
    direction: str
    intersect: int = 0
    crashed: bool = False

    def __gt__(self, other: Cart) -> bool:
        if self.y > other.y:
            return True
        if self.y == other.y:
            return self.x > other.x
        return False

def parse_input(r: int, raw: str) -> None:
    for c, char in enumerate(raw):
        if char in " \n":
            continue
        tracks[(c, r)] = char
        if char in "<>":
            carts.append(Cart(x=c, y=r, direction=char))
            tracks[(c, r)] = "-"
        elif char in "v^":
            carts.append(Cart(x=c, y=r, direction=char))
            tracks[(c, r)] = "|"

def tick() -> None:
    carts.sort()
    for cart in carts:
        next_x = cart.x + CART_DELTA[cart.direction][0]
        next_y = cart.y + CART_DELTA[cart.direction][1]
        for c in carts:
            if c.x == next_x and c.y == next_y and not c.crashed:
                c.crashed = True
                cart.crashed = True
        next_char = tracks[(next_x, next_y)]
        if next_char != "+":
            next_char = NEXT_CHAR[cart.direction][next_char]
        else:
            direction = INTERSECTIONS[cart.intersect % 3]
            next_char = NEXT_CHAR_INTERSECTION[cart.direction][direction]
            cart.intersect += 1
        cart.x = next_x
        cart.y = next_y
        cart.direction = next_char

def crash() -> None | tuple:
    reduced = {}
    for cart in carts:
        y, x, _, _ = cart
        if reduced.get((x, y)):
            return x, y
        reduced[(x, y)] = True
    return None

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    tracks = {}
    carts = []
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        for r, raw in enumerate(file.readlines()):
            parse_input(r, raw)
    if args.part == 1:
        while not sum(cart.crashed for cart in carts):
            tick()
        crashed = next(cart for cart in carts if cart.crashed)
        print(f"{crashed.x},{crashed.y}")
    else:
        while len(carts) > 1:
            tick()
            carts = [cart for cart in carts if not cart.crashed]
        print(f"{carts[0].x},{carts[0].y}")
    print(time() - t)
