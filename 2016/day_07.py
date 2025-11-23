import argparse
import re

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

def is_abba(raw: str) -> bool:
    for i in range(len(raw) - 3):
        if raw[i] == raw[i + 1]:
            continue
        if raw[i: i + 2] == raw[i + 2:i + 4][::-1]:
            return True
    return False

def get_abas(raw:str) -> list:
    abas = []
    for i in range(len(raw) - 2):
        if raw[i] == raw[i + 1]:
            continue
        if raw[i] == raw[i + 2]:
            abas.append(raw[i:i + 3])
    return abas

def has_bab(aba: str, raw: str) -> bool:
    return aba[1] + aba[:2] in raw

def supports_tls(raw: str) -> bool:
    matches = re.findall(r"\]?(\w+)\[?", raw)
    for match in matches[1::2]:
        if is_abba(match):
            return False
    for match in matches[::2]:
        if is_abba(match):
            return True
    return False

def supports_ssl(raw: str) -> bool:
    matches = re.findall(r"\]?(\w+)\[?", raw)
    for match in matches[::2]:
        abas = get_abas(match)
        for aba in abas:
            for squarred_match in matches[1::2]:
                if has_bab(aba, squarred_match):
                    return True
    return False

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    if args.part == 1:
        print(sum([supports_tls(raw) for raw in data]))
    else:
        print(sum([supports_ssl(raw) for raw in data]))
