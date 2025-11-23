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

def find_line(pattern: list) -> int:
    for i in range(1, len(pattern)):
        if pattern[i - 1] == pattern[i]:
            min_range = min(i - 1, len(pattern) - i - 1)
            for j in range(min_range + 1):
                if pattern[i - 1 - j] != pattern[i + j]:
                    break
            else:
                return i
            continue
    return 0

def find_line_2(pattern: list) -> int:
    for i in range(1, len(pattern)):
        diff = sum(x != y for x, y in zip(pattern[i - 1], pattern[i]))
        if diff <= 1:
            mismatch = bool(diff)
            min_range = min(i - 1, len(pattern) - i - 1)
            for j in range(min_range + 1):
                if pattern[i - 1 - j] != pattern[i + j]:
                    new_diff = sum(x != y for x, y in zip(pattern[i - 1 - j], pattern[i + j]))
                    if mismatch:
                        if j > 0:
                            break
                        else:
                            continue
                    elif new_diff == 1:
                        mismatch = True
                    else:
                        break
            else:
                if mismatch:
                    return i
            continue
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        idx = 0
        while line := file.readline():
            if line.strip():
                data[idx] = data.get(idx, []) + [line.strip()]
            else:
                idx += 1
    if args.part == 1:
        calculation = [
            100 * find_line(pattern) + find_line(list(zip(*pattern)))
            for pattern in data.values()
        ]
        print(sum(calculation))
    else:
        calculation = [
            100 * find_line_2(pattern) + find_line_2(["".join(item) for item in list(zip(*pattern))])
            for pattern in data.values()
        ]
        print(sum(calculation))
    print(time() - t)

