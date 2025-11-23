import argparse

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
class Instruction:
    action_item: str
    action: str
    action_value: int
    condition_item: str
    condition: str
    condition_value: int

ACTION_MAP = {
    "inc": lambda x, y: x + y,
    "dec": lambda x, y: x - y,
}

CONDITION_MAP = {
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
}

def parse_input(raw: str) -> Instruction:
    elements = raw.split(" ")
    return Instruction(
        action_item=elements[0],
        action=elements[1],
        action_value=int(elements[2]),
        condition_item=elements[4],
        condition=elements[5],
        condition_value=int(elements[6]),
    )

def compute_registers(instructions: list[Instruction]) -> tuple[int, dict]:
    registers = dict()
    max_value = 0
    for instruction in instructions:
        if not CONDITION_MAP[instruction.condition](registers.get(instruction.condition_item, 0), instruction.condition_value):
            continue
        new_value = ACTION_MAP[instruction.action](registers.get(instruction.action_item, 0), instruction.action_value)
        registers[instruction.action_item] = new_value
        if new_value > max_value:
            max_value = new_value
    return max_value, registers

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().split("\n")]
    max_val, reg = compute_registers(data)
    if args.part == 1:
        print(max(reg.values()))
    else:
        print(max_val)
