from pathlib import Path

def get_previous(serie: list) -> int:
    if not any(serie):
        return 0
    diff = []
    for i in range(len(serie) - 1, 0, -1):
        diff.insert(0, serie[i] - serie[i - 1])
    return serie[0] - get_previous(diff)

if __name__ == "__main__":
    with Path("day_09/input.txt").open("r") as file:
        data = []
        while line := file.readline():
            data.append([int(x.strip()) for x in line.split(" ")])
    all_previous = [get_previous(serie) for serie in data]
    print(sum(all_previous))
