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

REGISTER = {i: 0 for i in range(6)}

def run(*, is_part_one: bool) -> int:
    seen = set()
    prev_reg_5 = 0
    while True:
        REGISTER[4] = REGISTER[5] | 65536
        REGISTER[5] = 13284195
        while True:
            REGISTER[3] = REGISTER[4] & 255
            REGISTER[5] += REGISTER[3]
            REGISTER[5] &= 16777215
            REGISTER[5] *= 65899
            REGISTER[5] &= 16777215
            if REGISTER[4] < 256:
                break
            REGISTER[3] = 0
            while ((REGISTER[3] + 1) * 256) <= REGISTER[4]:
                REGISTER[3] += 1
            REGISTER[4] = REGISTER[3]
        if is_part_one:
            return REGISTER[5]
        if REGISTER[5] in seen:
            return prev_reg_5
        prev_reg_5 = REGISTER[5]
        seen.add(prev_reg_5)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    print(run(is_part_one=args.part == 1))
    print(time() - t)
