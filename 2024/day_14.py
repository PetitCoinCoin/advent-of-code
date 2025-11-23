import argparse

from dataclasses import dataclass
from pathlib import Path
from time import time, sleep

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

WIDTH = 101
HEIGHT = 103

@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

def parse_input(raw: str) -> Robot:
    p, v = raw.split(" ")
    p = p[2:].split(",")
    v = v[2:].split(",")
    return Robot(
        x=int(p[0]),
        y=int(p[1]),
        vx=int(v[0]),
        vy=int(v[1]),
    )

def move(robots: list[Robot], duration: int) -> None:
    for r in robots:
        r.x = (r.x + r.vx * duration) % WIDTH
        r.y = (r.y + r.vy * duration) % HEIGHT

def safety_factor(robots: list[Robot]) -> int:
    quadrant = {
        "TL" : 0,
        "TR" : 0,
        "BL" : 0,
        "BR" : 0,
    }
    for r in robots:
        # left
        if r.x < WIDTH // 2:
            # bottom
            if r.y < HEIGHT // 2:
                quadrant["BL"] += 1
            # top
            elif r.y > HEIGHT // 2:
                quadrant["TL"] += 1
        # right
        elif r.x > WIDTH // 2:
            # bottom
            if r.y < HEIGHT // 2:
                quadrant["BR"] += 1
            # top
            elif r.y > HEIGHT // 2:
                quadrant["TR"] += 1
    result = 1
    for nb in quadrant.values():
        result *= nb
    return result

def has_frame(robots: list[Robot]) -> bool:
    """Looking for at least 10 robots in a row."""
    robots_dict = {}
    for r in robots:
        robots_dict[r.y] = robots_dict.get(r.y, set()) | {r.x}
    for set_x in robots_dict.values():
        if len(set_x) < 10:
            continue
        list_x = list(set_x)
        n = 0
        for i in range(1, len(set_x)):
            if list_x[i] - list_x[i - 1] == 1:
                n += 1
            elif n > 10:
                return True
            else:
                n = 0
    return False

def find_tree(robots: list[Robot]) -> int:
    """Assuming the tree is symmetrical."""
    duration = 0
    frame = has_frame(robots)
    while duration < 142000 and not frame:
        move(robots, 1)
        frame = has_frame(robots)
        duration += 1
    return duration

def pprint(robots: list[Robot]) -> None:
    robots_dict = {(r.x, r.y): "#" for r in robots}
    for y in range(HEIGHT):
        print("".join(robots_dict.get((x, y), ".") for x in range(WIDTH)))

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line.strip()) for line in file.readlines()]
    if args.part == 1:
        move(data, 100)
        print(safety_factor(data))
    else:
        print(find_tree(data))
        pprint(data)
    print(time() - t)
