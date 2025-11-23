import argparse

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

def parse_input(raw: str) -> tuple[str, list]:
    splitted = raw.split(" <-> ")
    key = splitted[0]
    value = [x.strip() for x in splitted[1].split(",")]
    return key, value

def get_linked(pipes: dict, start: str) -> list:
    seen = dict()
    linked = []
    queue = [start]
    while queue:
        program = queue.pop(0)
        for prog in pipes[program]:
            if seen.get(prog):
                continue
            linked.append(prog)
            queue.append(prog)
            seen[prog] = True
    return linked

if __name__ == "__main__":
    args = _parse_args()
    data = dict()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            key, value = parse_input(line)
            data[key] = value
    if args.part == 1:
        print(len(get_linked(data, '0')))
    else:
        count = 0
        while data:
            for key in data.keys():
                start = key
                break
            linked = get_linked(data, start)
            count += 1
            for key in linked:
                del data[key]
        print(count)