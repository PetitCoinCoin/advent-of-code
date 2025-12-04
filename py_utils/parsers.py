import argparse

def parse_args() -> argparse.Namespace:
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

def parse_grid_of_int(lines: list[str]) -> tuple:
    grid = {}
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            grid[(r, c)] = int(val)
            max_c = c
        max_r = r
    return grid, max_r + 1, max_c + 1

def parse_grid_of_char(lines: list[str], keep_only: str = "", *, as_set: bool = False) -> tuple:
    grid = set() if as_set else {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if not keep_only or char in keep_only:
                if as_set:
                    grid.add((r, c))
                else:
                    grid[(r, c)] = char
            max_c = c
        max_r = r
    return grid, max_r + 1, max_c + 1
