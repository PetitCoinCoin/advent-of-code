from pathlib import Path

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
    with Path("day_21/input.txt").open("r") as file:
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
