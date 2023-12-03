from collections import defaultdict
from contextlib import suppress
from pathlib import Path

if __name__ == "__main__":
    with Path("day_03/input.txt").open("r") as file:
        data = file.read().split()

    col = len(data[0])
    row = len(data)
    gear = defaultdict(lambda: [])
    for i in range(row):
        star = None
        str_nb = ""
        for j in range(col):
            if data[i][j].isdigit():
                if not star:
                    str_nb += data[i][j]
                    with suppress(IndexError):
                        for y in (i -1, i, i + 1):
                            for x in (j - 1, j, j + 1):
                               if data[y][x] == "*":
                                    star = (y, x)
                                    break
                            else:
                                continue
                            break
                else:
                    str_nb += data[i][j]
                if star and j == len(data[i]) - 1:
                    gear[star].append(int(str_nb))
                    str_nb = ""
                    star = None
            else:
                if star:
                    gear[star].append(int(str_nb))
                str_nb = ""
                star = None
    result = 0
    for k,value in gear.items():
        if len(value) == 2:
            result += value[0] * value[1]
    print(result)
