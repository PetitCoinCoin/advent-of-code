import argparse

from enum import Enum
from collections import Counter
from dataclasses import dataclass, field
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

CARDS_RANKING_1 = {
    "2": "a",
    "3": "b",
    "4": "c",
    "5": "d",
    "6": "e",
    "7": "f",
    "8": "g",
    "9": "h",
    "T": "i",
    "J": "j",
    "Q": "k",
    "K": "l",
    "A": "m",
}

CARDS_RANKING_2 = {
    "J": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h",
    "9": "i",
    "T": "j",
    "Q": "k",
    "K": "l",
    "A": "m",
}

class HandType(Enum):
    FIVE = 7
    FOUR = 6
    FULL = 5
    THREE = 4
    TWO = 3
    ONE = 2
    HIGH = 1

@dataclass(order=True)
class Hand():
    sort_one: int = field(init=False, repr=False)
    sort_second: str = field(init=False, repr=False)
    value: str
    mapped_value: str
    bid: int
    htype: HandType

    def __post_init__(self):
        self.sort_one = self.htype.value
        self.sort_second = self.mapped_value

def annotate_hand_1(raw_hand: str) -> Hand:
    value = raw_hand.split(" ")[0]
    bid = int(raw_hand.split(" ")[1])
    mapped_value = ""
    for item in value:
        mapped_value += CARDS_RANKING_1[item]
    cards = Counter(value)
    max_card_count = cards.most_common(1)[0][1]
    if max_card_count == 5:
        return Hand(value, mapped_value, bid, HandType.FIVE)
    if max_card_count == 4:
        return Hand(value, mapped_value, bid, HandType.FOUR)
    if max_card_count == 3:
        if cards.most_common(2)[1][1] == 2:
            return Hand(value, mapped_value, bid, HandType.FULL)
        return Hand(value, mapped_value, bid, HandType.THREE)
    if max_card_count == 2:
        if cards.most_common(2)[1][1] == 2:
            return Hand(value, mapped_value, bid, HandType.TWO)
        return Hand(value, mapped_value, bid, HandType.ONE)
    return Hand(value, mapped_value, bid, HandType.HIGH)

def annotate_hand_2(raw_hand: str) -> Hand:
    value = raw_hand.split(" ")[0]
    bid = int(raw_hand.split(" ")[1])
    mapped_value = ""
    for item in value:
        mapped_value += CARDS_RANKING_2[item]
    if value == "JJJJJ":
        return Hand(value, mapped_value, bid, HandType.FIVE)
    cards = Counter(value)
    joker_count = cards["J"]
    if joker_count:
        max_card, _ = cards.most_common(1)[0]
        if max_card == "J":
            max_card, _ = cards.most_common(2)[1]
        cards = Counter(value.replace("J", max_card))
    max_card_count = cards.most_common(1)[0][1]
    if max_card_count == 5:
        return Hand(value, mapped_value, bid, HandType.FIVE)
    if max_card_count == 4:
        return Hand(value, mapped_value, bid, HandType.FOUR)
    if max_card_count == 3:
        if cards.most_common(2)[1][1] == 2:
            return Hand(value, mapped_value, bid, HandType.FULL)
        return Hand(value, mapped_value, bid, HandType.THREE)
    if max_card_count == 2:
        if cards.most_common(2)[1][1] == 2:
            return Hand(value, mapped_value, bid, HandType.TWO)
        return Hand(value, mapped_value, bid, HandType.ONE)
    return Hand(value, mapped_value, bid, HandType.HIGH)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = []
    func = annotate_hand_1 if args.part == 1 else annotate_hand_2
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            data.append(func(line))
    data.sort()
    result = 0
    for i in range(len(data)):
        result += (i + 1) * data[i].bid
    print(result)
    print(time() - t)

