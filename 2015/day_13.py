import argparse
import re

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

def get_nodes(row: str, nodes: dict) -> None:
    node1 = row.split(" ")[0]
    node2 = row.split(" ")[-1][:-1]
    happiness = int(re.search(r"\d+", row).group())
    if "lose" in row:
        happiness = -happiness
    for n, m in zip((node1, node2), (node2, node1)):
        nodes[n] = nodes.get(n, {})
        nodes[n][m] = nodes[n].get(m, 0) + happiness

def max_happiness(step: str, happiness: int, seen: set, nodes: dict, start: str) -> int:
    if len(seen) == len(nodes.keys()) - 1:
        return happiness + nodes[step][start]
    seen.add(step)
    max_happy = 0
    for neighbor, happy in nodes[step].items():
        if neighbor in seen:
            continue
        max_happy = max(max_happy, max_happiness(neighbor, happiness + happy, seen, nodes, start))
    seen.remove(step)
    return max_happy

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    nodes = dict()
    for row in data:
        get_nodes(row, nodes)
    if args.part == 1:
        print(max_happiness("Alice", 0, set(), nodes, "Alice"))
    else:
        me = "Andréa"
        nodes[me] = dict()
        for node in nodes.keys():
            nodes[me][node] = 0
            nodes[node][me] = 0
        # Global happiness decreases when I'm sitting at the table :'(
        print(max_happiness(me, 0, set(), nodes, me))
