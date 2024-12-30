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
class Galaxy:
    x: int
    y: int

@dataclass
class Expansion:
    rows: list
    columns: list

def expand(universe: list) -> list:
    rows = []
    columns = []
    for i in range(len(universe)):
        if not universe[i].replace(".", ""):
            rows.append(i)
    for j in range(len(universe[0])):
        if not [universe[x][j] for x in range(len(universe)) if universe[x][j] != "."]:
            columns.append(j)
    for i, idx in enumerate(rows):
        universe.insert(idx + i, universe[idx + i])
    for i in range(len(universe)):
        universe[i] = [x for x in universe[i]]
        for j, idx in enumerate(columns):
            universe[i].insert(j + idx, universe[i][j + idx])
    return universe

def expand_2(universe: list) -> Expansion:
    rows = []
    columns = []
    for i in range(len(universe)):
        if not universe[i].replace(".", ""):
            rows.append(i)
    for j in range(len(universe[0])):
        if not [universe[x][j] for x in range(len(universe)) if universe[x][j] != "."]:
            columns.append(j)
    return Expansion(rows=rows, columns=columns)

def get_galaxies(universe: list) -> list:
    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                galaxies.append(Galaxy(x=j, y=i))
    return galaxies

def evaluate_paths(galaxies: list, expansion: None | Expansion = None) -> list:
    paths = []
    glen = len(galaxies)
    for i in range(glen):
        for j in range(i + 1, glen):
            if expansion is not None:
                base_path = abs(galaxies[j].x - galaxies[i].x) + abs(galaxies[j].y - galaxies[i].y)
                additional_x = 0
                additional_y = 0
                for k in range(min(galaxies[i].x, galaxies[j].x), max(galaxies[i].x, galaxies[j].x)):
                    if k in expansion.columns:
                        additional_x += 999999
                for k in range(min(galaxies[i].y, galaxies[j].y), max(galaxies[i].y, galaxies[j].y)):
                    if k in expansion.rows:
                        additional_y += 999999
                paths.append(base_path + additional_x + additional_y)
            else:
                paths.append(abs(galaxies[j].x - galaxies[i].x) + abs(galaxies[j].y - galaxies[i].y))
    return paths

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        expanded = expand(data)
        paths = evaluate_paths(get_galaxies(expanded))
        print(sum(paths))
    else:
        expansion = expand_2(data)
        paths = evaluate_paths(get_galaxies(data), expansion)
        print(sum(paths))
    print(time() - t)

