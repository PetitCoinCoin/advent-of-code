from pathlib import Path

def clean_data(card: str) -> int:
    """Returns count of winning numbers per card."""

    without_id = card.split(":")[-1]
    winning = [
        x.strip()
        for x in without_id.split(" | ")[0].strip().split(" ")
        if x != ""
    ]
    played_and_win = [
        x.strip()
        for x in without_id.split(" | ")[1].strip().split(" ")
        if x != "" and x in winning
    ]
    return len(played_and_win)

def count_copies(sub_data: list) -> int:
    count = sub_data.pop(0)
    if count > 0:
        total = 0
        for i in range(count):
            total += 1 + count_copies(sub_data[i:])
        return total
    else:
        return 0

if __name__ == "__main__":
    with Path("day_04/input.txt").open("r") as file:
        data = file.read().split("\n")
    cleaned_data = [clean_data(card) for card in data]

    total = 0
    for i in range(len(cleaned_data)):
        total += 1 + count_copies(cleaned_data[i:])
    print(total)
