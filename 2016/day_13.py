import argparse

from collections import Counter
from heapq import heappop, heappush
from pathlib import Path
from math import inf

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

def is_open_space(x: int, y: int) -> bool:
    return not(bool(Counter(bin(x *x + 3 * x + 2 * x *y + y + y * y + FAVORITE))["1"] % 2))

def next_steps(x: int, y: int) -> list:
    return [
        (nx, ny)
        for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        if nx >= 0 and ny >= 0 and is_open_space(nx, ny)
    ]

def dijsktra(gx: int, gy: int) -> int:
    start = (1, 1)
    dists = {start: 0}
    queue = [(0, start)]
    while queue:
        dist, step = heappop(queue)
        x, y = step
        if x == gx and y == gy:
            return dist
        for next_step in next_steps(x, y):
            if dist + 1 < dists.get(next_step, inf):
                heappush(queue, (dist + 1, next_step))
                dists[next_step] = dist + 1
    return 0

def bfs(max_step: int) -> int:
    start = (1, 1)
    queue = [(0, start)]
    seen = {start}
    while queue:
        dist, step = heappop(queue)
        x, y = step
        for next_step in next_steps(x, y):
            if next_step not in seen and dist < max_step:
                seen.add(next_step)
                heappush(queue, (dist + 1, next_step))
    return len(seen)

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        FAVORITE = int(file.read().strip())
    if args.part == 1:
        print(dijsktra(31, 39))
    else:
        print(bfs(50))
