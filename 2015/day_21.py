import argparse
import re

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

def parse_input(raw: str, data: list) -> None:
    groups = re.findall(r"(\w+\s?\+?\d?)", raw)
    data.append((int(groups[1]), sum([int(x) for x in groups[-2:]])))


if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        weapons = []
        armors = [(0, 0)]
        rings = [(0, 0), (0, 0)]
        while line := file.readline():
            if line.startswith("Weapons"):
                current = weapons
                continue
            if line.startswith("Armor"):
                current = armors
                continue
            if line.startswith("Rings"):
                current = rings
                continue
            if line.strip():
                parse_input(line.strip(), current)
    min_cost = 500
    max_cost = 0
    for weapon in weapons:
        for armor in armors:
            for i, ring1 in enumerate(rings):
                for ring2 in rings[i + 1:]:
                    stats = weapon[1] + armor[1] + ring1[1] + ring2[1]
                    cost = weapon[0] + armor[0] + ring1[0] + ring2[0]
                    # According input, I need to buy items such as armor + damage >= 10 (boss_armor + boss_damage)
                    if stats >= 10 and cost < min_cost:
                        min_cost = cost
                    if stats < 10 and cost > max_cost:
                        max_cost = cost
    if args.part == 1:
        print(min_cost)
    else:
        print(max_cost)
