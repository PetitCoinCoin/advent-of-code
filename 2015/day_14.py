import argparse
import re

from dataclasses import dataclass
from pathlib import Path

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
class Reindeer:
    name: str
    speed: int
    duration: int
    rest: int

def parse_input(raw: str) -> Reindeer:
    name = raw.split(" ")[0]
    groups = re.findall(r"\d+", raw)
    return Reindeer(
        name=name,
        speed=int(groups[0]),
        duration=int(groups[1]),
        rest=int(groups[2]),
    )

def race(reindeer: Reindeer, duration: int) -> int:
    pattern_duration = reindeer.duration + reindeer.rest
    pattern_length = reindeer.speed * reindeer.duration
    count = duration // pattern_duration
    extra_duration = duration % pattern_duration
    extra_length = pattern_length if extra_duration >= reindeer.duration else reindeer.speed * extra_duration
    return count * pattern_length + extra_length

def get_positions(reindeer: Reindeer, duration: int) -> list:
    positions = [0]
    pattern_duration = reindeer.duration + reindeer.rest
    for s in range(1, duration + 1):
        positions.append(
            positions[s - 1] + reindeer.speed
            if (s - 1) % pattern_duration < reindeer.duration
            else positions[s - 1]
        )
    return positions

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(raw) for raw in file.read().split("\n")]
    race_duration = 2503
    if args.part == 1:
        print(max([race(reindeer, race_duration) for reindeer in data]))
    else:
        positions = dict()
        scores = dict()
        for reindeer in data:
            positions[reindeer.name] = get_positions(reindeer, race_duration)
        for s in range(1, race_duration + 1):
            max_km = max([pos[s] for pos in positions.values()])
            for name, pos in positions.items():
                if pos[s] == max_km:
                    scores[name] = scores.get(name, 0) + 1
        print(max(scores.values()))
