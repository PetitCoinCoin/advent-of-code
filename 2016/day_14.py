import argparse

from collections import deque
from hashlib import md5
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

SALT = "qzyelonm"

def contains_multiple(raw: str, count: int, char: str = "") -> str:
    if char:
        if char * count in raw:
            return char
        return ""
    for i in range(len(raw) - count + 1):
        for c in range(1, count):
            if raw[i + c] != raw[i]:
                break
        else:
            return raw[i]
        continue
    return ""

def salt_encode(idx: int, part_one: bool) -> str:
    processed = md5(f"{SALT}{idx}".encode()).hexdigest()
    if part_one:
        return processed
    i = 0
    while i < 2016:
        processed = md5(processed.encode()).hexdigest()
        i += 1
    return processed

def get_index( part_one: bool) -> int:
    key_indexes = []
    hashes = deque([salt_encode(i, part_one) for i in range(1001)])
    i = 0
    while len(key_indexes) < 64:
        processed = hashes.popleft()
        char = contains_multiple(processed, 3)
        if char:
            for h in hashes:
                if contains_multiple(h, 5, char):
                    key_indexes.append(i)
                    break
        i += 1
        hashes.append(salt_encode(i + 1000, part_one))
    return key_indexes[-1]

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        SALT = file.read().strip()
    print(get_index(args.part == 1))
