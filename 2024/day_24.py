import argparse

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
    id: int
    op1: str
    op2: str
    action: callable
    res: str

ACTION_MAP = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "XOR": lambda x, y: x ^ y,
}

def parse_init(raw: str) -> dict:
    res = {}
    for line in raw.split("\n"):
        k, v = line.split(": ")
        res[k] = int(v)
    return res

def parse_inst(raw: str) -> list[Instruction]:
    res = []
    for i, line in enumerate(raw.split("\n")):
        left, right = line.split(" -> ")
        op1, operator, op2 = left.split(" ")
        if operator == "XOR":
            if op1[0] not in "xy" and op2[0] not in "xy" and right[0] != "z":
                to_switch.add(right)
            if op1[0] in "xy" and op2[0] in "xy" and right[0] == "z" and right != "z00":
                to_switch.add(right)
        res.append(Instruction(
            id=i,
            op1=op1,
            op2=op2,
            action=ACTION_MAP[operator],
            res=right,
        ))
    return res

def simulate() -> None:
    seen = set()
    while len(seen) < len(instructions):
        for instruction in instructions:
            if instruction.id in seen:
                continue
            try:
                op1 = instruction.op1 if instruction.op1.isdigit() else data[instruction.op1]
                op2 = instruction.op2 if instruction.op2.isdigit() else data[instruction.op2]
            except KeyError:
                continue
            data[instruction.res] = instruction.action(op1, op2)
            seen.add(instruction.id)

def read_register(start: str) -> int:
    res = []
    for key, val in data.items():
        if key.startswith(start):
            res.append((int(key[1:]), str(val)))
    res.sort(reverse=True)
    return int("".join([x[1] for x in res]), 2)

def find_swap(op: str) -> str:
    for inst in instructions:
        if inst.op1 == op or inst.op2 == op:
            if inst.res.startswith("z"):
                return "z{:02d}".format(int(inst.res[1:]) - 1)
            else:
                return find_swap(inst.res)

def perform_swap() -> None:
    for res1, res2 in swap_pairs:
        for inst in instructions:
            if inst.res == res1:
                inst.res = res2
            elif inst.res == res2:
                inst.res = res1

def find_missing(idx: int) -> tuple:
    return tuple([
        inst.res
        for inst in instructions
        if inst.op1[1:].isdigit() and inst.op2[1:].isdigit() and int(inst.op1[1:])==idx and int(inst.op2[1::])
    ])

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        init, inst = file.read().split("\n\n")
    data = parse_init(init)
    to_switch = set()
    instructions = parse_inst(inst.strip())
    if args.part == 1:
        simulate()
        print(read_register("z"))
    else:
        # print(bin(x + y - z)) and search for errors
        # Found 3 pairs to swap that way:
        # mwk - Z10
        # z18 - qgd
        # hsw - jmh
        # At this point, this already seemed to work fine. I was checking the rest manually, started to give up.
        # Someone suggested to change the input, so I tried with x=17592186044415 (only 1s)  and z=0.
        # Found the last swap with same method as previously (which was just the next check I was supposed to make)
        # gqp, z33
        # Then print(",".join(sorted(["mwk", "z10", "z18", "qgd", "hsw", "jmh", "gqp", "z33"])))

        # Later tried the programmatic approach thanks to this post: https://shorturl.at/espZf
        swap_pairs = [(item, find_swap(item)) for item in to_switch]
        perform_swap()
        simulate()
        delta = read_register("x") + read_register("y") - read_register("z")
        diff_bit = bin(delta)[2 if delta else 3:][::-1].index('1')
        swap_pairs.extend([find_missing(diff_bit)])
        print(",".join(sorted([item for pair in swap_pairs for item in pair])))
    print(time() - t)
