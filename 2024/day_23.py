import argparse

from itertools import combinations
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

def parse_input(raw:str) -> None:
    c1, c2 = raw.split("-")
    data[c1] = data.get(c1, set()) | {c2}
    data[c2] = data.get(c2, set()) | {c1}

def connected_three() -> list:
    lans = []
    for computer, linked in data.items():
        for other in linked:
            lan = linked.intersection(data[other])
            for comp in lan:
                three_lan = {computer, other, comp}
                if three_lan not in lans and (
                    computer.startswith("t") 
                    or other.startswith("t") 
                    or comp.startswith("t")
                ):
                    lans.append(three_lan)
    return lans

def lan_party() -> str:
    max_lan_count = 0
    max_lan = set()
    for computer, linked in data.items():
        combi = len(linked)
        while combi > max_lan_count - 1:
            for c in combinations(list(linked), combi):
                lan = set(c)
                lan.add(computer)
                for comp in c:
                    lan = lan.intersection({comp} | data[comp])
                if len(lan) > max_lan_count:
                    max_lan_count = len(lan)
                    max_lan = lan
            combi -= 1
    return ",".join(sorted(list(max_lan)))

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            parse_input(line.strip())
    if args.part == 1:
        print(len(connected_three()))
    else:
        print(lan_party())
    print(time() - t)
