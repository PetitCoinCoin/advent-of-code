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

STATE_MAP = {
    "A": {
        "next_value": lambda x: (x + 1) % 2,
        "next_slot": lambda x, y: x + (-1 if y else 1),
        "next_state": lambda x: "C" if x else "B", 
    },
    "B": {
        "next_value": lambda _: 1,
        "next_slot": lambda x, _: x - 1,
        "next_state": lambda x: "D" if x else "A", 
    },
    "C": {
        "next_value": lambda x: (x + 1) % 2,
        "next_slot": lambda x, _: x + 1,
        "next_state": lambda x: "C" if x else "D", 
    },
    "D": {
        "next_value": lambda _: 0,
        "next_slot": lambda x, y: x + (1 if y else -1),
        "next_state": lambda x: "E" if x else "B", 
    },
    "E": {
        "next_value": lambda _: 1,
        "next_slot": lambda x, y: x + (-1 if y else 1),
        "next_state": lambda x: "F" if x else "C", 
    },
    "F": {
        "next_value": lambda _: 1,
        "next_slot": lambda x, y: x + (1 if y else -1),
        "next_state": lambda x: "A" if x else "E", 
    },
}

def parse_input(raw: str) -> tuple:
    settings = raw.split("\n\n")[0].split("\n")
    return int(settings[-1].split(" ")[-2]), settings[0][-2]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        STEPS, START = parse_input(file.read().strip())
    state = START
    tape = dict()
    i = 0
    cursor = 0
    while i < STEPS:
        value = tape.get(cursor, 0)
        tape[cursor] = STATE_MAP[state]["next_value"](value)
        cursor = STATE_MAP[state]["next_slot"](cursor, value)
        state = STATE_MAP[state]["next_state"](value)
        i += 1
    if args.part == 1:
        print(sum(tape.values()))
    else:
        print("all stars!")
