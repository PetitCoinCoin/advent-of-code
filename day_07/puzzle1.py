from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

CARDS_RANKING = {
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

def annotate_hand(raw_hand: str) -> Hand:
    value = raw_hand.split(" ")[0]
    bid = int(raw_hand.split(" ")[1])
    mapped_value = ""
    for item in value:
        mapped_value += CARDS_RANKING[item]
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
    
if __name__ == "__main__":
    with Path("day_07/input.txt").open("r") as file:
        data = []
        while line := file.readline():
            data.append(annotate_hand(line))
        data.sort()
        result = 0
        for i in range(len(data)):
            result += (i + 1) * data[i].bid
        print(result)
