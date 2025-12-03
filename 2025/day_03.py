from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def largest_joltage(bank: str, length: int) -> str:
    if not length:
        return ""

    index_max = max(range(len(bank) - length + 1), key=bank.__getitem__)
    return bank[index_max] + largest_joltage(bank[index_max + 1:], length - 1)

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    print(sum(
        int(largest_joltage(bank, 2 if args.part == 1 else 12))
        for bank in data
    ))
    print(time() - t)
