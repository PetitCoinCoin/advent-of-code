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

def exchange(l: str, indexes: tuple[int, int]) -> str:
    x, y = indexes
    if x == y:
        return l
    if x > y:
        return l[:y] + l[x] + l[y + 1:x] + l[y] + l[x + 1:]
    return l[:x] + l[y] + l[x + 1:y] + l[x] + l[y + 1:]

def partner(l: str, letters: tuple[str, str]) -> str:
    x, y = letters
    idx_x = l.index(x)
    idx_y = l.index(y)
    return exchange(l, (idx_x, idx_y))

START = "abcdefghijklmnop"
RANGE_SIZE = 10**6
ACTION_MAP = {
    "s": lambda l, t: l[-t[0]:] + l[:len(l) - t[0]],
    "x": exchange,
    "p": partner,
}

@dataclass
class Instruction:
    action: callable
    params: tuple

def parse_input(raw: str) -> Instruction:
    action = raw[0]
    if action == "s":
        return Instruction(action=ACTION_MAP[action], params=(int(raw[1:]),))
    if action == "x":
        return Instruction(action=ACTION_MAP[action], params=tuple(int(char) for char in raw[1:].split("/")))
    return Instruction(action=ACTION_MAP[action], params=tuple(raw[1:].split("/")))

def dance(instructions: list, start: str) -> str:
    prog = start
    for instruction in instructions:
        prog = instruction.action(prog, instruction.params)
    return prog

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(raw) for raw in file.read().split(",")]
    prog = START
    for i in range(RANGE_SIZE):
        prog = dance(data, prog)
        if args.part == 1 and not i:
            print(prog)
            break
        if prog == START:
            for _ in range(RANGE_SIZE % (i + 1)):
                prog = dance(data, prog)
            print(prog)
            break
