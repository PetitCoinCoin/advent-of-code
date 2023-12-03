from contextlib import suppress
from pathlib import Path

if __name__ == "__main__":
    with Path("day_03/input.txt").open("r") as file:
        data = file.read().split()

    result = 0
    col = len(data[0])
    row = len(data)
    for i in range(row):
        to_add = False
        str_nb = ""
        for j in range(col):
            if data[i][j].isdigit():
                if not to_add:
                    str_nb += data[i][j]
                    with suppress(IndexError):
                        for y in (i - 1, i, i + 1):
                            for x in (j - 1, j, j + 1):
                               if (x != j or y != i) and x>=0 and y >= 0 and data[y][x] != "." and not data[y][x].isdigit():
                                    to_add = True
                                    break
                            else:
                                continue
                            break
                else:
                    str_nb += data[i][j]
                if to_add and j == len(data[i]) - 1:
                    result += int(str_nb)
                    str_nb = ""
                    to_add = False
            else:
                if to_add:
                    result += int(str_nb)
                str_nb = ""
                to_add = False
    print(result)
