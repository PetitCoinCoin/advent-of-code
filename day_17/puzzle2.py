from dataclasses import dataclass, field
from heapq import heappop, heappush
from math import inf
from pathlib import Path

@dataclass
class Step:
    source: tuple
    straight_count: int
    direction: str

NEXT_DIRECTION = {
    "right": ("up", "down"),
    "left": ("up", "down"),
    "up": ("right", "left"),
    "down": ("right", "left"),
    "": ("right", "down"),
}
DIRECTION_DELTA = {
    "right": (0, 1),
    "left": (0, -1),
    "up": (-1, 0),
    "down": (1, 0),
}
N, M = 141, 141

def calculate_position(source: tuple, direction: str) -> tuple:
    return (source[0] + DIRECTION_DELTA[direction][0], source[1] + DIRECTION_DELTA[direction][1])

def is_valid(position: tuple) -> bool:
    return 0 <= position[0] < N and 0 <= position[1] < M

def neighbors(step: tuple, data: list) -> list:
    source, straight_count, current_direction = step
    neighbors = []
    if not current_direction:
        for direction in NEXT_DIRECTION[current_direction]:
            next_step = calculate_position(source, direction)
            if is_valid(next_step):
                neighbors.append((data[next_step[0]][next_step[1]], (next_step, 1, direction)))
    else:
        if straight_count >= 4:
            for direction in NEXT_DIRECTION[current_direction]:
                next_step = calculate_position(source, direction)
                if is_valid(next_step):
                    neighbors.append((data[next_step[0]][next_step[1]], (next_step, 1, direction)))
        straight_next_step = calculate_position(source, current_direction)
        if straight_count < 10 and is_valid(straight_next_step):
            neighbors.append((data[straight_next_step[0]][straight_next_step[1]], (straight_next_step, straight_count + 1, current_direction)))
    return neighbors

if __name__ == "__main__":
    with Path("day_17/input.txt").open("r") as file:
        data = [[int(x) for x in row]for row in file.read().splitlines()]
    start = (0, 0), 0, ""
    queue = [(0, start)]
    dists = {start : 0}

    while len(queue) > 0:
        heat_loss, step = heappop(queue)
        source, count, direction = step
        if source[0] == N - 1 and source[1] == M - 1:
            print(heat_loss)
            break
        for neighbor in neighbors(step, data):
            loss, next_step = neighbor
            if heat_loss + loss < dists.get(next_step, inf):
                dists[next_step] = heat_loss + loss
                heappush(queue, (heat_loss + loss, next_step))
