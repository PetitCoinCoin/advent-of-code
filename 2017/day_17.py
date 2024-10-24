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

STEPS = 301

if __name__ == "__main__":
    args = _parse_args()
    idx = 0
    if args.part == 1:
        data = [0]
        for val in range(1, 2018):
            idx = (idx + STEPS) % len(data)
            data = data[:idx + 1] + [val] + data[idx + 1:]
            idx += 1
        print(data[idx + 1])
    else:
        sec_value = 0
        for val in range(1, 50000001):
            idx = (idx + STEPS) % val
            if not idx:
                sec_value = val
            idx += 1
        print(sec_value)
