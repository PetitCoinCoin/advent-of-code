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

def combo(value: int) -> int:
    if value < 4:
        return value
    if value == 4:
        return data["A"]
    if value == 5:
        return data["B"]
    if value == 6:
        return data["C"]
    raise ValueError

def debug() -> list:
    logs = []
    i = 0
    if len(program) % 2:
        print("wtf")
    while i < len(program):
        match program[i]:
            case 0:
                data["A"] = data["A"] // (2 ** combo(program[i + 1]))
            case 1:
                data["B"] = data["B"] ^ program[i + 1]
            case 2:
                data["B"] = combo(program[i + 1]) % 8
            case 3:
                if data["A"]:
                    i = program[i + 1]
                    continue
            case 4:
                data["B"] = data["B"] ^ data["C"]
            case 5:
                logs.append(combo(program[i + 1]) % 8)
            case 6:
                data["B"] = data["A"] // (2 ** combo(program[i + 1]))
            case 7:
                data["C"] = data["A"] // (2 ** combo(program[i + 1]))
            case _:
                continue
        i += 2
    return logs

def reverse_eng() -> int:
    prev = {0}
    for value in program[::-1]:
        new_prev = set()
        for prev_a in prev:
            for last in range(0, 8):
                if not prev_a and not last:
                    continue
                a = prev_a * 8 + last
                b = a % 8
                b = b ^ 2
                c = a // (2 ** b)
                b = b ^ 7
                b = b ^ c
                if b % 8 == value:
                    new_prev.add(a)
        if not new_prev:
            print("oh no")
            break
        prev = new_prev
    return min(prev)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line:= file.readline():
            if line.startswith("Register A:"):
                data["A"] = int(line.split(":")[-1])
            elif line.startswith("Register B:"):
                data["B"] = int(line.split(":")[-1])
            elif line.startswith("Register C:"):
                data["C"] = int(line.split(":")[-1])
            elif line.startswith("Program:"):
                program = [int(x) for x in line.split(":")[-1].split(",")]
    if args.part == 1:
        print(",".join([str(x) for x in debug()]))
    else:
        print(reverse_eng())
    print(time() - t)
