from math import prod
from itertools import combinations
from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def square_distance(pos1: tuple, pos2: tuple) -> int:
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2

def get_pairs() -> list:
    return [
        (square_distance(pos1, pos2), pos1, pos2)
        for pos1, pos2 in combinations(data, 2)
    ]

def build_circuits(count: int = 0) -> list:
    pairs = sorted(get_pairs())
    if count:
        pairs = pairs[:count]
    pairs = [(pos1, pos2) for _, pos1, pos2 in pairs]
    circuits = {0: {pairs[0][0], pairs[0][1]}}
    junction_to_circuit = {
        pairs[0][0]: 0,
        pairs[0][1]: 0,
    }
    next_circuit = 1
    max_circuit = 2
    for pos1, pos2 in pairs[1:]:
        circuit1 = junction_to_circuit.get(pos1)
        circuit2 = junction_to_circuit.get(pos2)
        if circuit1 is None and circuit2 is None:
            circuits[next_circuit] = {pos1, pos2}
            junction_to_circuit[pos1] = next_circuit
            junction_to_circuit[pos2] = next_circuit
            next_circuit += 1
        elif circuit1 is None:
            circuits[circuit2].add(pos1)
            junction_to_circuit[pos1] = circuit2
            max_circuit = max(max_circuit, len(circuits[circuit2]))
        elif circuit2 is None:
            circuits[circuit1].add(pos2)
            junction_to_circuit[pos2] = circuit1
            max_circuit = max(max_circuit, len(circuits[circuit1]))
        elif circuit1 == circuit2:
            continue
        else:
            circuits[circuit1] |= circuits[circuit2]
            for junction in circuits[circuit2]:
                junction_to_circuit[junction] = circuit1
            del circuits[circuit2]
            max_circuit = max(max_circuit, len(circuits[circuit1]))
        if not count and max_circuit == len(data):
            return [pos1, pos2]
    return circuits.values()

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [tuple(map(int, line.split(","))) for line in file.read().strip().split("\n")]
    if args.part == 1:
        circuits = [len(c) for c in build_circuits(1000)]
        circuits.sort(reverse=True)
        print(prod(circuits[:3]))
    else:
        junction1, junction2 = build_circuits()
        print(junction1[0] * junction2[0])
    print(time() - t)
