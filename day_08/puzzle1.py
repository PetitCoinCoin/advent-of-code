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
                value = line.split(" = ")[1].replace("(", "").replace(")\n", "").split(", ")
                data[key] = value
        
        node = "AAA"
        steps = 0
        while node != "ZZZ":
            node = data[node][DIRECTIONS_MAP[directions[steps % len(directions)]]]
            steps += 1
        print(steps)
