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

NUMBERS_MAP = {
    complex(-1, 1): 1,
    complex(0, 1): 2,
    complex(1, 1): 3,
    complex(-1, 0): 4,
    complex(0, 0): 5,
    complex(1, 0): 6,
    complex(-1, -1): 7,
    complex(0, -1): 8,
    complex(1, -1): 9,
}

FANCY_NUMBERS_MAP = {
    complex(0, 2): 1,
    complex(-1, 1): 2,
    complex(0, 1): 3,
    complex(1, 1): 4,
    complex(-2, 0): 5,
    complex(-1, 0): 6,
    complex(0, 0): 7,
    complex(1, 0): 8,
    complex(2, 0): 9,
    complex(-1, -1): "A",
    complex(0, -1): "B",
    complex(1, -1): "C",
    complex(0, -2): "D",
}

CODE_MAP = {
    "U": lambda c: c + 1j if c.imag in (-1.0, 0.0) else c,
    "R": lambda c: c + 1 if c.real in (-1.0, 0.0) else c,
    "D": lambda c: c - 1j if c.imag in (1.0, 0.0) else c,
    "L": lambda c: c - 1 if c.real in (1.0, 0.0) else c,
}

FANCY_CODE_MAP = {
    "U": lambda c: c + 1j if abs((c + 1j).imag) + abs(c.real) < 3 else c,
    "R": lambda c: c + 1 if abs(c.imag) + abs((c + 1).real) < 3 else c,
    "D": lambda c: c - 1j if abs((c - 1j).imag) + abs(c.real) < 3 else c,
    "L": lambda c: c - 1 if abs(c.imag) + abs((c - 1).real) < 3 else c,
}

def get_number(instruction: str, start: complex, code_map: dict) -> complex:
    result = start
    for code in instruction:
        result = code_map[code](result)
    return result

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    numbers = []
    if args.part == 1:
        start = complex(0, 0)
        keypad = NUMBERS_MAP
        code_map = CODE_MAP
    else:
        start = complex(-2, 0)
        keypad = FANCY_NUMBERS_MAP
        code_map = FANCY_CODE_MAP
    for instruction in data:
        start = get_number(instruction, start, code_map)
        numbers.append(str(keypad[start]))
    print("".join(numbers))
