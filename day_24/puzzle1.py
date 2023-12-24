from pathlib import Path

def sign(a: float) -> int:
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0

def calculate_trajectory(row: str) -> tuple:
    position = [int(pos) for pos in row.split(" @ ")[0].split(", ")]
    speed = [int(s) for s in row.split(" @ ")[1].split(", ")]
    # Trajectory is y = ax + b (don't pay attention to z for now), with:
    a = speed[1] / speed[0]
    b = position[1] - (speed[1] * position[0]) / speed[0]
    return a, b, position, speed

def in_future(x: float, y: float, positions: list, speed: list) -> bool:
    if sign(y - positions[1]) != sign(speed[1]):
        return False
    if sign(x - positions[0]) != sign(speed[0]):
        return False
    return True

def get_intesections(data: list, min_th: int, max_th: int) -> list:
    intersections = []
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            if data[i][0] == data[j][0]:  # parallel paths
                continue
            x_cross = (data[j][1] - data[i][1]) / (data[i][0] - data[j][0])
            y_cross = data[i][0] * (data[j][1] - data[i][1]) / (data[i][0] - data[j][0]) + data[i][1]
            if max_th >= x_cross >= min_th and max_th >= y_cross >= min_th and \
                in_future(x_cross, y_cross, data[i][2], data[i][3]) and in_future(x_cross, y_cross, data[j][2], data[j][3]):
                intersections.append((x_cross, y_cross))
    return intersections

if __name__ == "__main__":
    with Path("day_24/input.txt").open("r") as file:
        data = [calculate_trajectory(row) for row in  file.read().splitlines()]
    print(len(get_intesections(data, 200000000000000, 400000000000000)))
