import argparse
import math
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
class Race():
    duration: int
    distance: int

def get_margins(race: Race) -> int:
    """
    Solving this problem is equivalent to solving:
    x(T-x) = D with T, race.duration and D, race.distance.
    """
    delta = (race.duration ** 2) - (4 * race.distance)
    min_duration = (-race.duration + delta ** 0.5) / -2
    if math.ceil(min_duration) == min_duration:
        min_duration += 1
    else:
        min_duration = math.ceil(min_duration)
    max_duration = (-race.duration - delta ** 0.5) / -2
    if int(max_duration) == max_duration:
        max_duration -= 1
    else:
        max_duration = int(max_duration)
    return int(max_duration - min_duration + 1)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        times, distances = [
            map(int, re.findall(r"(\d+)", raw))
            for raw in file.read().strip().split("\n")
        ]
    if args.part == 1:
        races = [Race(dt, d) for dt, d in zip(times, distances)]
        margins = [get_margins(race) for race in races]
        result = 1
        for margin in margins:
            result *= margin
        print(result)
    else:
        race = Race(41777096, 249136211271011)
        margins = get_margins(race)
        print(margins)
    print(time() - t)

