import argparse

from collections import Counter
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

DIR_MAPPING = {
    "n+": ("se+", "ne-"),
    "n-": ("se-", "ne+"),
    "ne+": ("se-", "n-"),
    "ne-": ("se+", "n+"),
    "se+": ("n+", "ne-"),
    "se-": ("n-", "ne+"),
}

def min_steps(steps: list) -> int:
    count = Counter(steps)
    remaining = dict()
    remaining["n"] = count["n"] - count["s"]
    remaining["ne"] = count["ne"] - count["sw"]
    remaining["se"] = count["se"] - count["nw"]
    max_dir = ""
    next_max_dir = ""
    impossible = []
    while not max_dir and len(impossible) < 3:
        for key, val in remaining.items():
            aug_key = key + ("+" if val >= 0 else "-")
            if abs(val) >= abs(remaining.get(max_dir[:-1], 0)) and aug_key not in impossible:
                max_dir = aug_key
        for key, val in remaining.items():
            aug_key = key + ("+" if val >= 0 else "-")
            if key != max_dir and abs(val) >= abs(remaining.get(next_max_dir[:-1], 0)) and aug_key in DIR_MAPPING[max_dir]:
                next_max_dir = aug_key
        if not next_max_dir:
            impossible.append(max_dir)
            max_dir = ""
    if not max_dir:
        return sum(abs(val) for val in remaining.values())
    if (max_dir == "n+" and next_max_dir == "se+") or \
        (max_dir == "n-" and next_max_dir == "se-") or \
        (max_dir == "ne+" and next_max_dir == "se-") or \
        (max_dir == "ne-" and next_max_dir == "se+"):
        return abs(remaining["n"]) + abs(remaining["ne"])
    if (max_dir == "n+" and next_max_dir == "ne-") or \
        (max_dir == "n-" and next_max_dir == "ne+") or \
        (max_dir == "se+" and next_max_dir == "ne-") or \
        (max_dir == "se-" and next_max_dir == "ne+"):
        return abs(remaining["n"] + remaining["ne"]) + abs(remaining["se"] + remaining["ne"])
    if (max_dir == "ne+" and next_max_dir == "n-") or \
        (max_dir == "ne-" and next_max_dir == "n+") or \
        (max_dir == "se+" and next_max_dir == "n+") or \
        (max_dir == "se-" and next_max_dir == "n-"):
        return abs(remaining["se"]) + abs(remaining["ne"])

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [x.strip() for x in file.read().split(",")]
    end_steps = min_steps(data)
    if args.part == 1:
        print(end_steps)
    else:
        max_steps = 0
        for s in range(end_steps, len(data)):
            steps = min_steps(data[:s])
            if steps > max_steps:
                max_steps = steps
        print(max_steps)
