import argparse

from heapq import heappop, heappush
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

MAX_IP = 4294967295

if __name__ == "__main__":
    args = _parse_args()
    min_range = []
    max_range = []
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        idx = 0
        while line := file.readline():
            heappush(min_range, (int(line.split("-")[0]), idx))
            max_range.append(int(line.split("-")[1]))
            idx += 1
    allowed = 0
    mini = 0
    min_ip, idx = heappop(min_range)
    while min_range:
        while min_ip <= mini and min_range:
            mini = max(mini, max_range[idx] + 1)
            min_ip, idx = heappop(min_range)
        if args.part == 1 and not allowed:
            print(mini)
            break
        if min_ip > mini:
            allowed += min_ip - mini
            mini = max_range[idx] + 1
        else:
            # End of avaiable ranges
            allowed += MAX_IP - max(mini, max_range[idx] + 1) + 1
    if args.part == 2:
        print(allowed)
