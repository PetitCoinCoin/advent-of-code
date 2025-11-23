import argparse
import math
import re

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

def parse_rules(raw: str) -> dict:
    result = {}
    for line in raw.split("\n"):
        key, values = tuple(line.split(":"))
        matches = [int(x) for x in re.findall(r"(\d+)", values)]
        result[key] = set(range(matches[0], matches[1] + 1)) | set(range(matches[2], matches[3] + 1))
    return result

def is_invalid(ticket: list) -> int:
    """Assuming only one wrong value per ticket > seems like a correct assumption!"""
    for value in ticket:
        for rule in rules.values():
            if value in rule:
                break
        else:
            return value
    return 0

def get_mapping() -> dict:
    valid_tickets = [ticket for ticket in nearby_tickets if not is_invalid(ticket)]
    mapping = {}
    for i in range(len(my_ticket)):
        all_values = {ticket[i] for ticket in valid_tickets}
        mapping[i] = set()
        for key, val in rules.items():
            if all_values.intersection(val) == all_values:
                mapping[i].add(key)
    to_remove = {next(iter(rule)) for rule in mapping.values() if len(rule) == 1}
    while len(to_remove) != len(mapping.keys()):
        for key, rule in mapping.items():
            if len(rule) > 1:
                mapping[key] = rule - to_remove
                if len(mapping[key]) == 1:
                    to_remove |= mapping[key]
    return mapping

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        input_rules, input_my, input_nearby = tuple(file.read().strip().split("\n\n"))
    rules = parse_rules(input_rules)
    my_ticket = [int(x) for x in input_my.split("\n")[-1].split(",")]
    nearby_tickets = [[int(x) for x in row.split(",")] for row in input_nearby.split("\n")[1:]]
    if args.part == 1:
        print(sum(is_invalid(ticket) for ticket in nearby_tickets))
    else:
        mapping = get_mapping()
        print(math.prod(
            my_ticket[i]
            for i, rule in mapping.items()
            if rule.pop().startswith("departure")
        ))
    print(time() - t)
