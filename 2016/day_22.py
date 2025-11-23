import argparse
import re

from dataclasses import dataclass
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

@dataclass
class Node:
    name: complex
    used: int
    avail: int
    size: int

def parse_input(raw: str) -> Node:
    groups = [int(x) for x in re.findall(r"x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)", raw)[0]]
    return Node(
        name=complex(groups[0], groups[1]),
        used=groups[3],
        avail=groups[4],
        size=groups[2],
    )

def pretty(node: Node) -> str:
    if not node.used:
        return "_"
    if node.size > 100:
        return "#"
    if node.name == complex(32, 0):
        return "G"
    return "."

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(raw) for raw in file.readlines() if raw.startswith("/dev")]
    if args.part == 1:
        viables = 0
        for i, node_a in enumerate(data):
            for node_b in data[i+1:]:
                if (node_a.used and node_a.used <= node_b.avail) or (node_b.used and node_b.used <= node_a.avail):
                    viables += 1
        print(viables)
    else:
        for i in range(30):
            y = data[i].name.imag
            print("".join([pretty(node) for node in data[i::30]]), int(y))
        # 12 to the left
        # 29 top
        # 29 to the right
        # 31 loop of 5 steps
        print(12 + 29 + 29 + 5 * 31)
