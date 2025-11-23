import argparse

from pathlib import Path
from time import time

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

REGION_SIZE = 10000

def manhattan(x: complex, y: complex) -> int:
    return abs(x.real - y.real) + abs(x.imag - y.imag)

def closest_neighbor(coordinates: dict, position: complex) -> int:
    min_distance = 0, 1000000
    multi = False
    for coord, pos in coordinates.items():
        distance = manhattan(pos, position)
        if distance < min_distance[1]:
            min_distance = coord, distance
            multi = False
        elif distance == min_distance[1]:
            multi = True
    return 0 if multi else min_distance[0]

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = dict()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        coordinate = 1
        max_real, max_imag = 0, 0
        while line:= file.readline().strip():
            real, imag = tuple(int(x) for x in line.split(", "))
            if real > max_real:
                max_real = real
            if imag > max_imag:
                max_imag = imag
            data[coordinate] = complex(real, imag)
            coordinate += 1
    if args.part == 1:
        areas = dict()
        for coord in range(1, coordinate):
            areas[coord] = 0
        infinite = set()
        for r in range(max_real + 1):
            for i in range(max_imag + 1):
                closest = closest_neighbor(data, complex(r, i))
                if closest:
                    areas[closest] += 1
                    if r in (0, max_real) or i in (0, max_imag):
                        infinite.add(closest)
        max_area = 0
        for coord, area in areas.items():
            if area > max_area and coord not in infinite:
                max_area = area
        print(max_area)
    else:
        safe_area = 0
        for r in range(max_real + 1):
            for i in range(max_imag + 1):
                distance = sum(manhattan(pos, complex(r, i)) for pos in data.values())
                if distance < REGION_SIZE:
                    safe_area += 1
        print(safe_area)
    print(time() - t)
