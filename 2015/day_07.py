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
class Wire:
    operation: str
    entries: list

OPERATION_MAP = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "LSHIFT": lambda x, y: x << y,
    "RSHIFT": lambda x, y: x >> y,
    "NOT": lambda x: x ^ 65535,  # 0xffff = 1111 1111 1111 1111
    "IDENTITY": lambda x: x,
}

def parse_input(raw: str, data: dict) -> None:
    groups = [
        item
        for item in re.findall(r"(\w+)\s?(AND|OR|LSHIFT|RSHIFT|NOT)?\s?(\w*)\s->\s(.+)", raw)[0]
        if item
    ]
    wire = groups[-1]
    if len(groups) == 4:
        operation = groups[1]
        entries = [int(item) if item.isdigit() else item for item in (groups[0], groups[2])]
    elif len(groups) == 3:
        operation = "NOT"
        entries = [int(groups[1]) if groups[1].isdigit() else groups[1]]
    else:
        operation = "IDENTITY"
        entries = [int(groups[0]) if groups[0].isdigit() else groups[0]]
    data[wire] = Wire(operation=operation, entries=entries)

def propagate(data: dict, wire: str, seen: dict) -> int:
    if data.get(wire) is None:
        seen[wire] = wire
        return wire
    action = data[wire]
    processed_entries = []
    for entry in action.entries:
        if seen.get(entry) is None:
            processed = propagate(data, entry, seen)
            seen[entry] = processed
        processed_entries.append(seen[entry])
    return OPERATION_MAP[action.operation](*processed_entries)

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = dict()
        while line := file.readline():
            parse_input(line.strip(), data)
    if args.part == 1:
        print(propagate(data, "a", dict()))
    else:
        b_override = propagate(data, "a", dict())
        data["b"].entries = [b_override]
        print(propagate(data, "a", dict()))
