import argparse
import re

from heapq import heappop, heappush
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

TOOL_MAP = {
    0: ("T", "C"),
    1: ("C", "N"),
    2: ("T", "N"),
}

def erosion_level(geo_idx: int) -> int:
    return (geo_idx + depth) % 20183

def set_erosion(x: int, y: int) -> None:
    if not x:
        erosion_map[(x, y)] = erosion_level(48271 * y)
    elif not y:
        erosion_map[(x, y)] = erosion_level(16807 * x)
    else:
        if erosion_map.get((x - 1, y)) is None:
            set_erosion(x - 1, y)
        if erosion_map.get((x, y - 1)) is None:
            set_erosion(x, y - 1)
        erosion_map[(x, y)] = erosion_level(erosion_map[(x - 1, y)] * erosion_map[(x, y - 1)])

def build_map() -> None:
    for y in range(0, ty + 1):
        for x in range(0, tx + 1):
            if (x, y) == (tx, ty):
                erosion_map[(x, y)] = erosion_level(0)
            else:
                set_erosion(x, y)

def get_neighbours(position: tuple, tool: str) -> list:
    other_tool = next((t for t in TOOL_MAP[erosion_map[position] % 3] if t != tool))
    x, y = position
    result = [(7, (x, y), other_tool)]
    for dx, dy in zip((0, 0, 1, -1), (1, -1, 0, 0)):
        if x + dx >= 0 and y + dy >= 0:
            if erosion_map.get((x + dx, y + dy)) is None:
                set_erosion(x + dx, y + dy)
            if tool in TOOL_MAP[erosion_map[(x + dx, y + dy)] % 3]:
                result.append((1, (x + dx, y + dy), tool))
    return result

def walk() -> int:
    seen = set()
    queue = []
    heappush(queue, (0, (0, 0), "T"))
    while queue:
        duration, position, tool = heappop(queue)
        if position == (tx, ty) and tool == "T":
            return duration
        if (position, tool) in seen:
            continue
        seen.add((position, tool))
        for delay, neighbour, new_tool in get_neighbours(position, tool):
            if (neighbour, new_tool) in seen:
                continue
            heappush(queue, (duration + delay, neighbour, new_tool))
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    pattern = r"depth: (\d+)\ntarget: (\d+),(\d+)"
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read()
    depth, tx, ty = map(int, re.findall(pattern, data)[0])
    erosion_map = {}
    build_map()
    if args.part == 1:
        print(sum(erosion % 3 for erosion in erosion_map.values()))
    else:
        print(walk())
    print(time() - t)
