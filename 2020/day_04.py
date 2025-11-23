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

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
OPTIONNAL_FIELDS = {"cid"}

def parse_input(raw: str) -> dict:
    raw = raw.replace("\n", " ")
    res = {}
    for pair in raw.split(" "):
        key, value = tuple(pair.split(":"))
        res[key] = value
    return res

def has_all_required(passport: dict) -> bool:
    keys = set(passport.keys())
    return not len(REQUIRED_FIELDS - keys)

def is_valid(passport: dict) -> bool:
    for key in ("byr", "iyr", "eyr"):
        if not passport[key].isdigit():
            return False
    byr = int(passport["byr"])
    if byr < 1920 or byr > 2002:
        return False
    iyr = int(passport["iyr"])
    if iyr < 2010 or iyr > 2020:
        return False
    eyr = int(passport["eyr"])
    if eyr < 2020 or eyr > 2030:
        return False

    hgt = passport["hgt"]
    if hgt[-2:] not in ("cm", "in"):
        return False
    if not hgt[:-2].isdigit():
        return False
    hgt_digit = int(hgt[:-2])
    if hgt[-2:] == "cm" and (hgt_digit < 150 or hgt_digit > 193):
        return False
    if hgt[-2:] == "in" and (hgt_digit < 59 or hgt_digit > 76):
        return False

    if not passport["hcl"].startswith("#"):
        return False
    try:
        int(passport["hcl"][1:], 16)
    except ValueError:
        return False

    if passport["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        return False
    
    if len(passport["pid"]) != 9 or not passport["pid"].isdigit():
        return False
    return True

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(raw) for raw in file.read().strip().split("\n\n")]
    data_with_required = [passport for passport in data if has_all_required(passport)]
    if args.part == 1:
        print(len(data_with_required))
    else:
        print(sum(is_valid(passport) for passport in data_with_required))
    print(time() - t)
