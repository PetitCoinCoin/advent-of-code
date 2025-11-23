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

def make_recipe(elf_1: int, elf_2: int) -> tuple:
    recipe_1 = data[elf_1]
    recipe_2 = data[elf_2]
    for digit in str(recipe_1 + recipe_2):
        data.append(int(digit))
    return (elf_1 + 1 + recipe_1) % len(data), (elf_2 + 1 + recipe_2) % len(data)

def is_valid() -> int:
    if data[-len(recipe_list):] == recipe_list:
        return len(data) - len(recipe_list)
    if data[-len(recipe_list) - 1: -1] == recipe_list:
        return len(data) - len(recipe_list) - 1
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        recipes_count = int(file.read())
    data = [3, 7]
    elf_1, elf_2 = 0, 1
    if args.part == 1:
        while len(data) < recipes_count + 10:
            elf_1, elf_2 = make_recipe(elf_1, elf_2)
        print("".join([str(x) for x in data[recipes_count: recipes_count + 10]]))
    else:
        recipe_list = [int(x) for x in str(recipes_count)]
        while not is_valid():
            elf_1, elf_2 = make_recipe(elf_1, elf_2)
        print(is_valid())
    print(time() - t)
