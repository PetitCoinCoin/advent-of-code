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

def evenly_divided(row: list) -> int:
    for i in range(len(row) - 1):
        for j in range(i + 1, len(row)):
            if min(row[i], row[j]) and not max(row[i], row[j]) % min(row[i], row[j]):
                return max(row[i], row[j]) // min(row[i], row[j])
    print("WTF")
    return 0

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [[int(x.strip()) for x in raw.split("\t") if x != ""] for raw in file.read().split("\n")]
    if args.part == 1:
        print(sum(max(row) - min(row) for row in data))
    else:
        print(sum(evenly_divided(row) for row in data))
