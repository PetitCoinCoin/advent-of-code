from pathlib import Path

def calculate_points(card: str) -> int:
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
    if played_and_win:
        return 2 ** (len(played_and_win) - 1)
    else:
        return 0

if __name__ == "__main__":
    with Path("day_04/input.txt").open("r") as file:
        data = file.read().split("\n")
    print(sum([
        calculate_points(card)
        for card in data
    ]))
