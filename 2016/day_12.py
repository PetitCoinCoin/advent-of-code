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
    val: str
    dest: str
    action: str

ACTIONS_MAP = {
    "inc": lambda x: x + 1,
    "dec": lambda x: x - 1,
}

def parse_input(raw: str) -> Instruction:
    elements = raw.strip().split(" ")
    if elements[0] == "cpy":
        value = elements[1]
        destination = elements[2]
    elif elements[0] == "jnz":
        value = elements[1]
        destination = elements[2]
    else:
        value = ""
        destination = elements[1]
    return Instruction(
        action=elements[0],
        val=value,
        dest=destination,
    )

def process(instructions: list, part_one: bool) -> int:
    data = {
        "a": 0,
        "b": 0,
        "c": 0 if part_one else 1,
        "d": 0,
    }
    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        if instruction.action in ("inc", "dec"):
            data[instruction.dest] = ACTIONS_MAP[instruction.action](data[instruction.dest])
            i += 1
        elif instruction.action == "cpy":
            data[instruction.dest] = int(instruction.val) if instruction.val.isdigit() else data[instruction.val]
            i += 1
        else:
            if instruction.val.isdigit() and int(instruction.val):
                i += int(instruction.dest)
            else:
                i += int(instruction.dest) if data.get(instruction.val, "0") else 1
    return data["a"]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        instructions = [parse_input(raw) for raw in file.readlines()]
    print(process(instructions, args.part == 1))
