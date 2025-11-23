import argparse

from copy import deepcopy
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

DELTAS = (
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (-1, 1), (-1, -1), (1, -1),
)

class Area:
    def __init__(self, seats: str, part: int) -> None:
        self.seats = {}
        for r, row in enumerate(seats.split("\n")):
            for c, char in enumerate(row):
                if char != ".":
                    self.seats[(r, c)] = 1 if char == "#" else 0
                self.max_c = c
            self.max_r = r
        self.previous_seats = {}
        self.stable = False
        self.closest_seat = part == 1
        self.max_occupied = 4 if part == 1 else 5
    
    def simulate(self) -> None:
        self.previous_seats = deepcopy(self.seats)
        self.stable = True
        for seat, state in self.previous_seats.items():
            r, c = seat
            if not state and not sum(self.previous_seats.get(s, 0) for s in self.__get_next_seats(r, c)):
                self.seats[seat] = 1
                self.stable = False
            if state and sum(self.previous_seats.get(s, 0) for s in self.__get_next_seats(r, c)) >= self.max_occupied:
                self.seats[seat] = 0
                self.stable = False

    def __get_next_seats(self, r: int, c: int) -> list:
        result = []
        for dr, dc in DELTAS:
            i = 1
            while 0 <= r + i * dr <= self.max_r and 0 <= c + i * dc <= self.max_c:
                if (r + i * dr, c + i * dc) in self.previous_seats:
                    result.append((r + i * dr, c + i * dc))
                    break
                if self.closest_seat:
                    break
                i += 1
        return result

    def pprint(self) -> None:
        """For debug"""
        for r in range(self.max_r + 1):
            print("".join("#" if self.seats.get((r, c), -1) == 1 else "L" if self.seats.get((r, c), - 1) == 0 else "." for c in range(self.max_c + 1)))
        print()

    @property
    def occupied(self) -> int:
        return sum(self.seats.values())

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip()
    area = Area(data, args.part)
    while not area.stable:
        area.simulate()
    print(area.occupied)
    print(time() - t)
