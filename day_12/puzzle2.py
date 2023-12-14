from functools import cache
from pathlib import Path

@cache
def get_arrangements(springs: str, operationals: tuple) -> int:
    if not operationals:
        return 1 if "#" not in springs else 0
    current, operationals = operationals[0], operationals[1:]
    min_length = current + sum(operationals) + len(operationals) - 1
    delta = len(springs) - min_length
    result = 0
    for i in range(delta):
        if "#" in springs[:i]:
            break
        next_i = i + current
        if next_i <= len(springs) and "." not in springs[i:next_i] and springs[next_i:next_i + 1] != "#":
            result += get_arrangements(springs[next_i + 1:], operationals)
    return result

if __name__ == "__main__":
    with Path("day_12/input.txt").open("r") as file:
        data = file.read().split()
    arrangements = [
        get_arrangements(
            "?".join(5 * [data[i]]),
            5 * tuple(int(x) for x in data[i + 1].split(","))
        )
        for i in range(0, len(data), 2)
    ]
    print(sum(arrangements))
