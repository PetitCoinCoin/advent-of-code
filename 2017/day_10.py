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

SIZE = 256

def hash_round(lengths: list, elements: list, current: int, skip: int) -> tuple[list, int, int]:
    for length in lengths:
        if length > SIZE:
            continue
        if length == 1:
            pass
        elif current + length < SIZE:
            sub = elements[current: current + length]
            elements = elements[:current] + sub[::-1] + elements[current + length:]
        else:
            sub = elements[current:] + elements[:(current + length) % SIZE]
            rev = sub[::-1]
            elements = rev[SIZE - current:] + elements[(current + length) % SIZE: current] + rev[:SIZE - current]
        current = (current + length + skip) % SIZE
        skip += 1
    return elements, current, skip

if __name__ == "__main__":
    args = _parse_args()
    if args.part == 1:
        with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
            data = [int(x.strip()) for x in file.read().split(",")]
        items, _, _ = hash_round(data, list(range(SIZE)), 0, 0)
        print(items[0] * items[1])
    else:
        with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
            data = [ord(x) for x in file.read()] + [17, 31, 73, 47, 23]
        items = list(range(SIZE))
        current = 0
        skip = 0
        for _ in range(64):
            items, current, skip = hash_round(data, items, current, skip)
        dense_hash = ""
        for i in range(16):
            xor = items[i * 16]
            for j in range(1, 16):
                xor ^= items[i * 16 + j]
            dense_hash += f"{xor:02x}"
        print(dense_hash, len(dense_hash))
