from dataclasses import dataclass
from pathlib import Path

@dataclass
class Galaxy:
    x: int
    y: int

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

def get_galaxies(universe: list) -> list:
    galaxies = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                galaxies.append(Galaxy(x=j, y=i))
    return galaxies

def evaluate_paths(galaxies: list) -> list:
    paths = []
    glen = len(galaxies)
    for i in range(glen):
        for j in range(i + 1, glen):
            paths.append(abs(galaxies[j].x - galaxies[i].x) + abs(galaxies[j].y - galaxies[i].y))
    return paths

if __name__ == "__main__":
    with Path("day_11/input.txt").open("r") as file:
        data = file.read().split()
    expanded = expand(data)
    paths = evaluate_paths(get_galaxies(expanded))
    print(sum(paths))
