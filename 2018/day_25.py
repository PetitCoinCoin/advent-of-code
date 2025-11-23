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

def distance(t1: tuple, t2: tuple) -> int:
    return sum(abs(t1[i] - t2[i]) for i in range(4))

def is_in_same_constellation(t1: tuple, t2: tuple) -> bool:
    return distance(t1, t2) <= 3

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [tuple([int(x) for x in line.split(",")]) for line in file.read().strip().split("\n")]
    if args.part == 1:
        constellations = {}
        const_key = 1
        to_del = set()
        for coord in data:
            linked = 0
            for k, constellation in constellations.items():
                if k in to_del:
                    continue
                for star in constellation:
                    if is_in_same_constellation(star, coord):
                        if linked:
                            constellation |= constellations[linked]
                            to_del.add(linked)
                            linked = k
                            break
                        else:
                            constellation.add(coord)
                            linked = k
                            break
            if not linked:
                constellations[const_key] = {coord}
                const_key += 1
        print(len(constellations.keys()) - len(to_del))
    else:
        raise NotImplementedError
    print(time() - t)
