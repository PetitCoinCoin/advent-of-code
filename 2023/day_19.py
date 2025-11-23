import argparse
import re

from copy import deepcopy
from dataclasses import dataclass
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

@dataclass
class Instruction:
    result: str
    criterion: str | None = None
    is_greater: bool | None = None
    value: int | None = None

@dataclass
class Node:
    name: str
    proba: int
    children: list

def format_workflow(workflow: str) -> tuple:
    name = workflow.split("{")[0]
    instructions = []
    for instruction in workflow[:-1].split("{")[1].split(","):
        groups = re.findall(r"(\w{1})(<|>)(\d+):(\w+)", instruction)
        if groups:
            instructions.append(Instruction(
                criterion = groups[0][0],
                is_greater = groups[0][1] == ">",
                value = int(groups[0][2]),
                result = groups[0][3],
            ))
        else:
            instructions.append(Instruction(result = instruction))
    return name, instructions

def format_rating(rating: str) -> dict:
    formatted = {}
    for criterion in ("x", "m", "a", "s"):
        pattern = re.escape(criterion) + r"=(\d+)"
        value = re.findall(pattern, rating)
        formatted[criterion] = int(value[0]) if value else None
    return formatted

def process(rating: dict, workflows: dict, start: str) -> str:
    for instruction in workflows[start]:
        if instruction.criterion is not None and rating[instruction.criterion] is not None:
            if not (instruction.is_greater ^ (rating[instruction.criterion] > instruction.value)):
                return instruction.result if instruction.result in ("A", "R") else process(rating, workflows, instruction.result)
        else:
            return instruction.result if instruction.result in ("A", "R") else process(rating, workflows, instruction.result)

def format_workflow_2(workflow: str) -> tuple:
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
    args = _parse_args()
    t = time()
    if args.part == 1:
        with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
            is_workflow = True
            workflows = {}
            ratings = []
            while line := file.readline():
                if line.strip():
                    if is_workflow:
                        name, workflow = format_workflow(line.strip())
                        workflows[name] = workflow
                    else:
                        ratings.append(format_rating(line.strip()))
                else:
                    is_workflow = False
        accepted = [
            rating for rating in ratings
            if process(rating, workflows, "in") == "A"
        ]
        print(sum([sum(rating.values()) for rating in accepted]))
    else:
        with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
            workflows = {}
            while line := file.readline():
                if line.strip():
                    name, workflow = format_workflow_2(line.strip())
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
    print(time() - t)

