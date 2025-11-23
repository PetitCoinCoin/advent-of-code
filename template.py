from pathlib import Path
from time import time

from py_utils.parsers import parse_args

if __name__ == "__main__":
    args = parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    if args.part == 1:
        print(data)
    else:
        raise NotImplementedError
    print(time() - t)
