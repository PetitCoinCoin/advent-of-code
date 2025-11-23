import argparse
import re

from dataclasses import dataclass
from pathlib import Path

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
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

def parse_input(raw: str) -> Ingredient:
    groups = re.findall(r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)", raw)
    return Ingredient(
        name=groups[0][0],
        capacity=int(groups[0][1]),
        durability=int(groups[0][2]),
        flavor=int(groups[0][3]),
        texture=int(groups[0][4]),
        calories=int(groups[0][5]),
    )

def bruteforce(data: list, limit_calories: int = 0):
    max_cookie = 0
    for x in range(1, 101):
        for y in range(1, 101):
            for z in range(1, 101):
                if x + y + z > 100:
                    break
                capacity = max(0, sum([a * b for a,b in zip([x, y, z, (100 - x - y - z)], [ing.capacity for ing in data])]))
                durability = max(0, sum([a * b for a,b in zip([x, y, z, (100 - x - y - z)], [ing.durability for ing in data])]))
                flavor = max(0, sum([a * b for a,b in zip([x, y, z, (100 - x - y - z)], [ing.flavor for ing in data])]))
                texture = max(0, sum([a * b for a,b in zip([x, y, z, (100 - x - y - z)], [ing.texture for ing in data])]))
                if not limit_calories or sum([a * b for a,b in zip([x, y, z, (100 - x - y - z)], [ing.calories for ing in data])]) == limit_calories:
                    max_cookie = max(max_cookie, capacity * durability * flavor * texture)
    print(max_cookie)

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(row) for row in file.read().split("\n")]
    if args.part == 1:
        bruteforce(data)
    else:
        bruteforce(data, 500)
