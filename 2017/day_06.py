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

def redistribute(items: list) -> list:
    max_idx = items.index(max(items))
    nb_blocks = items[max_idx]
    items[max_idx] = 0
    items = [item + nb_blocks // len(items) for item in items]
    for delta in range(1, nb_blocks % len(items) + 1):
        items[(max_idx + delta) % len(items)] += 1
    return items

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().split("\t")]
    seen = dict()
    cpt = 0
    while seen.get(str(data)) is None:
        seen[str(data)] = cpt
        data = redistribute(data)
        cpt += 1
    if args.part == 1:
        print(cpt)
    else:
        print(cpt - seen.get(str(data)))
