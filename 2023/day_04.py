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

def calculate_points(card: str) -> int:
    without_id = card.split(":")[-1]
    winning = [
        x.strip()
        for x in without_id.split(" | ")[0].strip().split(" ")
        if x != ""
    ]
    played_and_win = [
        x.strip()
        for x in without_id.split(" | ")[1].strip().split(" ")
        if x != "" and x in winning
    ]
    if played_and_win:
        return 2 ** (len(played_and_win) - 1)
    else:
        return 0

def clean_data(card: str) -> int:
    """Returns count of winning numbers per card."""

    without_id = card.split(":")[-1]
    winning = [
        x.strip()
        for x in without_id.split(" | ")[0].strip().split(" ")
        if x != ""
    ]
    played_and_win = [
        x.strip()
        for x in without_id.split(" | ")[1].strip().split(" ")
        if x != "" and x in winning
    ]
    return len(played_and_win)

def count_copies(sub_data: list) -> int:
    count = sub_data.pop(0)
    if count > 0:
        total = 0
        for i in range(count):
            total += 1 + count_copies(sub_data[i:])
        return total
    else:
        return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    if args.part == 1:
        print(sum([
            calculate_points(card)
            for card in data
        ]))
    else:
        cleaned_data = [clean_data(card) for card in data]
        total = 0
        for i in range(len(cleaned_data)):
            total += 1 + count_copies(cleaned_data[i:])
        print(total)
    print(time() - t)

