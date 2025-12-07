from pathlib import Path
from time import time

from py_utils.parsers import parse_args

def parse_input(lines: list) -> int:
    start_col = None
    for r, line in enumerate(lines):
        if "S" in line:
            start_col = line.index("S")
        elif "^" in line:
            data[r] = {c for c in range(len(line)) if line[c] == "^"}
    return start_col

if __name__ == "__main__":
    args = parse_args()
    t = time()
    data = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        start = parse_input(file.read().strip().split("\n"))
    # We consider that splitters are located one every two rows
    beams = {0: {start}}
    timelines = {(0, start): 1}
    max_row = 0
    splitted = 0
    for row, splitters in data.items():
        new_beams = set()
        for splitter in splitters:
            if splitter in beams[row - 2]:
                splitted += 1
                new_beams |= {splitter - 1, splitter + 1}
                timelines[(row, splitter - 1)] = timelines.get((row, splitter - 1), 0) + timelines[(row - 2, splitter)]
                timelines[(row, splitter + 1)] = timelines.get((row, splitter + 1), 0) + timelines[(row - 2, splitter)]
        for beam in beams[row - 2] - splitters:
            timelines[(row, beam)] = timelines.get((row, beam), 0) + timelines[row - 2, beam]
        beams[row] = beams[row - 2] - splitters | new_beams
        max_row = row
    if args.part == 1:
        print(splitted)
    else:
        print(sum(
            timeline
            for position, timeline in timelines.items()
            if position[0] == max_row
        ))
    print(time() - t)
