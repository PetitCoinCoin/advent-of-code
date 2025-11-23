import argparse

from hashlib import md5
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

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip()
    index = 0
    code = [""] * 8
    while len([c for c in code if c]) < 8:
        if md5(f"{data}{index}".encode()).hexdigest().startswith("00000"):
            if args.part == 1:
                code[len([c for c in code if c])] = md5(f"{data}{index}".encode()).hexdigest()[5]
            else:
                hashed = md5(f"{data}{index}".encode()).hexdigest()
                if hashed[5].isdigit() and int(hashed[5]) < 8 and not code[int(hashed[5])]:
                    code[int(hashed[5])] = hashed[6]
        index += 1
    print("".join(code))
