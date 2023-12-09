from pathlib import Path

def get_next(serie: list) -> int:
    if not any(serie):
        return 0
    diff = []
    for i in range(1, len(serie)):
        diff.append(serie[i] - serie[i - 1])
    return serie[-1] + get_next(diff)

if __name__ == "__main__":
    with Path("day_09/input.txt").open("r") as file:
        data = []
        while line := file.readline():
            data.append([int(x.strip()) for x in line.split(" ")])
    all_next = [get_next(serie) for serie in data]
    print(sum(all_next))
