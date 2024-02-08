import argparse

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

def dragon(raw: str) -> str:
    reversed_raw = "".join(['1' if c == '0' else '0' for c in raw[::-1]])
    return f"{raw}0{reversed_raw}"

def get_checksum(raw:str) -> str:
    checksum = ""
    for i in range(0, len(raw), 2):
        checksum += "1" if raw[i] == raw[i + 1] else "0"
    return checksum

if __name__ == "__main__":
    args = _parse_args()
    data = "10001001100000001"
    if args.part == 1:
        dragon_length = 272
    else:
        dragon_length = 35651584
    while len(data) < dragon_length:
        data = dragon(data)
    checksum = get_checksum(data[:dragon_length])
    while not len(checksum) % 2:
        checksum = get_checksum(checksum)
    print(checksum)
