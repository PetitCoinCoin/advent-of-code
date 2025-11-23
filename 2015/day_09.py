import argparse

from copy import deepcopy
from math import inf
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

def get_graph(vertices: set, edges: dict, raw: str) -> None:
    nodes = raw.split(" = ")[0].split(" to ")
    dist = int(raw.split(" = ")[1])
    vertices |= set(nodes)
    edges[nodes[0]] = edges.get(nodes[0], set()) | {(dist, nodes[1])}
    edges[nodes[1]] = edges.get(nodes[1], set()) | {(dist, nodes[0])}

def bruteforce(start: tuple, edges: dict, seen: set, min_wanted: bool = True) -> int:
    distance, node = start
    seen.add(node)
    children = [child for child in edges[node] if child[1] not in seen]
    if not children:
        return distance
    result_distance = inf if min_wanted else 0
    func = min if min_wanted else max
    for child in children:
        result_distance = func(result_distance, bruteforce(child, edges, deepcopy(seen), min_wanted))
    return distance + result_distance

if __name__ == "__main__":
    args = _parse_args()
    vertices = set()
    edges = dict()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            get_graph(vertices, edges, line)
    if args.part == 1:
        print(min([bruteforce((0, vertex), edges, set()) for vertex in vertices]))
    else:
        print(max([bruteforce((0, vertex), edges, set(), False) for vertex in vertices]))
