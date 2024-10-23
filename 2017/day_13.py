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

def parse_input(raw: str) -> int:
    splitted = raw.split(": ")
    return int(splitted[0]), int(splitted[1])

def get_severity(layers: dict, max_layer: int, offset: int = 0, *, is_part_two: bool = False) -> tuple[int, int]:
    caught = []
    for i in range(max_layer + 1):
        if not layers.get(i):
            continue
        if not (i + offset) % (2 * (layers[i] - 1)):
            if is_part_two:
                return 1
            caught.append(i)
    return sum(layers[l] * l for l in caught)


if __name__ == "__main__":
    args = _parse_args()
    data = dict()
    max_layer = 0
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            key, value = parse_input(line)
            data[key] = value
            max_layer = key
    if args.part == 1:
        print(get_severity(data, max_layer))
    else:
        delta = 0
        while get_severity(data, max_layer, delta, is_part_two=True):
            delta += 1
        print(delta)
