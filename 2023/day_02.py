import argparse
import re

from dataclasses import dataclass
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

@dataclass
class Game:
    gid: int
    max_r: int
    max_g: int
    max_b: int

def format_game(game: str) -> Game:
    gid = int(game.split(":")[0].split(" ")[-1])
    max_r = max([int(x) for x in re.findall(r"(\d+)\sred", game)])
    max_g = max([int(x) for x in re.findall(r"(\d+)\sgreen", game)])
    max_b = max([int(x) for x in re.findall(r"(\d+)\sblue", game)])
    return Game(
        gid=gid,
        max_r=max_r,
        max_g=max_g,
        max_b=max_b,
    )

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = []
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            data.append(line)
    games = [format_game(game) for game in data]
    if args.part == 1:
        filtered_games = [
            game.gid
            for game in games
            if game.max_r <= 12 and
            game.max_g <= 13 and
            game.max_b <= 14
        ]
        print(sum(filtered_games))
    else:
        powered_games = [
            game.max_r * game.max_g * game.max_b
            for game in games
        ]
        print(sum(powered_games))
    print(time() - t)

