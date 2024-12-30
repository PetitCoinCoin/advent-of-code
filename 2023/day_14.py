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

def tilt_west(row: str) -> str:
    round_count = len([rock for rock in row if rock == "O"])
    return round_count * "O" + (len(row) - round_count) * "."

def tilt(platform: list) -> list:
    return ["#".join([tilt_west(sub_row) for sub_row in row.split("#")]) for row in platform]

def transpose(matrix: list) -> list:
    return ["".join(item) for item in list(zip(*matrix))]

def tilt_row_west(row: str) -> str:
    round_count = len([rock for rock in row if rock == "O"])
    return round_count * "O" + (len(row) - round_count) * "."

def tilt_row_east(row: str) -> str:
    round_count = len([rock for rock in row if rock == "O"])
    return (len(row) - round_count) * "." + round_count * "O"

def tilt_north(platform: list) -> list:
    return transpose(
        [
            "#".join([tilt_row_west(sub_row) for sub_row in row.split("#")])
            for row in transpose(platform)
        ]
    )

def tilt_cycle(platform: list) -> list:
    tilt1 = tilt_north(platform)
    tilt2 = ["#".join([tilt_row_west(sub_row) for sub_row in row.split("#")]) for row in tilt1]
    tilt3 = tilt_north(tilt2[::-1])[::-1]
    return ["#".join([tilt_row_east(sub_row) for sub_row in row.split("#")]) for row in tilt3]

def get_round(row: str) -> int:
    return len([rock for rock in row if rock == "O"])

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split()
    if args.part == 1:
        tilted_north = transpose(tilt(transpose(data)))
        count = len(data)
        weights = [(count - i) * get_round(row) for i, row in enumerate(tilted_north)]
        print(sum(weights))
    else:
        cache = {"-".join(data): 0}
        for i in range(1, 1000000000):
            data = tilt_cycle(data)
            if "-".join(data) in cache:
                init = cache["-".join(data)]
                delta = i - init
                shift = (100000000 - init) % delta + init
                for k, v in cache.items():
                    if v == 104:
                        final = k.split("-")
                        count = len(final)
                        weights = [(count - i) * get_round(row) for i, row in enumerate(final)]
                        print(sum(weights))
                        break
                break
            else:
                cache["-".join(data)] = i
    print(time() - t)

