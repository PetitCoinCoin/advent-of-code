from fractions import Fraction
from time import time

class Solver:
    """
    self.Aim to solve self.AX = B.
    - self.A is an m * n matrix
    - X is a n * 1 matrix representing the unknowns
    - B is an m * 1 matrix representing the right parts of the m equations
    """

    def __init__(self) -> None:
        self.A = []
        self.B = []
        self.equations = 0
        self.unknowns = 0

    def add_equation(self, coefficients: list[int], result: int) -> None:
        if self.unknowns and len(coefficients) != self.unknowns:
            raise ValueError(f"There are currently {self.unknowns}, but {len(coefficients)} parameters were provided")
        self.A.append(coefficients)
        self.B.append(result)
        self.equations += 1
        self.unknowns = self.unknowns or len(coefficients)

    def solve_exactly(self, *, int_only: bool = True) -> list:
        if self.equations < self.unknowns:
            raise TypeError("There are less equations than unknowns, use another method to solve")
        self.__gaussian_elimination()
        solutions = [None] * self.unknowns
        for r in range(self.equations - 1, -1, -1):
            solutions[r] = (self.B[r] - sum(a * b for a,b in zip(self.A[r][r + 1:], solutions[r + 1:]))) / self.A[r][r]
        if not int_only:
            return solutions
        if any(not x.is_integer() for x in solutions):
            print("Some values aren't int")
            return []
        return [int(x) for x in solutions]

    def __gaussian_elimination(self) -> None:
        pivot_row = 0
        pivot_col = 0
        while pivot_row < self.equations and pivot_col < self.unknowns:
            # Find pivot
            max_abs = max(abs(self.A[r][pivot_col]) for r in range(pivot_row, self.equations))
            r_max = min(r for r in range(pivot_row, self.equations) if abs(self.A[r][pivot_col]) == max_abs)
            if not self.A[r_max][pivot_col]:  # No pivot here, move on
                pivot_col += 1
                continue
            # Swap rows
            self.A[pivot_row], self.A[r_max] = self.A[r_max], self.A[pivot_row]
            self.B[pivot_row], self.B[r_max] = self.B[r_max], self.B[pivot_row]
        
            for r in range(pivot_row + 1, self.equations):
                factor = Fraction(self.A[r][pivot_col], self.A[pivot_row][pivot_col])
                for c in range(pivot_col, self.unknowns):
                    self.A[r][c] -= self.A[pivot_row][c] * factor
                self.B[r] -= self.B[pivot_row] * factor
            pivot_row += 1
            pivot_col += 1

if __name__ == "__main__":
    t = time()
    solv = Solver()
    solv.add_equation([2, 1, -1], 8)
    solv.add_equation([-3, -1, 2], -11)
    solv.add_equation([-2, 1, 2], -3)
    print(solv.solve_exactly())
    print(time() - t)
