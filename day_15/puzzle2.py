from dataclasses import dataclass
from pathlib import Path

@dataclass
class Lens:
    label: str
    focal: int

def hash_sequence(sequence: str) -> int:
    result = 0
    for char in sequence:
        result += ord(char)
        result *= 17
        result %= 256
    return result

def handle_sequence(sequence: str, boxes: dict) -> None:
    add_split = sequence.split("=")
    add_lens = True
    if len(add_split) > 1:
        lens = Lens(label=add_split[0], focal=int(add_split[1]))
        box = hash_sequence(lens.label)
    else:
        add_lens = False
        label = sequence[:-1]
        box = hash_sequence(label)
    if add_lens:
        for i, v in enumerate(boxes[box]):
            if v.label == lens.label:
                boxes[box][i] = lens
                break
        else:
            boxes[box].append(lens)
    else:
        boxes[box] = [l for l in boxes[box] if l.label != label]

def focusing_power(lenses: list, box: int) -> int:
    result = 0
    for i, v in enumerate(lenses):
        result += (box + 1) * (i + 1) * v.focal
    return result

if __name__ == "__main__":
    with Path("day_15/input.txt").open("r") as file:
        data = file.read().split(",")
    boxes = {}
    for i in range(256):
        boxes[i] = []
    for sequence in data:
        handle_sequence(sequence, boxes)
    power = 0
    for k, v in boxes.items():
        power += focusing_power(v, k)
    print(power)
