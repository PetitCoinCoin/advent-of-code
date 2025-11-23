import argparse
import re

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

PAPER_GIFT = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

def find_sue(raw: str, retro: bool = False) -> int:
    for key in PAPER_GIFT.keys():
        pattern = key + r": (\d+).*"
        matched = re.search(pattern, raw)
        if matched is not None:
            if (not retro and int(matched.group(1)) != PAPER_GIFT[key]) or \
                (retro and key not in ("cats", "trees", "pomeranians", "goldfish") and int(matched.group(1)) != PAPER_GIFT[key]) or \
                (retro and key in ("cats", "trees") and int(matched.group(1)) <= PAPER_GIFT[key]) or \
                (retro and key in ("pomeranians", "goldfish") and int(matched.group(1)) >= PAPER_GIFT[key]):
                return 0
    return int(re.search(r"Sue (\d+).*", raw).group(1))
    
if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    if args.part == 1:
        sues = [find_sue(row) for row in data]
    else:
        sues = [find_sue(row, True) for row in data]
    print([sue for sue in sues if sue][0])
