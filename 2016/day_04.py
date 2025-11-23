import argparse

from collections import Counter
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

ALPHA = "abcdefghijklmnopqrstuvwxyz"

def is_decoy(raw: str) -> tuple:
    name = " ".join(raw.split("-")[:-1])
    room_id = int(raw.split("-")[-1].split("[")[0])
    checksum = raw.split("[")[-1][:-1]
    count = Counter(name)
    c = []
    for key, val in count.items():
        if key != " ":
            heappush(c, (-val, key))
    for char in checksum:
        if heappop(c)[1] != char:
            return 0, ""
    return room_id, name

def decrypt(room: tuple) -> tuple:
    count, raw = room
    name = ""
    for char in raw:
        if char == " ":
            name += " "
        else:
            name += ALPHA[(ALPHA.index(char) + count) % 26]
    return name, count

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    real_rooms = [is_decoy(row) for row in data]
    if args.part == 1:
        print(sum([room[0] for room in real_rooms]))
    else:
        real_rooms = [decrypt(room) for room in real_rooms if room[0]]
        print([room for room in real_rooms if "object" in room[0]])
