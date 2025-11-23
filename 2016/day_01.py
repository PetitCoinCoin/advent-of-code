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

DIRECTIONS_MAP = {
    "R": complex(0, -1),
    "L": complex(0, 1),
}

def get_range(previous: int, current: int) -> range:
    reverse = 1 if current > previous else -1
    return range(previous + reverse, current - reverse, reverse)

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split(", ")
    step = complex(0, 0)
    multiplicator = complex(0, 1)
    if args.part == 1:
        for direction in data:
            multiplicator *= DIRECTIONS_MAP[direction[0]]
            step += int(direction[1:]) * multiplicator
        print(step, abs(step.real) + abs(step.imag))
    else:
        seen = {step}
        for direction in data:
            previous_step =step
            multiplicator *= DIRECTIONS_MAP[direction[0]]
            blocks = int(direction[1:])
            step += blocks * multiplicator
            if multiplicator.real:
                for x in get_range(int(previous_step.real), int(step.real)):
                    if complex(x, step.imag) in seen:
                        print(abs(x) + abs(step.imag))
                        break
                    else:
                        seen.add(complex(x, step.imag))
                else:
                    continue
                break
            else:
                for x in get_range(int(previous_step.imag), int(step.imag)):
                    if complex(step.real, x) in seen:
                        print(abs(x) + abs(step.real))
                        break
                    else:
                        seen.add(complex(step.real, x))
                else:
                    continue
                break
