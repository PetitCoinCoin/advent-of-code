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
    action: str
    r_range: range
    c_range: range

ACTION_MAP_PART1 = {
    "on": lambda _ : 1,
    "off": lambda _ : -1,
    "toggle": lambda x : -x,
}

ACTION_MAP_PART2 = {
    "on": lambda x : x + 1,
    "off": lambda x : max(0, x - 1),
    "toggle": lambda x : x + 2,
}

def parse_instructions(raw: str) -> Instruction:
    groups = re.findall(r"([a-z]*)\s(\d{1,3},\d{1,3})", raw)
    action = groups[0][0]
    start_range = [int(x) for x in groups[0][1].split(",")]
    end_range = [int(x) for x in groups[1][1].split(",")]
    return Instruction(
        action=action,
        r_range=range(start_range[0], end_range[0] + 1),
        c_range=range(start_range[1], end_range[1] + 1),
    )

def build_grid(start_value: int) -> dict:
    grid = dict()
    for r in range(1000):
        for c in range(1000):
            grid[complex(r, c)] = start_value
    return grid

def follow_instructions(lights: dict, instructions: list, action_map: dict) -> None:
    for instruction in instructions:
        for r in instruction.r_range:
            for c in instruction.c_range:
                lights[complex(r, c)] = action_map[instruction.action](lights[complex(r, c)])

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_instructions(row) for row in file.read().split("\n")]
    if args.part == 1:
        lights = build_grid(-1)
        follow_instructions(lights, data, ACTION_MAP_PART1)
        print(sum([light for light in lights.values() if light == 1]))
    else:
        lights = build_grid(0)
        follow_instructions(lights, data, ACTION_MAP_PART2)
        print(sum(lights.values()))
