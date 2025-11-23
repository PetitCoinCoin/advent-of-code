import argparse
import math

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

REGISTER = {i: 0 for i in range(6)}

OPCODES = {
    "addr": lambda x, y: REGISTER[x] + REGISTER[y],
    "addi": lambda x, y: REGISTER[x] + y,
    "mulr": lambda x, y: REGISTER[x] * REGISTER[y],
    "muli": lambda x, y: REGISTER[x] * y,
    "banr": lambda x, y: REGISTER[x] & REGISTER[y],
    "bani": lambda x, y: REGISTER[x] & y,
    "borr": lambda x, y: REGISTER[x] | REGISTER[y],
    "bori": lambda x, y: REGISTER[x] | y,
    "setr": lambda x, _: REGISTER[x],
    "seti": lambda x, _: x,
    "gtir": lambda x, y: int(x > REGISTER[y]),
    "gtri": lambda x, y: int(REGISTER[x] > y),
    "gtrr": lambda x, y: int(REGISTER[x] > REGISTER[y]),
    "eqir": lambda x, y: int(x == REGISTER[y]),
    "eqri": lambda x, y: int(REGISTER[x] == y),
    "eqrr": lambda x, y: int(REGISTER[x] == REGISTER[y]),
}

@dataclass
class Instruction:
    opcode: int
    a: int
    b: int
    c: int

def parse_input(raw: str) -> Instruction:
    opcode, a, b, c = raw.split(" ")
    return Instruction(
        opcode=opcode,
        a=int(a),
        b=int(b),
        c=int(c),
    )

def run() -> None:
    ip = REGISTER[ipr]
    while ip in range(len(data)):
        REGISTER[ipr] = ip
        inst = data[ip]
        REGISTER[inst.c] = OPCODES[inst.opcode](inst.a, inst.b)
        ip = REGISTER[ipr] + 1

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        raw_data = file.read().split("\n")
    ipr = int(raw_data[0][4:])
    data = [parse_input(line) for line in raw_data[1:] if line]
    # This works for part 1, but part 2's approach is way quicker!
    # Just keeping it for archive purpose
    # run()
    # print(REGISTER[0])

    # As usual, we need to dive in and understand what it does :)
    # First part (end of instructions) just sets registers 2 and 5.
    # Beginning with register 0 at 1 considerably increases the end values
    # (and thus number of loops that will happen after).
    reg_2 = REGISTER[2] + 2
    reg_2 *= reg_2
    reg_2 = (19 * reg_2) * 11
    reg_5 = (REGISTER[5] + 4) * 22 + 16
    reg_2 += reg_5
    if args.part == 2:
        reg_5 = (27 * 28 + 29) * 30 * 14 * 32
        reg_2 += reg_5
    # Then the loops begin: we sum the different factors that compose reg 2
    # (decomposition in 2 factors - can't express this correctly in english)
    result = 0
    for i in range(1, int(math.sqrt(reg_2)) + 1):
        quotient, rest = divmod(reg_2, i)
        if not rest:
            result += i
            if quotient!= i:
                result += quotient
    print(result)
    print(time() - t)
