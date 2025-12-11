import re

from functools import cache
from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def parse_input(lines: list) -> None:
    pattern = r"(\w+)"
    for line in lines:
        devices = re.findall(pattern, line)
        if devices[0] in data:
            print("Watch out!")
        data[devices[0]] = devices[1:]

@cache
def get_paths_out(start: str, seen: str = "", via_devices: tuple = ()) -> tuple:
    if start == "out":
        if not via_devices:  # part 1
            return 1
        return 1 if all(device in seen for device in via_devices) else 0
    if start in via_devices:
         seen += start
    return sum(get_paths_out(child, seen, via_devices) for child in data[start])

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        parse_input(file.read().strip().split("\n"))
    if args.part == 1:
        print(get_paths_out("you"))
    else:
        print(get_paths_out("svr", via_devices=("dac", "fft")))
    print(time() - t)
