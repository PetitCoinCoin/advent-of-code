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

def remove_garbage(stream: str) -> tuple[str, int]:
    res = ""
    garbage_count = 0
    in_garbage = False
    masked = 0
    for i, char in enumerate(stream):
        garbage_start = False
        if masked and i == masked + 2:
            masked = 0
        if char == "<":
            if not in_garbage:
                garbage_start = True
            in_garbage = True
        elif char == ">" and in_garbage and not masked:
            in_garbage = False
        elif char == "!" and in_garbage and not masked:
            masked = i
        if in_garbage and not masked and not garbage_start:
            garbage_count += 1
        if not in_garbage and char in ("{", "}"):
            res += char
    return res, garbage_count

def get_score(stream: str) -> int:
    score = 0
    current = 0
    for char in stream:
        if char == "{":
            current += 1
            score += current
        elif char == "}":
            current -= 1
        else:
            print("WTF")
    return score

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read()
    clean, count = remove_garbage(data)
    if args.part == 1:
        print(get_score(clean))
    else:
        print(count)
