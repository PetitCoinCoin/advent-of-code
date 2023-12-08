import math
from pathlib import Path

DIRECTIONS_MAP = {
    "L": 0,
    "R": 1,
}

if __name__ == "__main__":
    with Path("day_08/input.txt").open("r") as file:
        data = {}
        directions = ""
        while line := file.readline():
            if len(line) > 1 and len(line.split(" = ")) != 2:
                directions = line.strip()
            elif len(line) > 1:
                key = line.split(" = ")[0]
                value = line.split(" = ")[1].replace("(", "").replace(")", "").split(", ")
                data[key] = [val.strip() for val in value]

        znodes = [key for key in data.keys() if key[-1] == "Z"]
        print(znodes)
        zsteps = {}
        for node in znodes:
            zstep = 0
            while node[-1] != "Z" or zstep == 0:
                node = data[node][DIRECTIONS_MAP[directions[zstep % len(directions)]]]
                zstep += 1
            zsteps[node] = zstep
        print(zsteps)

        anodes = [key for key in data.keys() if key[-1] == "A"]        
        print(anodes)
        asteps = {}
        for node in anodes:
            astep = 0
            while node[-1] != "Z":
                node = data[node][DIRECTIONS_MAP[directions[astep % len(directions)]]]
                astep += 1
            asteps[node] = astep
        print(asteps)

        # We notice that each --Z node loops on itself, and --Z > --> always equals --A > --Z
        print(math.lcm(*asteps.values()))
