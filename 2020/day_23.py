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

class Cup:
    def __init__(self, value: int) -> None:
        self.value = value
        self.right = None
        self.left = None
    
    def __str__(self) -> str:
        return f"{self.value}: {self.left.value} - {self.right.value}"
    
class CircleList:
    def __init__(self, cups: list) -> None:
        self.current = None
        self.max = len(cups)
        for value in cups:
            cup = Cup(value)
            if not self.current:
                cup.right, cup.left = cup, cup
            else:
                right = self.current.right
                self.current.right = cup
                cup.left = self.current
                cup.right = right
                right.left = cup
            self.current = cup
        self.current = self.current.right

    def move(self) -> None:
        picked = [self.current.right, self.current.right.right, self.current.right.right.right]
        picked_values = [cup.value for cup in picked]
        dest_value = self.current.value - 1
        if not dest_value:
            dest_value = self.max
        while dest_value in picked_values:
            dest_value -= 1
            if not dest_value:
                dest_value = self.max
        self.current.right = picked[-1].right
        picked[-1].right.left = self.current
        cup = self.current.right
        while cup.value != dest_value:
            cup = cup.right
        cup.right.left = picked[-1]
        picked[-1].right = cup.right
        cup.right = picked[0]
        picked[0].left = cup
        self.current = self.current.right

    @property
    def order(self) -> str:
        cup = self.current
        while cup.left.value != 1:
            cup = cup.right
        result = ""
        while cup.value != 1:
            result += str(cup.value)
            cup = cup.right
        return result

def play(cups: list) -> int:
    current = cups[-1]
    for _ in range(10000000):
        picked = [cups[current], cups[cups[current]], cups[cups[cups[current]]]]
        destination = current - 1
        if not destination:
            destination = len(cups) - 1
        while destination in picked:
            destination -= 1
            if not destination:
                destination = len(cups) - 1
        cups[destination], cups[current], cups[picked[-1]] = cups[current], cups[picked[-1]], cups[destination]
        current = cups[current]
    right = cups[1]
    sec_right = cups[right]
    print(right, sec_right)
    return right * sec_right

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip()]
    if args.part == 1:
        game = CircleList(data)
        for i in range(100):
            game.move()
        print(game.order)
    else:
        game = list(range(1, 1000000 + 1))
        for i, cup in enumerate(data):
            game[cup] = data[(i + 1) % len(data)]
        game[0] = 0
        game[data[-1]] = len(data) + 1
        game.append(data[0])
        print(play(game))
    print(time() - t)
