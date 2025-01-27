import argparse
import re

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

class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.right = None
        self.left = None
    
class CircleList:
    def __init__(self) -> None:
        self.current = None

    def insert(self, value: int) -> None:
        node = Node(value)
        if not self.current:
            node.right, node.left = node, node
        else:
            left = self.current.right
            right = left.right
            node.left = left
            left.right = node
            node.right = right
            right.left = node
        self.current = node

    def pop(self) -> int:
        for _ in range(6):
            self.current = self.current.left
        deleted = self.current.left
        self.current.left = deleted.left
        deleted.left.right = self.current
        return deleted.value

def play() -> int:
    players = {}
    for p in range(PLAYERS):
        players[p] = 0
    circle = CircleList()
    marble = 0
    while marble <= MAX_MARBLE:
        if marble and not marble % 23:
            player = ((marble % PLAYERS) - 1) % PLAYERS
            players[player] += marble + circle.pop()
        else:
            circle.insert(marble)
        marble += 1
    return max(players.values())

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        PLAYERS, MAX_MARBLE = map(int, re.findall(r"(\d+)", file.read()))
    if args.part == 2:
        MAX_MARBLE *= 100
    print(play())
    print(time() - t)
