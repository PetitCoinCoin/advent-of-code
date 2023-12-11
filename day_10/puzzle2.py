from dataclasses import dataclass
from pathlib import Path

@dataclass
class Position:
    x: int
    y: int
    steps: int
    direction: str

def find_start(data: list) -> Position:
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "S":
                return Position(x=j, y=i, steps=0, direction="")

def move(start: Position, data: list) -> Position:
    direction = ""
    if start.direction == "n":
        if data[start.y - 1][start.x] == "|":
            direction = "n"
        elif data[start.y - 1][start.x] == "F":
            direction = "e"
        elif data[start.y - 1][start.x] == "7":
            direction = "w"
        return Position(start.x, start.y - 1, position.steps + 1, direction)
    if start.direction == "e":
        if data[start.y][start.x + 1] == "-":
            direction = "e"
        if data[start.y][start.x + 1] == "J":
            direction = "n"
        if data[start.y][start.x + 1] == "7":
            direction = "s"
        return Position(start.x + 1, start.y, position.steps + 1, direction)
    if start.direction == "s":
        if data[start.y + 1][start.x] == "|":
            direction = "s"
        if data[start.y + 1][start.x] == "J":
            direction = "w"
        if data[start.y + 1][start.x] == "L":
            direction = "e"
        return Position(start.x, start.y + 1, position.steps + 1, direction)
    if start.direction == "w":
        if data[start.y][start.x - 1] == "-":
            direction = "w"
        if data[start.y][start.x - 1] == "L":
            direction = "n"
        if data[start.y][start.x - 1] == "F":
            direction = "s"
        return Position(start.x - 1, start.y, position.steps + 1, direction)

if __name__ == "__main__":
    with Path("day_10/input.txt").open("r") as file:
        data = []
        while line := file.readline():
            data.append(line.strip())
    position = find_start(data)
    start_y = position.y
    if data[position.y - 1][position.x] in ("|", "F", "7"):
        position.direction = "n"
    elif data[position.y][position.x + 1] in ("-", "7", "J"):
        position.direction = "e"
    elif data[position.y + 1][position.x] in ("|", "L", "J"):
        position.direction = "s"
    elif data[position.y][position.x - 1] in ("-", "L", "F"):
        position.direction = "w"
    pipe = {}
    while data[position.y][position.x] != "S" or position.steps == 0:
        if data[position.y][position.x] != "-":
            pipe[position.y] = pipe.get(position.y, []) + [position.x]
        position = move(position, data)
    data[start_y].replace("S", "L")  # because I checked it

    cpt = 0
    for i in range(len(data)):
        pipeline = pipe.get(i, [])
        if not pipeline:
            continue
        pipeline.sort()
        inside = False
        for k in range(len(pipeline) - 1):
            if data[i][pipeline[k]] == "|" or \
                (data[i][pipeline[k]] == "F" and data[i][pipeline[k + 1]] == "J") or \
                (data[i][pipeline[k]] == "L" and data[i][pipeline[k + 1]] == "7"):
                inside = not inside
            if data[i][pipeline[k]] in ("F", "L"):
                continue
            if inside:
                cpt += pipeline[k + 1] - pipeline[k] - 1
    print(cpt)