import argparse

from copy import deepcopy
from pathlib import Path
from random import randrange
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

def parse_input(row: str) -> tuple:
    vertice = row.split(": ")[0]
    neighbors = row.split(": ")[1].split(" ")
    return vertice, neighbors

def contract(data: dict) -> None:
    while len(data.keys()) > 2:
        keys = list(data.keys())
        node_a = keys[randrange(len(keys))]
        neighbors = data[node_a]
        node_b = neighbors[randrange(len(neighbors))]
        data[f"{node_a}-{node_b}"] = [n for n in data[node_a] + data[node_b] if n != node_a and n != node_b]
        for n in data[node_a]:
            data[n].remove(node_a)
        for n in data[node_b]:
            data[n].remove(node_b)
        for n in data[f"{node_a}-{node_b}"]:
            data[n].append(f"{node_a}-{node_b}")
        del data[node_a]
        del data[node_b]

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            vertice, neighbors = parse_input(line.strip())
            data[vertice] = data.get(vertice, []) + neighbors
            for n in neighbors:
                data[n] = data.get(n, []) + [vertice]
    if args.part == 1:
        to_be_contracted = deepcopy(data)
        contract(to_be_contracted)
        keys = list(to_be_contracted.keys())
        while len(to_be_contracted[keys[0]]) > 3:
            to_be_contracted = deepcopy(data)
            contract(to_be_contracted)
            keys = list(to_be_contracted.keys())
        subgraphs = [len(key.split("-")) for key in keys]
        print(subgraphs[0] * subgraphs[1])
    else:
        raise NotImplementedError
    print(time() - t)

