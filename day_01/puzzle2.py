from pathlib import Path

NUM_MAP = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5e",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}
def digitize(value: str) -> int:
    for k,v in NUM_MAP.items():
        value = value.replace(k, v)
    digits = [x for x in value if x.isdigit()]
    return int(digits[0] + digits[-1])

if __name__ == "__main__":
    with Path("day_01/input.txt").open("r") as file:
        data = file.read().split()
    calibrations_values = [digitize(value) for value in data]
    print(sum(calibrations_values))
