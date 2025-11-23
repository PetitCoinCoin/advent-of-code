import argparse

from contextlib import suppress
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
    opcode: int
    a: int
    b: int
    c: int

@dataclass
class Sample:
    before: dict
    after: dict
    instruction: Instruction

OPCODES = {
    "addr": lambda x, y, reg: reg[x] + reg[y],
    "addi": lambda x, y, reg: reg[x] + y,
    "mulr": lambda x, y, reg: reg[x] * reg[y],
    "muli": lambda x, y, reg: reg[x] * y,
    "banr": lambda x, y, reg: reg[x] & reg[y],
    "bani": lambda x, y, reg: reg[x] & y,
    "borr": lambda x, y, reg: reg[x] | reg[y],
    "bori": lambda x, y, reg: reg[x] | y,
    "setr": lambda x, _, reg: reg[x],
    "seti": lambda x, _, _r: x,
    "gtir": lambda x, y, reg: int(x > reg[y]),
    "gtri": lambda x, y, reg: int(reg[x] > y),
    "gtrr": lambda x, y, reg: int(reg[x] > reg[y]),
    "eqir": lambda x, y, reg: int(x == reg[y]),
    "eqri": lambda x, y, reg: int(reg[x] == y),
    "eqrr": lambda x, y, reg: int(reg[x] == reg[y]),
}

def parse_input(raw: str) -> Sample:
    before_raw, opcode_raw, after_raw = raw.split("\n")
    before = {i: int(x) for i, x in enumerate(before_raw[9:-1].split(", "))}
    after = {i: int(x) for i, x in enumerate(after_raw[9:-1].split(", "))}
    opcode = [int(x) for x in opcode_raw.split(" ")]
    return Sample(
        before=before,
        after=after,
        instruction=Instruction(*opcode)
    )

def parse_program(raw: str) -> Instruction:
    return Instruction(*[int(x) for x in raw.split(" ")])

def is_like_three_or_more(sample: Sample) -> bool:
    has_matched = 0
    for opcode in OPCODES.values():
        for key in range(4):
            if key != sample.instruction.c and sample.before[key] != sample.after[key]:
                print("WTF")
                return False
            if key == sample.instruction.c:
                if opcode(sample.instruction.a, sample.instruction.b, sample.before) == sample.after[key]:
                    has_matched += 1
                    if has_matched >= 3:
                        return True
    return False

def identify_opcodes(sample: Sample) -> None:
    # Already identified
    if len(opcodes.get(sample.instruction.opcode, set())) == 1:
        return
    # Find matching opcodes
    matching = set()
    for opcode, func in OPCODES.items():
        # Logic is simplified based on part 1
        if func(sample.instruction.a, sample.instruction.b, sample.before) == sample.after[sample.instruction.c]:
            matching.add(opcode)
    if not matching:
        return
    if opcodes.get(sample.instruction.opcode):
        opcodes[sample.instruction.opcode] = matching.intersection(opcodes[sample.instruction.opcode])
    else:
        opcodes[sample.instruction.opcode] = matching

def is_clean() -> bool:
    for matching in opcodes.values():
        if len(matching) > 1:
            return False
    return True

def cleaning() -> None:
    while not is_clean():
        to_remove = set()
        for val in opcodes.values():
            if len(val) == 1:
                to_remove.add(next(iter(val)))
        for val in opcodes.values():
            if len(val) > 1:
                for code in to_remove:
                    with suppress(KeyError):
                        val.remove(code)
    for key, val in opcodes.items():
        opcodes[key] = next(iter(val))

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        samples, test_program = file.read().split("\n\n\n\n")
        samples = [parse_input(raw) for raw in samples.split("\n\n")]
        test_program = [parse_program(raw) for raw in test_program.split("\n") if raw]
    if args.part == 1:
        print(sum(is_like_three_or_more(sample) for sample in samples))
    else:
        opcodes = {}
        for sample in samples:
            identify_opcodes(sample)
        cleaning()
        registers = {i: 0 for i in range(4)}
        for instruction in test_program:
            registers[instruction.c] = OPCODES[opcodes[instruction.opcode]](instruction.a, instruction.b, registers)
        print(registers[0])
    print(time() - t)
