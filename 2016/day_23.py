import argparse

from math import factorial
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

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        instructions = [parse_input(raw) for raw in file.readlines()]
    # Lines 20 and 21 from input file do the trick here
    print(factorial(7 if args.part == 1 else 12) + int(instructions[19].val) * int(instructions[20].val))
