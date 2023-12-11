from dataclasses import dataclass
from pathlib import Path

@dataclass
class Galaxy:
    x: int
    y: int

@dataclass
class Expansion:
    rows: list
    columns: list

def expand(universe: list) -> Expansion:
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

def evaluate_paths(galaxies: list, expansion: Expansion) -> list:
    paths = []
    glen = len(galaxies)
    for i in range(glen):
        for j in range(i + 1, glen):
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
    return paths

if __name__ == "__main__":
    with Path("day_11/input.txt").open("r") as file:
        data = file.read().split()
    expansion = expand(data)
    paths = evaluate_paths(get_galaxies(data), expansion)
    print(sum(paths))
