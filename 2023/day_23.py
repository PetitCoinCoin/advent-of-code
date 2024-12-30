import argparse

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

SIZE = 140

def is_valid_child(step: tuple, r: int, c: int, value: str) -> bool:
    if value == ".":
        return True
    if value == "#":
        return False
    if step[0] == r:
        return (c > step[1] and value != "<") or (c < step[1] and value != ">")
    return (r > step[0] and value != "^") or (r < step[0] and value !="v")

def next_steps(step: tuple, data: list, prev_r: int, prev_c: int) -> list:
    if data[step[0]][step[1]] == ">":
        return [(step[0], step[1] + 1)]
    elif data[step[0]][step[1]] == "^":
        return [(step[0] - 1, step[1])]
    elif data[step[0]][step[1]] == "<":
        return [(step[0], step[1] - 1)]
    elif data[step[0]][step[1]] == "v":
        return [(step[0] + 1, step[1])]
    else:
        result = []
        for i, j in (
            (step[0], step[1] + 1),
            (step[0] - 1, step[1]),
            (step[0], step[1] - 1),
            (step[0] + 1, step[1]),
        ):
            if len(data) > i >= 0 and len(data[0]) > j >= 0 and \
                (i != prev_r or j != prev_c) and \
                is_valid_child(step, i, j, data[i][j]):
                result.append((i, j))
        return result

def build_tree(root: tuple, data: list, paths: dict) -> None:
    q = [(root, 0, 0)]
    seen = dict()
    while q:
        node, prev_r, prev_c = q.pop(0)
        seen[node] = True
        children = next_steps(node, data, prev_r, prev_c)
        for child in children:
            paths[child] = paths[node] + 1
            q.append((child, node[0], node[1]))           

def get_adjacents(step: tuple, data: list) -> list:
    result = []
    for i, j in (
        (step[0], step[1] + 1),
        (step[0] - 1, step[1]),
        (step[0], step[1] - 1),
        (step[0] + 1, step[1]),
    ):
        if len(data) > i >= 0 and len(data[0]) > j >= 0 and data[i][j] != "#":
            result.append((i, j))
    return result

def contract(step: tuple, source: tuple, edges: dict, seen: dict, destination: tuple) -> tuple:
    distance = 1
    adjacents = get_adjacents(step, data)
    while len(adjacents) == 2 or step == (0, 1):
        distance += 1
        seen.add(step)
        step = [n for n in adjacents if n not in seen][0]
        adjacents = get_adjacents(step, data)
    if distance > 1:
        edges[source] = edges.get(source, set()) | {(distance, step)}
        edges[step] = edges.get(step, set()) | {(distance, source)}
    return step, distance

def get_contracted_graph(data: dict, source: tuple, destination: tuple) -> dict:
    edges = dict()
    seen = set()
    queue = [source]
    while queue:
        start = queue.pop(0)
        step = start
        adjacents = get_adjacents(step, data)
        if len(adjacents) > 2:
            seen.add(start)
            for child in [n for n in adjacents if n not in seen]:
                seen.add(child)
                node, dist = contract(child, step, edges, seen, destination)
                if dist > 1:
                    queue.append(node)
            seen.remove(start)
        else:
            node, dist = contract(step, step, edges, seen, destination)
            if dist > 1:
                queue.append(node)
    return edges

def longest_path(step: tuple, destination: tuple, edges: dict, distance: int = 0, seen: set = set()) -> int:
    if step == destination:
        return distance
    seen.add(step)
    max_path = 0
    for dist, neighbor in edges[step]:
        if neighbor in seen:
            continue
        max_path = max(max_path, longest_path(neighbor, destination, edges, distance + dist, seen))
    seen.remove(step)
    return max_path

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        start = (0, 1)
        paths = { start: 0 }
        build_tree(start, data, paths)
        print(paths[(SIZE, SIZE - 1)])
    else:
        size = len(data)  # square data
        start = (0, 1)
        destination = (size - 1, size - 2)
        edges = get_contracted_graph(data, start, destination)
        print(longest_path(start, destination, edges) - 1)  # - 1 because path from start to 1st node is 1 unit too long.
    print(time() - t)
