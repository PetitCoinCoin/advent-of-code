import argparse

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

def fill_diagonal(code: int, row: int, col: int) -> int:
    """
    Element in position r, c is the nth element, with n given by:
    n = 1 + r * (r - 1) - sum(i, i from 1 to r - 1) + (c - 1) * (r + c - 1) - sum(i, i from 0 to c - 2)
    """
    n = 1 + row * (row - 1) - sum(range(1, row)) + (col - 1) * (row + col - 1) - sum(range(0, col - 1))
    i = 1
    while i < n:
        code = (code * 252533) % 33554393
        i += 1
    return code

if __name__ == "__main__":
    args = _parse_args()
    if args.part == 1:
        print(fill_diagonal(20151125, 2947, 3029))
    else:
        raise NotImplementedError
