import argparse

from contextlib import suppress
from heapq import heappop, heappush
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

MAX = 7

def parse_input(line: int, raw: str, data_dict: dict) -> None:
    for column, char in enumerate(raw):
        if char == "#":
            continue
        data_dict[complex(line, column)] = char

def bfs_distances(start: complex, end: complex) -> int:
    queue = [(0, (start.real, start.imag))]
    seen = {start}
    while queue:
        dist, step = heappop(queue)
        complex_step = complex(step[0], step[1])
        if complex_step == end:
            return dist
        for s in (1, -1, 1j, -1j):
            if complex_step + s not in seen and data.get(complex_step + s):
                complex_next = complex_step + s
                heappush(queue, (dist + 1, (complex_next.real, complex_next.imag)))
                seen.add(complex_next)
    return 0

def walk(start: int, distances: dict, part_one: bool) -> int:
    start = 0
    queue = [(0, start, {start}, [start])]
    while queue:
        dist, step, seen, path = heappop(queue)
        if len(seen) == MAX + 1 and part_one:
            return dist
        # part two
        if len(seen) == MAX + 1 and path[-1] == start:
            return dist
        for next_step in distances[step]:
            value, additional_dist = next_step
            heappush(queue, (dist + additional_dist, value, seen | {value}, path + [value]))
    return 0
    

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = {}
        for line, raw in enumerate(file.read().split("\n")):
            parse_input(line, raw, data)
    coordinates = {}
    for key, value in data.items():
        with suppress(ValueError):
            int_val = int(value)
            coordinates[int_val] = key
    distances = {}
    for i in range(MAX + 1):
        for j in range(i + 1, MAX + 1):
            dist = bfs_distances(coordinates[i], coordinates[j])
            distances[i] = distances.get(i, set()) | {(j, dist)}
            distances[j] = distances.get(j, set()) | {(i, dist)}
    print(walk(0, distances, args.part == 1))
