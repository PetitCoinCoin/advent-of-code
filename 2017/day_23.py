import argparse

from collections import deque
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
    action: str
    reg: str | int
    value: str | int | None = None

def parse_input(raw: str) -> Instruction:
    elements = raw.split(" ")
    if elements[1].isdigit() or elements[1].startswith("-"):
        elements[1] = int(elements[1])
    if len(elements) > 2 and (elements[2].isdigit() or elements[2].startswith("-")):
        elements[2] = int(elements[2])
    if elements[0] in ("snd", "rcv"):
        return Instruction(
            action=elements[0],
            reg=elements[1],
        )
    return Instruction(
        action=elements[0],
        reg=elements[1],
        value=elements[2],
    )

def debug(instructions: list) -> int:
    register = dict()
    count_mul = 0
    i = 0
    while 0 <= i < len(instructions):
        inst = instructions[i]
        delta = 1
        if inst.action == "set":
            register[inst.reg] = inst.value if isinstance(inst.value, int) else register.get(inst.value, 0)
        elif inst.action == "sub":
            register[inst.reg] = register.get(inst.reg, 0) - (inst.value if isinstance(inst.value, int) else register.get(inst.value, 0))
        elif inst.action == "mul":
            register[inst.reg] = register.get(inst.reg, 0) * (inst.value if isinstance(inst.value, int) else register.get(inst.value, 0))
            count_mul += 1
        elif inst.action == "jnz":
            if (isinstance(inst.reg, int) and inst.reg != 0) or (isinstance(inst.reg, str) and register.get(inst.reg, 0) != 0):
                delta = inst.value if isinstance(inst.value, int) else register.get(inst.value, 0)
        else:
            print("WTF")
            return -1
        i += delta
    return count_mul

def is_not_prime(val: int) -> bool:
    for i in range(2, val // 2):
        if not val % i:
            return True
    return False

def recover_h() -> int:
    b = 67 * 100 + 100000
    c = b + 17000
    return sum([is_not_prime(i) for i in range(b, c + 1, 17)])

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().split("\n")]
    if args.part == 1:
        print(debug(data))
    else:
        print(recover_h())
