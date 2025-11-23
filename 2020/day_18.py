import argparse
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

OP_MAP = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
}

def evaluate(expr: list) -> int:
    result = int(expr[0])
    for i in range(1, len(expr), 2):
        result = OP_MAP[expr[i]](result, int(expr[i + 1]))
    return result

def evaluate_advanced(expr: list) -> int:
    while "+" in expr:
        add_idx = expr.index("+")
        expr = expr[:add_idx - 1] + [int(expr[add_idx - 1]) + int(expr[add_idx + 1])] + expr[add_idx + 2:]
    return evaluate(expr)


def linear_evaluation(expr: str, *, is_advanced: bool) -> int:
    evaluate_sub = evaluate_advanced if is_advanced else evaluate
    expr = expr.replace(" ", "")
    char_list = []
    sub_indexes = {}
    for i, char in enumerate(expr):
        if char.isdigit() or char in "+*":
            if sub_indexes:
                sub_indexes[max(sub_indexes.keys())].append(char)
            else:
                char_list.append(char)
        elif char == "(":
            sub_indexes[i] = []
        elif char ==")":
            last_sub = sub_indexes.pop(max(sub_indexes.keys()))
            if sub_indexes:
                sub_indexes[max(sub_indexes.keys())].append(evaluate_sub(last_sub))
            else:
                char_list.append(evaluate_sub(last_sub))
        else:
            print("WTF", char)
            raise ValueError
    return evaluate_sub(char_list)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    print(sum(linear_evaluation(expr, is_advanced=args.part == 2) for expr in data))
    print(time() - t)
