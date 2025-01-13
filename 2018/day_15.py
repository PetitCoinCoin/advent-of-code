from __future__ import annotations

import argparse

from copy import deepcopy
from heapq import heapify, heappop, heappush
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

class Battle:
    def __init__(self, plan: dict, units: list, goblins: int, elves: int, part: int) -> None:
        self.plan = plan
        self.units = units
        self.goblins = goblins
        self.elves = elves
        self.round = 0
        self.is_part_two = part == 2
        self.elf_power = 3
    
    def target_range(self, unit: Unit, *, to_attack: bool = False) -> list:
        targets = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            target = self.plan.get((unit.x + dx, unit.y + dy))
            if isinstance(target, Unit) and target.type != unit.type and target.is_alive:
                heappush(targets, target)
        if targets and to_attack:
            min_hp = min(target.hp for target in targets)
            targets = [target for target in targets if target.hp == min_hp]
            heapify(targets)
        return targets

    def path_to_closest(self, unit: Unit) -> tuple:
        paths = []
        seen = set()
        heappush(paths, (0, (unit.y, unit.x), None))
        while paths:
            dist, step, delta = heappop(paths)
            y, x = step
            target = self.plan.get((x, y))
            if isinstance(target, Unit) and target != unit:
                if target.type != unit.type:
                    return delta
                continue
            seen.add(step)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if self.plan.get((x + dx, y + dy), "#") != "#" and (y + dy, x + dx) not in seen:
                    seen.add((y + dy, x + dx))
                    heappush(paths, (dist + 1, (y + dy, x + dx), delta if delta is not None else (dy, dx)))
        return 0, 0

    def fight(self) -> bool:
        """return True if battle is still ongoing."""
        next_units = []
        while self.units:
            unit: Unit = heappop(self.units)
            if not unit.is_alive:
                continue
            unit.move()
            should_go_on = unit.attack()
            if not should_go_on:
                return False
            if not self.goblins or not self.elves:
                heappush(next_units, unit)
                if not self.units:
                    self.round += 1
                else:
                    for remaining in self.units:
                        heappush(next_units, remaining)
                self.units = next_units
                return False
            heappush(next_units, unit)
        self.round += 1
        self.units = next_units
        return True

class Unit:
    def __init__(self, battle: Battle, utype: str, x: int, y: int) -> None:
        self.battle = battle
        self.type = utype
        self.x = x
        self.y = y
        self.hp = 200
        self.is_alive = True

    def __gt__(self, other: Unit) -> bool:
        if self.y > other.y:
            return True
        if self.y == other.y:
            return self.x > other.x
        return False

    def __repr__(self):
        return f"{self.type} ({self.x}, {self.y}) - HP {self.hp}"

    def move(self) -> None:
        if self.battle.target_range(self):
            return
        dy, dx = self.battle.path_to_closest(self)
        self.battle.plan[(self.x, self.y)] = "."
        self.x += dx
        self.y += dy
        self.battle.plan[(self.x, self.y)] = self

    def attack(self) -> bool:
        """returns True if battle is still ongoing (only relevant for part 2)"""
        targets = self.battle.target_range(self, to_attack = True)
        if not targets:
            return True
        target = heappop(targets)
        if self.type == target.type:
            print("WTF, it's your friend")
        if not target.is_alive:
            print("WTF, it's already dead")
        target.hp -= 3 if self.type == "G" else self.battle.elf_power
        if target.hp <= 0:
            target.die()
            if self.battle.is_part_two and target.type == "E":
                return False
        return True


    def die(self) -> None:
        self.battle.plan[(self.x, self.y)] = "."
        if self.type == "G":
            self.battle.goblins -= 1
        else:
            self.battle.elves -= 1
        self.is_alive = False

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    units = []
    battle = Battle(
        plan=data,
        units=units,
        goblins=0,
        elves=0,
        part=args.part,
    )
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        for y, raw in enumerate(file.read().split("\n")):
            for x, char in enumerate(raw):
                if char in "GE":
                    unit = Unit(
                        battle=battle,
                        utype=char,
                        x=x,
                        y=y,
                    )
                    data[(x, y)] = unit
                    heappush(units, unit)
                    if char == "G":
                        battle.goblins += 1
                    else:
                        battle.elves += 1
                elif char == ".":
                    data[(x, y)] = char
    if args.part == 1:
        keep_fighting = True
        while keep_fighting:
            keep_fighting = battle.fight()
        print(battle.round * sum(unit.hp for unit in battle.units if unit.is_alive))
    else:
        power = 3
        current_battle = deepcopy(battle)
        while current_battle.goblins:
            current_battle = deepcopy(battle)
            power += 1
            current_battle.elf_power = power
            keep_fighting = True
            while keep_fighting:
                keep_fighting = current_battle.fight()
        print(current_battle.round * sum(unit.hp for unit in current_battle.units if unit.is_alive))
    print(time() - t)
