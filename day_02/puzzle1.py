import re
from dataclasses import dataclass
from pathlib import Path

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
    with Path("day_02/input.txt").open("r") as file:
        data = []
        while line := file.readline():
            data.append(line)
    games = [format_game(game) for game in data]
    filtered_games = [
        game.gid
        for game in games
        if game.max_r <= 12 and
        game.max_g <= 13 and
        game.max_b <= 14
    ]
    print(sum(filtered_games))
