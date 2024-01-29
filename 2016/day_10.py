import argparse
import re

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
    min_chip: int
    min_output: bool
    max_chip: int
    max_output: bool

def parse_bot(raw: str) -> tuple:
    return tuple([int(x) for x in re.findall(r"\d+", raw)])

def parse_instruction(raw: str) -> tuple:
    digits = [int(x) for x in re.findall(r"\d+", raw)]
    outputs = re.findall(r"low to (\w+).*high to (\w+)", raw)[0]
    return digits[0], Instruction(
        min_chip=digits[1],
        min_output=outputs[0]=="output",
        max_chip=digits[2],
        max_output=outputs[1]=="output",
    )

def process(bots: dict, instructions: dict, part_one: bool = True) -> int:
    MIN_CHIP = 17
    MAX_CHIP = 61
    outputs = dict()
    queue = [k for k, v in bots.items() if len(v) == 2]
    while queue:
        bot = queue.pop(0)
        bots[bot].sort()
        if part_one and bots[bot] == [MIN_CHIP, MAX_CHIP]:
            return bot
        min_chip, max_chip = tuple(bots[bot])
        instruction = instructions[bot]
        if not instruction.min_output:
            bots[instruction.min_chip].append(min_chip)
            if len(bots[instruction.min_chip]) == 2:
                queue.append(instruction.min_chip)
        else:
            outputs[instruction.min_chip] = min_chip
        if not instruction.max_output:
            bots[instruction.max_chip].append(max_chip)
            if len(bots[instruction.max_chip]) == 2:
                queue.append(instruction.max_chip)
        else:
            outputs[instruction.max_chip] = max_chip
        bots[bot] = []
    print(outputs)
    return outputs[0] * outputs[1] * outputs[2]

if __name__ == "__main__":
    args = _parse_args()
    bots = dict()
    instructions = dict()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            if line.startswith("value"):
                value, bot = parse_bot(line)
                bots[bot] = bots.get(bot, []) + [value]
            else:
                bot, instruction = parse_instruction(line)
                instructions[bot] = instruction
    for bot in instructions.keys():
        if not bots.get(bot):
            bots[bot] = []
    if args.part == 1:
        print(process(bots, instructions))
    else:
        print(process(bots, instructions, False))
