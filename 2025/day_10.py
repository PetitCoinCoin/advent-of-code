import re

from fractions import Fraction
from itertools import product
from pathlib import Path
from time import time
from typing import Iterable

from py_utils.parsers import parse_args

class Machine:
    OP = {
        ".": "#",
        "#": ".",
    }

    def __init__(self, line:str) -> None:
        pattern = r"(\[.+\]) (\(.+\))+ ({.+})"
        parts = re.findall(pattern, line)[0]
        self.lights = parts[0][1:-1]
        self.wirings = {
            tuple([int(x) for x in wiring[1:-1].split(",")])
            for wiring in parts[1].split()
        }
        self.joltage = [int(x) for x in parts[2][1:-1].split(",")]

    def configure_light(self) -> int:
        light = "." * len(self.lights)
        pressed = 0
        configurations = {light}
        while configurations:
            next_config = set()
            for config in configurations:
                if config == self.lights:
                    return pressed
                for wiring in self.wirings:
                    next_config.add("".join(self.OP[ch] if i in wiring else ch for i, ch in enumerate(config)))
            configurations = next_config
            pressed += 1
        return 0

    def configure_joltage(self) -> int:
        # Use matrix to get solution of system of {self.joltage} equations, with {self.wirings} unknowns
        eq = len(self.joltage)
        unknowns = len(self.wirings)
        max_joltage = max(self.joltage)
        init_joltage_sum = sum(self.joltage)
        A = [
            [1 if idx in wire else 0 for wire in self.wirings]
            for idx in range(eq)
        ]
    
        pivot_row = 0
        pivot_col = 0
        while pivot_row < eq and pivot_col < unknowns:
            # Find pivot
            max_abs = max(abs(A[r][pivot_col]) for r in range(pivot_row, eq))
            r_max = min(r for r in range(pivot_row, eq) if abs(A[r][pivot_col]) == max_abs)
            if not A[r_max][pivot_col]:  # No pivot here, move on
                pivot_col += 1
                continue
            # Swap rows
            A[pivot_row], A[r_max] = A[r_max], A[pivot_row]
            self.joltage[pivot_row], self.joltage[r_max] = self.joltage[r_max], self.joltage[pivot_row]
        
            for r in range(pivot_row + 1, eq):
                factor = Fraction(A[r][pivot_col], A[pivot_row][pivot_col])
                for c in range(pivot_col, unknowns):
                    A[r][c] -= A[pivot_row][c] * factor
                self.joltage[r] -= self.joltage[pivot_row] * factor
            pivot_row += 1
            pivot_col += 1

        while not(len([x for x in A[-1] if x])):
            if self.joltage[-1]:
                raise RuntimeError("WTF")
            A = A[:-1]
            self.joltage = self.joltage[:-1]
            eq -= 1

        if eq == unknowns:
            solutions = [None] * unknowns
            for r in range(eq - 1, -1, -1):
                solutions[r] = (self.joltage[r] - sum(a * b for a,b in zip(A[r][r + 1:], solutions[r + 1:]))) // A[r][r]
        else:
            solutions = [[None] * unknowns]
            handled = []
            for c in range(unknowns):
                h = len(handled)
                if c - h >= eq or not A[c - h][c]:
                    new_solutions = []
                    for solution in solutions:
                        for value in range(max_joltage + 1):
                            new_solutions.append([x if i != c else value for i,x in enumerate(solution)])
                    solutions = new_solutions
                    handled.append(c)
            for s, solution in enumerate(solutions):
                s_handled = [x for x in handled]
                for r in range(eq - 1, -1, -1):
                    if sum(x for x in solution if x is not None) > init_joltage_sum:
                        solutions[s] = None
                        break
                    while s_handled and s_handled[-1] >= r + len(s_handled):
                        s_handled = s_handled[:-1]
                    h = len(s_handled)
                    value = (self.joltage[r] - sum(a * b for a,b in zip(A[r][h + r + 1:], solution[h + r + 1:]))) / A[r][h + r]
                    if value < 0 or int(value) != value:
                        solutions[s] = None
                        break
                    solution[h + r] = int(value)
            return min(sum(solution) for solution in solutions if solution)
        return sum(solutions)

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [Machine(line) for line in file.read().strip().split("\n")]
    if args.part == 1:
        print(sum(
            machine.configure_light()
            for machine in data
        ))
    else:
        print(sum(
            machine.configure_joltage()
            for machine in data
        ))
    print(time() - t)
