import argparse

from pathlib import Path
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

def mix_prune(secret: int, temp: int) -> int:
    secret = secret ^ temp
    return secret % 16777216

def pseudorandom(secret: int, idx: int) -> int:
    if secret in cache:
        last = cache[secret] % 10
        changes[idx].append((last - changes[idx][-1][1], last))
        return cache[secret]
    init_secret = secret
    secret = mix_prune(secret, secret * 64)
    secret = mix_prune(secret, secret // 32)
    secret = mix_prune(secret, secret * 2048)
    cache[init_secret] = secret
    last = secret % 10
    changes[idx].append((last - changes[idx][-1][1], last))
    return secret

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.readlines()]
    cache = {}
    changes = {i: [(None, x % 10)] for i, x in enumerate(data)}
    for _ in range(2000):
        data = [pseudorandom(secret, i) for i, secret in enumerate(data)]
    if args.part == 1:
        print(sum(data))
    else:
        prices = {}
        for change in changes.values():
            seen = {}
            for i in range(1, len(change) - 4):
                seq = [x[0] for x in change[i: i + 4]]
                if str(seq) in seen:
                    continue
                prices[str(seq)] = prices.get(str(seq), 0) + change[i + 3][1]
                seen[str(seq)] = True
        print(max(prices.values()))
    print(time() - t)
