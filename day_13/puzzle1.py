from pathlib import Path

def find_line(pattern: list) -> int:
    for i in range(1, len(pattern)):
        if pattern[i - 1] == pattern[i]:
            min_range = min(i - 1, len(pattern) - i - 1)
            for j in range(min_range + 1):
                if pattern[i - 1 - j] != pattern[i + j]:
                    break
            else:
                return i
            continue
    return 0

if __name__ == "__main__":
    with Path("day_13/input.txt").open("r") as file:
        data = {}
        idx = 0
        while line := file.readline():
            if line.strip():
                data[idx] = data.get(idx, []) + [line.strip()]
            else:
                idx += 1
    calculation = [
        100 * find_line(pattern) + find_line(list(zip(*pattern)))
        for pattern in data.values()
    ]
    print(sum(calculation))
