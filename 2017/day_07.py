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
    weight: int
    children: list[str]

def parse_input(raw: str) -> tuple[str, Node]:
    pattern = r"([a-zA-Z]+) \((\d+)\)"
    result = re.search(pattern, raw)

    children = []
    split = raw.split(" -> ")
    if len(split) == 2:
        children = [x.strip() for x in split[-1].split(", ")]

    return result.group(1), Node(int(result.group(2)), children)

def find_root(graph: dict) -> str:
    keys = set(graph.keys())
    children = set(child for node in graph.values() for child in node.children)
    return (keys - children).pop()

def update_weight(graph: dict, node: str) -> int:
    if not graph[node].children:
        return graph[node].weight
    weight = graph[node].weight + sum([update_weight(graph, child) for child in graph[node].children])
    graph[node].weight = weight
    return weight

if __name__ == "__main__":
    args = _parse_args()
    data = dict()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            key, value = parse_input(line)
            data[key] = value
    root = find_root(data)
    if args.part == 1:
        print(root)
    else:
        update_weight(data, root)
        new_weight = None
        queue = [(root, 0)]
        while new_weight is None:
            key, expected = queue.pop(0)
            node = data[key]
            if len(node.children) > 2:
                for i in range(0, len(node.children) - 1):
                    if data[node.children[i]].weight == data[node.children[i + 1]].weight:
                        continue
                    else:
                        if i > 0:
                            queue.append((node.children[i + 1], data[node.children[i]].weight))
                            break
                        if data[node.children[0]].weight == data[node.children[-1]].weight:
                            queue.append((node.children[1], data[node.children[0]].weight))
                            break
                        queue.append((node.children[0], data[node.children[1]].weight))
                        break
                else:
                    new_weight = expected - sum(data[child].weight for child in node.children)
            # is this branch even possible? nah.
            elif len(node.children) == 2:
                if data[node.children[0]].weight != data[node.children[1]].weight:
                    queue.append((node.children[0], data[node.children[1]].weight))
                    queue.append((node.children[1], data[node.children[0]].weight))
                else:
                    new_weight = expected - sum(data[child].weight for child in node.children)
        print(new_weight)
