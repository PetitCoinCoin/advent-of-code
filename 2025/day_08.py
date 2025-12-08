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

def build_circuits() -> list:
    pairs = sorted(get_pairs())
    pairs = [(pos1, pos2) for _, pos1, pos2 in pairs[:1000]]
    circuits = [set([pairs[0][0], pairs[0][1]])]
    for pos1, pos2 in pairs[1:]:
        for circuit in circuits:
            if pos1 in circuit or pos2 in circuit:
                circuit |= {pos1, pos2}
                break
        else:
            circuits.append({pos1, pos2})
    return circuits

def connect_circuits(circ: list) -> list:
    prev_len = 0
    while len(circ) != prev_len:
        prev_len = len(circ)
        connected = [circ[0]]
        for circuit in circ[1:]:
            for c in connected:
                if c.intersection(circuit):
                    c |= circuit
                    break
            else:
                connected.append(circuit)
        circ = connected
    return circ

def build_one_circuit() -> list:
    pairs = sorted(get_pairs())
    pairs = [(pos1, pos2) for _, pos1, pos2 in pairs]
    circuits = [set([pairs[0][0], pairs[0][1]])]
    for pos1, pos2 in pairs[1:]:
        for circuit in circuits:
            if pos1 in circuit or pos2 in circuit:
                circuit |= {pos1, pos2}
                break
        else:
            circuits.append({pos1, pos2})
        circuits = connect_circuits(circuits)
        if len(circuits) == 1 and len(circuits[0]) == len(data):
            return pos1[0] * pos2[0]
    return 0

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [tuple(map(int, line.split(","))) for line in file.read().strip().split("\n")]
    if args.part == 1:
        circuits = build_circuits()
        circuits = [len(c) for c in connect_circuits(circuits)]
        circuits.sort(reverse=True)
        print(prod(circuits[:3]))
    else:
        print(build_one_circuit())
    print(time() - t)
