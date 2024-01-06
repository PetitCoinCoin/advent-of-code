import argparse

from itertools import groupby

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

def look_and_say(number: str) -> str:
    result = ""
    for value, group in groupby(number):
        result += str(len(list(group))) + value
    return result

if __name__ == "__main__":
    args = _parse_args()
    data = "3113322113"
    if args.part == 1:
        steps = 40
    else:
        # bruteforce with correct data structure seems to work :)
        steps = 50
    for i in range(steps):
        data = look_and_say(data)
    print(len(data))
