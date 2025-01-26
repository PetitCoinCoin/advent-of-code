from __future__ import annotations
import argparse
import re

from collections import Counter
from dataclasses import dataclass
from heapq import heappop, heappush
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

@dataclass
class Group:
    army: str
    id: str
    units: int
    hp: int
    weak_to: list[str]
    immune_to: list[str]
    attack_type: str
    attack_damage: int
    initiative: int
    targets: list[Group]

    def __gt__(self, other: Group) -> bool:
        if self.units * self.attack_damage < other.units * other.attack_damage:
            return True
        if self.units * self.attack_damage == other.units * other.attack_damage:
            return self.initiative < other.initiative
        return False

    def power(self) -> int:
        return self.units * self.attack_damage

def create_group(line: str, army: str, idx: int) -> Group:
    pattern = r"(\d+) units each with (\d+) hit points (\([\w,;\s]*\))?\s?with an attack that does (\d+) (\w+) damage at initiative (\d+)"
    units, hp, raw, damage, atype, initiative = re.findall(pattern, line)[0]
    weak_to = []
    immune_to = []
    if raw:
        for sub in raw[1:-1].split("; "):
            if sub.startswith("weak to"):
                weak_to = sub[8:].split(", ")
            elif sub.startswith("immune to"):
                immune_to = sub[10:].split(", ")
    return Group(
        army=army,
        id=f"{army}_{str(idx)}",
        units=int(units),
        hp=int(hp),
        weak_to=weak_to,
        immune_to=immune_to,
        attack_type=atype,
        attack_damage=int(damage),
        initiative=int(initiative),
        targets=[],
    )

def parse_input(raw: str) -> None:
    immune, infection = raw.strip().split("\n\n")
    for i, line in enumerate(immune.split("\n")[1:]):
        group = create_group(line, "immune", i)
        heappush(ready_to_target, group)
        data["infection"].append(group)
    for i, line in enumerate(infection.split("\n")[1:]):
        group = create_group(line, "infection", i)
        heappush(ready_to_target, group)
        data["immune"].append(group)

def get_targets() -> None:
    seen = set()
    while ready_to_target:
        group = heappop(ready_to_target)
        group.targets = []
        if not group.units:
            continue
        targets = []
        for other in data[group.army]:
            if not other.units or group.attack_type in other.immune_to:
                continue
            if other.id in seen:
                continue
            mul = -1 
            if group.attack_type in other.weak_to:
                mul = -2
            heappush(targets, (mul * group.power(), other))
        if targets:
            _, target = heappop(targets)
            group.targets.append(target)
            seen.add(target.id)
        heappush(ready_to_attack, (-group.initiative, group))

def launch_attack() -> int:
    damages = 0
    while ready_to_attack:
        _, group = heappop(ready_to_attack)
        if not group.units:
            continue
        if group.targets:
            target = group.targets.pop()
            mul = 1
            if group.attack_type in target.weak_to:
                mul = 2
            hits = (mul * group.power()) // target.hp
            target.units = max(0, target.units - hits)
            damages += hits
        heappush(ready_to_target, group)
    return damages

def boost_immune(group: Group) -> None:
    if group.army == "immune":
        group.attack_damage += 35  # found boost value manually
    heappush(ready_to_target, group)

def fight_is_over(damages: int) -> int:
    if len(Counter([
        group.army
        for group in ready_to_target
        if group.units
    ])) < 2:
        return 1
    if not damages:
        # fight is stuck
        return 0
    return -1

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    ready_to_target: list[Group] = []
    ready_to_attack: list[Group] = []
    data: dict[str, list[Group]] = {
        "immune": [],  # data["immune"] contains "infection" groups
        "infection": [],
    }
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        parse_input(file.read())
    damages = 1
    if args.part == 1:
        while fight_is_over(damages) < 0:
            get_targets()
            damages = launch_attack()
    else:
        winner = "infection"
        # boost has been chosen to go through loop only once!
        while winner != "immune":
            ready_to_target = []
            for group in data["infection"] + data["immune"]:
                boost_immune(group)
            while fight_is_over(damages) < 0:
                get_targets()
                damages = launch_attack()
            if damages:
                winner = next(group.army for group in ready_to_target if group.units)
            else:
                winner = "stuck"
    print(sum(group.units for group in ready_to_target))
    print(time() - t)
