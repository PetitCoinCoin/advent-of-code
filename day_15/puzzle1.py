from pathlib import Path

def hash_sequence(sequence: str) -> int:
    result = 0
    for char in sequence:
        result += ord(char)
        result *= 17
        result %= 256
    return result

if __name__ == "__main__":
    with Path("day_15/input.txt").open("r") as file:
        data = file.read().split(",")
    print(sum([hash_sequence(sequence) for sequence in data]))
