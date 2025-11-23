import argparse

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
        key, rule = tuple(line.split(": "))
        if rule.startswith('"'):
            result[int(key)] = rule[1]
        else:
            result[int(key)] = [
                [int(x) for x in sub_rule.split(" ")]
                for sub_rule in rule.split(" | ")
            ]
    return result

def get_full_rule(idx: int) -> set:
    if isinstance(rules[idx], str):
        return {rules[idx]}
    res = set()
    for rule in rules[idx]:
        sub = {""}
        for sub_rule in rule:
            new_sub = set()
            for chain in get_full_rule(sub_rule):
                for current in sub:
                    if len(current) + len(chain) <= max_length:
                        new_sub.add(current + chain)
            sub = new_sub
        res |= sub
    return res

def is_valid(item: str, rule: list) -> bool:
    """
        Used for part 1, wirth rule_0.
        Useless after refactor.
    """
    return item in rule

def validate_42_31(item: str, mul: int = 8, *, with_loop: bool = False) -> bool:
    """
        Rule 0 : n*42 m*42 m*31
        Possibilities in rules 42 and 31 all have length 8 in my input.
        But their length is 5 in example, so mul is here to ease debug.
    """
    if len(item) % mul or (len(item) < 3 * mul and with_loop) or (len(item) // mul != 3 and not with_loop):
        return False
    count_sub = len(item) // mul
    if with_loop:
        max_m = count_sub // 2 if count_sub % 2 else count_sub // 2 - 1
    else:
        max_m = 1
    for m in range(1, max_m + 1):
        n = count_sub - 2 * m if with_loop else 1
        for i in range(n):
            if item[i * mul: (i + 1) * mul] not in rule_42:
                break
        else:
            for i in range(m):
                if item[(n + i) * mul:(n + i + 1) * mul] not in rule_42:
                    break
                if item[-(i + 1) * mul:-i * mul if -i * mul else None] not in rule_31:
                    break
            else:
                return True
    return False

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        rules_input, data_input = tuple(file.read().strip().split("\n\n"))
    data = data_input.split("\n")
    max_length = max(len(item) for item in data)
    rules = parse_rules(rules_input)
    # Only rules 8, 11 and 0 are affected by the change for part 2
    # Rule 0 : 42 42 31 > n*42 m*42 m*31
    # In part 1, n = 1 and m = 1 only
    rule_42 = get_full_rule(42)
    rule_31 = get_full_rule(31)
    print(sum(validate_42_31(item, with_loop=args.part == 2) for item in data))
    print(time() - t)
