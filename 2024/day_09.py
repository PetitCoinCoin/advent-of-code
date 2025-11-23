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

def move(*, is_part_two: bool = False) -> tuple:
    res = []
    free_spaces = []
    files = []
    for i, char in enumerate(data):
        if not i % 2:
            if is_part_two:
                files.append((str(i // 2), len(res), int(char)))  # ID, idx, count
            for _ in range(int(char)):
                res.append(str(i // 2))
        else:
            if is_part_two:
                free_spaces.append((len(res), int(char)))  # idx, count
            res += list("." * int(char))
    return res, free_spaces, files

def rearrange_p1() -> list:
    raw, _, _ = move()
    i = 0
    j = len(raw) - 1
    while j > i:
        if raw[i] == ".":
            raw[i] = raw[j]
            j -= 1
            while raw[j] == ".":
                j -= 1
        i += 1
    return raw[:i + 1]

def rearrange_p2() -> list:
    raw, free_spaces, files = move(is_part_two=True)
    is_done = False
    while files and not is_done:
        file_id, file_idx, file_count = files.pop()
        for i, free_space in enumerate(free_spaces):
            free_idx, free_count = free_space
            if free_idx > file_idx:
                is_done = True
                break
            if free_count >= file_count:
                raw[free_idx: free_idx + file_count] = [file_id] * file_count
                raw[file_idx: file_idx + file_count] = ["."] * file_count
                free_spaces[i] = (free_idx + file_count, free_count - file_count)
                break
    return raw

def checksum(raw: list) -> int:
    return sum(i * int(char) for i, char in enumerate(raw) if char != ".")

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = list(file.read())
    if args.part == 1:
        print(checksum(rearrange_p1()))
    else:
        print(checksum(rearrange_p2()))
    print(time() - t)
