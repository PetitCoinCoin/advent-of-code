from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Instruction:
    result: str
    criterion: str | None = None
    is_greater: bool | None = None
    value: int | None = None

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

if __name__ == "__main__":
    with Path("day_19/input.txt").open("r") as file:
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