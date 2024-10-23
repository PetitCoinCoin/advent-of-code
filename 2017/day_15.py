import argparse

from time import time

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

START_A = 634
START_B = 301
FACTOR_A = 16807
FACTOR_B = 48271
DIV = 2147483647

def generate(start_a: int, start_b: int, *, is_part_two: bool = False) -> tuple:
    from_a = (start_a * FACTOR_A) % DIV
    from_b = (start_b * FACTOR_B) % DIV
    if not is_part_two:
        return from_a, from_b
    while from_a % 4:
        from_a = (from_a * FACTOR_A) % DIV
    while from_b % 8:
        from_b = (from_b * FACTOR_B) % DIV
    return from_a, from_b

def to_short_bin(val: int) -> str:
    return bin(val)[2:].zfill(32)[-16:]

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    start_a = START_A
    start_b = START_B
    loop = 40 if args.part == 1 else 5
    count = 0
    for i in range(loop * 10**6):
        start_a, start_b = generate(start_a, start_b, is_part_two=args.part == 2)
        if to_short_bin(start_a) == to_short_bin(start_b):
            count += 1
    print(count)
    print(time()-t)
