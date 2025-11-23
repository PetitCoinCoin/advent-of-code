import argparse
import math
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
class Particle:
    p: tuple[int, int, int]
    v: tuple[int, int, int]
    a: tuple[int, int, int]

def parse_input(raw: str) -> Particle:
    props = re.findall(r"p=<(.+)>, v=<(.+)>, a=<(.+)>", raw)[0]
    return Particle(
        p=tuple(int(x) for x in props[0].split(",")),
        v=tuple(int(x) for x in props[1].split(",")),
        a=tuple(int(x) for x in props[2].split(",")),
    )

def manhattan_quadratic(part: Particle) -> int:
    """Caculates manhattan distance over quadratic term.
    On the long term, only acceleration term is important."""
    return sum(i * j for i,j in zip(part.a, part.a))

def move(part: Particle) -> Particle:
    part.v = tuple(v + a for v,a in zip(part.v, part.a))
    part.p = tuple(p + v for p,v in zip(part.p, part.v))
    return part

def remove_collisions(particles: list) -> None:
    for i in range(len(particles) - 1):
        collides = False
        if particles[i] is not None:
            for j in range(i + 1, len(particles)):
                if particles[i].p == particles[j].p:
                    collides = True
                    particles[j] = None
            if collides:
                particles[i] = None

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().split("\n")]
    if args.part == 1:
        min_distance = math.inf
        min_distance_particle = -1
        for i, distance in enumerate(manhattan_quadratic(particle) for particle in data):
            if distance < min_distance:
                min_distance_particle = i
                min_distance = distance
        print(min_distance_particle)
    else:
        stable = 0
        data_length = len(data)
        while stable < 20:  # Arbitrary value for stabilisation (got lucky on first try!)
            data = [move(particle) for particle in data if particle is not None]
            remove_collisions(data)
            current_length = len([x for x in data if x is not None])
            if current_length == data_length:
                stable += 1
            else:
                data_length = current_length
        print(data_length)
