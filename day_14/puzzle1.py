from pathlib import Path

def tilt_west(row: str) -> str:
    round_count = len([rock for rock in row if rock == "O"])
    return round_count * "O" + (len(row) - round_count) * "."

def tilt(platform: list) -> list:
    return ["#".join([tilt_west(sub_row) for sub_row in row.split("#")]) for row in platform]

def transpose(matrix: list) -> list:
    return ["".join(item) for item in list(zip(*matrix))]

def get_round(row: str) -> int:
    return len([rock for rock in row if rock == "O"])

if __name__ == "__main__":
    with Path("day_14/input.txt").open("r") as file:
        data = file.read().split()
    tilted_north = transpose(tilt(transpose(data)))
    count = len(data)
    weights = [(count - i) * get_round(row) for i, row in enumerate(tilted_north)]
    print(sum(weights))
