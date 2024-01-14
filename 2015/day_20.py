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

def count_presents(house: int, amount: int, limit: int = 0) -> int:
    presents = set()
    for i in range(1, int(house ** (1/2) + 1)):
        if not house % i:
            if not limit or house // i <= limit:
                presents.add(i)
            if not limit or i <= limit:
                presents.add(house // i)
    return amount * sum(presents)

if __name__ == "__main__":
    args = _parse_args()
    data = 34000000
    i = 1
    if args.part == 1:
        while count_presents(i, 10) < data:
            i += 1
    else:
        while count_presents(i, 11, 50) < data:
            i += 1
    print(i)
