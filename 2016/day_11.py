import argparse

from copy import deepcopy
from itertools import combinations
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

def parse_input(raw: str) -> None:
    for i, floor in enumerate(raw.split("\n")):
        interest = floor.split("contains ")[-1]
        if interest.startswith("nothing"):
            DATA[i + 1] = []
            continue
        interest = interest.replace("and", ",")
        items = [item.strip()[2:].split(" ") for item in interest.split(", ") if item.strip()]
        DATA[i + 1] = [item[0][:2] + item[1][0].upper() for item in items]
        DATA[i + 1].sort()


def is_valid_together(combination: tuple, all_elements: list) -> bool:
    microchip = [c for c in combination if c[-1] == "M"]
    if len(microchip) == 1 and len(combination) > 1 and microchip[0][:-1] + "G" not in combination:
        # Two items in combination are not compatible with each other
        return False
    elements = [elt for elt in all_elements if elt not in combination]
    for elt in [elt for elt in elements if elt[-1] == "M"]:
        if elt[:-1] + "G" not in elements and [e for e in elements if e[-1] == "G"]:
            return False
    return True

def get_combinations(data: dict, elevator: int) -> list:
    return [c for c in combinations(data[elevator], 2) if is_valid_together(c, data[elevator])] + [c for c in combinations(data[elevator], 1) if is_valid_together(c, data[elevator])]

def empty_next_floors(data: dict, elevator: int, new_elevator: int) -> bool:
    if new_elevator > elevator:
        for e in range(new_elevator, 5):
            if data[e]:
                return False
        return True
    for e in range(1, new_elevator + 1):
        if data[e]:
            return False
    return True

def move_bfs() -> int:
    empty_first = False
    elevator = 1
    seen = set()
    queue = [(0, 1, DATA)]
    while queue:
        step, elevator, data = queue.pop(0)
        data = deepcopy(data)
        if (elevator, str(data)) in seen:
            continue
        seen.add((elevator, str(data)))
        combi = get_combinations(data, elevator)
        for new_elevator in (elevator + 1, elevator - 1):
            if new_elevator in (0, 5):
                continue
            for c in combi:
                if len(c) == 1 and empty_next_floors(data, elevator, new_elevator):
                    # If we bring only one item on empty floors, we will have to bring it back: useless steps
                    continue
                floor = data[new_elevator] + list(c)
                floor.sort()
                if not is_valid_together(tuple(), floor):
                    continue
                new_data = deepcopy(data)
                new_data[new_elevator] = floor
                new_data[elevator] = [elt for elt in new_data[elevator] if elt not in c]
                if not new_data[1] and not new_data[2] and not new_data[3]:
                    # Everything is on 4th floor
                    return step + 1
                if not new_data[1]:
                    empty_first = True
                if empty_first and new_data[1]:
                    # Once first floor is empty, there should be no reason to bring stuff back
                    continue
                if (new_elevator, str(new_data)) not in seen:
                    queue.append((step + 1, new_elevator, new_data))

if __name__ == "__main__":
    args = _parse_args()
    DATA = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        parse_input(file.read().strip())
    if args.part == 2:
        DATA[1] = DATA[1] + ["eM", "eG", "dM", "dG"]
        DATA[1].sort()
    print(move_bfs())
