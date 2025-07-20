import argparse

from collections import deque
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

class Player:
    def __init__(self, deck: list, idx: int) -> None:
        self.deck = deque(deck)
        self.idx = idx
    
    @property
    def score(self) -> int:
        return sum((i + 1) * x for i, x in enumerate(list(self.deck)[::-1]))
    
    @property
    def str_deck(self) -> str:
        return ",".join(str(x) for x in self.deck)

class Game:
    def __init__(self, p1: Player, p2: Player) -> None:
        self.p1 = p1
        self.p2 = p2
        self.winner = None
        self.history = set()
    
    def play(self):
        while self.p1.deck and self.p2.deck:
            c1 = self.p1.deck.popleft()
            c2 = self.p2.deck.popleft()
            if c1 > c2:
                self.p1.deck.extend([c1, c2])
            else:
                self.p2.deck.extend([c2, c1])
        if self.p1.deck:
            self.winner = self.p1
        else:
            self.winner = self.p2
    
    def play_recursive(self):
        while self.p1.deck and self.p2.deck:
            history = f"{self.p1.str_deck}+{self.p2.str_deck}"
            # avoid infinite loop
            if history in self.history:
                self.winner = self.p1
                return
            # let's play
            c1 = self.p1.deck.popleft()
            c2 = self.p2.deck.popleft()
            # recursion
            if len(self.p1.deck) >= c1 and len(self.p2.deck) >= c2:
                sub_game = Game(
                    Player([x for x in list(self.p1.deck)[:c1]], 1),
                    Player([x for x in list(self.p2.deck)[:c2]], 2),
                )
                sub_game.play_recursive()
                winner = sub_game.winner.idx
                if winner == 1:
                    self.p1.deck.extend([c1, c2])
                else:
                    self.p2.deck.extend([c2, c1])
            # classic
            else:
                if c1 > c2:
                    self.p1.deck.extend([c1, c2])
                else:
                    self.p2.deck.extend([c2, c1])
            self.history.add(history)
        if self.p1.deck:
            self.winner = self.p1
        else:
            self.winner = self.p2

    @property
    def winner_score(self) -> int:
        return self.winner.score

def parse_input(data: list) -> Game:
    p1 = Player([int(x) for x in data[0].split("\n")[1:]], 1)
    p2 = Player([int(x) for x in data[1].split("\n")[1:]], 2)
    return Game(p1, p2)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        game = parse_input(file.read().strip().split("\n\n"))
    if args.part == 1:
        game.play()
    else:
        game.play_recursive()
    print(game.winner_score)
    print(time() - t)
