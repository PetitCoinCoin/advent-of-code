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

class Ship:
    def __init__(self, part: int) -> None:
        self.position = complex(0, 0)
        self.waypoint = complex(10, 1)
        self.facing = 1
        self.move = self.__move_alone if part == 1 else self.__move_relative

    def __move_alone(self, instruction: str) -> None:
        action = instruction[0]
        value = int(instruction[1:])
        match action:
            case "N":
                self.position += value * 1j
            case "E":
                self.position += value
            case "S":
                self.position -= value * 1j
            case "W":
                self.position -= value
            case "F":
                self.position += value * self.facing
            case "R":
                self.facing *= (-1j) ** (value // 90)
            case "L":
                self.facing *= (1j) ** (value // 90)
            case _:
                print("WTF")

    def __move_relative(self, instruction: str) -> None:
        action = instruction[0]
        value = int(instruction[1:])
        match action:
            case "N":
                self.waypoint += value * 1j
            case "E":
                self.waypoint += value
            case "S":
                self.waypoint -= value * 1j
            case "W":
                self.waypoint -= value
            case "F":
                self.position += value * self.waypoint
            case "R":
                self.waypoint *= (-1j) ** (value // 90)
            case "L":
                self.waypoint *= (1j) ** (value // 90)
            case _:
                print("WTF")

    @property
    def distance(self) -> int:
        return int(abs(self.position.real) + abs(self.position.imag))

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    ship = Ship(args.part)
    for instruction in data:
        ship.move(instruction)
    print(ship.distance)
    print(time() - t)
