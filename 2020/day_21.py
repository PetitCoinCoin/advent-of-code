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

def parse_input(raw: str) -> None:
    for line in raw.split("\n"):
        ingredients, allergens = tuple(line.split(" ("))
        set_ingredients = set(ingredients.split(" "))
        for ingredient in set_ingredients:
            all_ingredients[ingredient] = all_ingredients.get(ingredient, 0) + 1
        for allergen in allergens[9:-1].split(", "):
            if allergen in data:
                data[allergen] = data[allergen].intersection(set_ingredients)
            else:
                data[allergen] = set_ingredients
    

def map_allergens() -> None:
    to_remove = {next(iter(ingredients)) for ingredients in data.values() if len(ingredients) == 1}
    while len(to_remove) != len(data.keys()):
        for allergen, ingredients in data.items():
            if len(ingredients) > 1:
                data[allergen] = ingredients - to_remove
                if len(data[allergen]) == 1:
                    to_remove |= data[allergen]

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = dict()
    all_ingredients = dict()
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        parse_input(file.read().strip())
    ingredients_probably_with_allergen = set()
    for ingredients in data.values():
        ingredients_probably_with_allergen |= ingredients
    if args.part == 1:
        print(sum(count for ingredient, count in all_ingredients.items() if ingredient not in ingredients_probably_with_allergen))
    else:
        map_allergens()
        data = dict(sorted(data.items()))
        print(",".join([next(iter(ingredient)) for ingredient in data.values()]))
    print(time() - t)
