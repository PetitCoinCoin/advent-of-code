from pathlib import Path

def energize(start: tuple, direction: str, records: dict, floor: list) -> None:
    if direction in records.get(start, []):
        return None
    records[start] = records.get(start, []) + [direction]
    i, j = start
    if direction == "right":
        if j == len(floor[i]) - 1:
            return None
        k = 1
        while j + k < len(floor[i]) and floor[i][j + k] in (".", "-"):
            records[(i, j + k)] = records.get((i, j + k), []) + [direction]
            k += 1
        if j + k == len(floor[i]):
            return None
        if floor[i][j + k] in "|/":
            energize((i, j + k), "up", records, floor)
        if floor[i][j + k] in "|\\":
            energize((i, j + k), "down", records, floor)
    elif direction == "left":
        if j == 0:
            return None
        k = 1
        while j - k >= 0 and floor[i][j - k] in (".", "-"):
            records[(i, j - k)] = records.get((i, j - k), []) + [direction]
            k += 1
        if j - k < 0:
            return None
        if floor[i][j - k] in "|\\":
            energize((i, j - k), "up", records, floor)
        if floor[i][j - k] in "|/":
            energize((i, j - k), "down", records, floor)
    elif direction == "up":
        if i == 0:
            return None
        k = 1
        while i - k >= 0 and floor[i - k][j] in (".", "|"):
            records[(i - k, j)] = records.get((i - k, j), []) + [direction]
            k += 1
        if i - k < 0:
            return None
        if floor[i - k][j] in "-\\":
            energize((i - k, j), "left", records, floor)
        if floor[i - k][j] in "-/":
            energize((i - k, j), "right", records, floor)
    else:  # down
        if i == len(floor) - 1:
            return None
        k = 1
        while i + k < len(floor) and floor[i + k][j] in (".", "|"):
            records[(i + k, j)] = records.get((i + k, j), []) + [direction]
            k += 1
        if i + k == len(floor):
            return None
        if floor[i + k][j] in "-\\":
            energize((i + k, j), "right", records, floor)
        if floor[i + k][j] in "-/":
            energize((i + k, j), "left", records, floor)

if __name__ == "__main__":
    with Path("day_16/input.txt").open("r") as file:
        data = file.read().split()
    energized = {}
    energize((0, 0), "down", energized, data)
    print(len(energized.keys()))
