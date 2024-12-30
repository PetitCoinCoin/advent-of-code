import argparse

from pathlib import Path
from time import time

# Failed to use only built-in packages for this one
import sympy as sp
from sympy import solve

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--part", "-p",
        type=int,
        choices={1, 2},
        help="Set puzzle part"
    )
    args = parser.parse_args()
    if not args.part:
        parser.error("Which part are you solving?")
    return args

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
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [calculate_trajectory(row) for row in  file.read().splitlines()]
    if args.part == 1:
        print(len(get_intesections(data, 200000000000000, 400000000000000)))
    else:
        # Took 3 first hailstones data to build a system of 9 equations with 9 variables
        x, y, z, t1, t2, t3, vx, vy, vz = sp.symbols('x, y, z, t1, t2, t3, vx, vy, vz')
        eq1 = sp.Eq(z + vz * t1 - 262795384692232 - 39 * t1, 0)
        eq2 = sp.Eq(y + vy * t1 - 401088290781515 + 36 * t1, 0)
        eq3 = sp.Eq(x + vx * t1 - 189484959431670 - 95 * t1, 0)
        eq4 = sp.Eq(z + vz * t2 - 297355219841654 + 56 * t2, 0)
        eq5 = sp.Eq(y + vy * t2 - 163094456512341 - 182 * t2, 0)
        eq6 = sp.Eq(x + vx * t2 - 175716591307178 - 160 * t2, 0)
        eq7 = sp.Eq(z + vz * t3 - 314435988531407 + 10 * t3, 0)
        eq8 = sp.Eq(y + vy * t3 - 363632912812075 - 37 * t3, 0)
        eq9 = sp.Eq(x + vx * t3 - 283402568811320 + 6 * t3, 0)
        output = solve([eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9], x, y, z, t1, t2, t3, vx, vy, vz, dict=True)
        print(output[0][x] + output[0][y] + output[0][z])
    print(time() - t)

