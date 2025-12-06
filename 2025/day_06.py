import operator

from itertools import accumulate
from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def parse_input(lines: list) -> list:
    splitted = [[x for x in line.split(" ")] for line in lines]
    splitted = [[[" "] if not x else [char for char in x] for x in line] for line in splitted]
    splitted = [[char for x in line for char in x] for line in splitted]
    result = []
    for i, op in enumerate(splitted[-1]):
        if op != " ":
            result.append([line[i] for line in splitted])
        else:
            result[-1] = [a + b for a,b in zip(result[-1], [line[i] for line in splitted])]
    return result

def solve_problem(prob: list) -> int:
    acc = accumulate(prob[:-1], operator.add if prob[-1] == "+" else operator.mul)
    return list(acc)[-1]

def transform(prob: list) -> list:
    return [
        "".join(line[i] for line in prob[:-1])
        for i in range(len(prob[-1]) - 1, -1, -1)
    ] + [prob[-1]]

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().split("\n"))
    if args.part == 2:
        data = [transform(problem) for problem in data]
    data = [[int(x) if x.strip().isdigit() else x.strip() for x in line] for line in data]
    print(sum(
        solve_problem(problem)
        for problem in data
    ))
    print(time() - t)
