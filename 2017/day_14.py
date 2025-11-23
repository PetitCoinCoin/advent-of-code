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

HASH_SIZE = 256
GRID_SIZE = 128

# From day 10
def hash_round(lengths: list, elements: list, current: int, skip: int) -> tuple[list, int, int]:
    for length in lengths:
        if length > HASH_SIZE:
            continue
        if length == 1:
            pass
        elif current + length < HASH_SIZE:
            sub = elements[current: current + length]
            elements = elements[:current] + sub[::-1] + elements[current + length:]
        else:
            sub = elements[current:] + elements[:(current + length) % HASH_SIZE]
            rev = sub[::-1]
            elements = rev[HASH_SIZE - current:] + elements[(current + length) % HASH_SIZE: current] + rev[:HASH_SIZE - current]
        current = (current + length + skip) % HASH_SIZE
        skip += 1
    return elements, current, skip

# From day 10
def knot_hash(keys: list) -> str:
    items = list(range(HASH_SIZE))
    current = 0
    skip = 0
    for _ in range(64):
        items, current, skip = hash_round(keys, items, current, skip)
    dense_hash = ""
    for i in range(16):
        xor = items[i * 16]
        for j in range(1, 16):
            xor ^= items[i * 16 + j]
        dense_hash += f"{xor:02x}"
    return dense_hash

# From stack overflow XD
def hextobin(h: str) -> str:
  return bin(int(h, 16))[2:].zfill(len(h) * 4)

def format_data(grid: list) -> dict:
    spaces = dict()
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c]:
                spaces[(r, c)] = [(r, c)]
                for d in (-1, 1):
                    if 0 <= r + d < GRID_SIZE and grid[r + d][c]:
                        spaces[(r, c)].append((r + d, c))
                    if 0 <= c + d < GRID_SIZE and grid[r][c + d]:
                        spaces[(r, c)].append((r, c + d))
    return spaces

# From day 12
def get_regions(linked: dict, start: tuple) -> list:
    seen = dict()
    regions = []
    queue = [start]
    while queue:
        space = queue.pop(0)
        for s in linked[space]:
            if seen.get(s):
                continue
            regions.append(s)
            queue.append(s)
            seen[s] = True
    return regions

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        INPUT = file.read().strip()
    data = []
    for i in range(GRID_SIZE):
        row_data = [ord(x) for x in f"{INPUT}-{i}"] + [17, 31, 73, 47, 23]
        data.append([int(x) for x in hextobin(knot_hash(row_data))])
    if args.part == 1:
        print(sum(sum(row) for row in data))
    else:
        # From day 12
        formatted_data = format_data(data)
        count = 0
        while formatted_data:
            for key in formatted_data.keys():
                start = key
                break
            region = get_regions(formatted_data, start)
            count += 1
            for key in region:
                del formatted_data[key]
        print(count)
