from pathlib import Path

def digitize(value: str) -> int:
    digits = [x for x in value if x.isdigit()]
    return int(digits[0] + digits[-1])

if __name__ == "__main__":
    with Path("day_01/input.txt").open("r") as file:
        data = file.read().split()
    calibrations_values = [digitize(value) for value in data]
    print(sum(calibrations_values))