from __future__ import annotations

import re

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Node:
    name: str
    proba: int
    children: list

def format_workflow(workflow: str) -> tuple:
    children = []
    proba = {
        "x": [range(1, 4001)],
        "m": [range(1, 4001)],
        "a": [range(1, 4001)],
        "s": [range(1, 4001)],
    }
    for i, instruction in enumerate(workflow[:-1].split("{")[1].split(",")):
        groups = re.findall(r"(\w{1})(<|>)(\d+):(\w+)", instruction)
        if groups:
            criterion = groups[0][0]
            init_proba = deepcopy(proba)
            if groups[0][1] == ">":
                init_proba[criterion] += [range(int(groups[0][2]) + 1, 4001)]
                children.append(Node(
                    name=groups[0][3],
                    proba=init_proba,
                    children=[],
                ))
                proba[criterion] = proba[criterion] + [range(1, int(groups[0][2]) + 1)]
            else:
                init_proba[criterion] += [range(1, int(groups[0][2]))]
                children.append(Node(
                    name=groups[0][3],
                    proba=init_proba,
                    children=[],
                ))
                proba[criterion] = proba[criterion] + [range(int(groups[0][2]), 4001)]
        else:
            children.append(Node(name=instruction, proba=proba, children=[]))
    return workflow.split("{")[0], children

def build_tree(workflows: dict, root: Node) -> Node:
    for node in workflows[root.name]:
        node_proba = deepcopy(node.proba)
        for k, v in node_proba.items():
            node_proba[k] = [range(max(*[r[0] for r in v + root.proba[k]]), min(*[r[-1] for r in v + root.proba[k]]) + 1)]
        node.proba = node_proba
        if node.name in ("A", "R"):
            root.children.append(node)
        else:
            root.children.append(build_tree(workflows, node))
    return root

def get_combinations(tree: Node) -> int:
    result = 0
    if not tree.children:
        if tree.name == "A":
            combinations = 1
            for r in tree.proba.values():
                combinations *= len(r[0])
            return combinations
        return 0
    else:
        for child in tree.children:
            result += get_combinations(child)
    return result

if __name__ == "__main__":
    with Path("day_19/input.txt").open("r") as file:
        workflows = {}
        while line := file.readline():
            if line.strip():
                name, workflow = format_workflow(line.strip())
                workflows[name] = workflow
            else:
                break
    tree = build_tree(
        workflows,
        Node("in", {
            "x": [range(1, 4001)],
            "m": [range(1, 4001)],
            "a": [range(1, 4001)],
            "s": [range(1, 4001)],
        }, []))
    print(get_combinations(tree))
