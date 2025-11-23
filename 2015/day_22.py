import argparse

from copy import deepcopy
from pathlib import Path

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

SPELLS_DATA = {
    (53, "Missile"): {"damage": 4},
    (73, "Drain"): {"damage": 2, "heal": 2},
    (113, "Shield"): {"armor": 7, "timer": 6},
    (173, "Poison"): {"damage": 3, "timer": 6},
    (229, "Recharge"): {"mana": 101, "timer": 5},
}

def parse_input(raw: str) -> tuple:
    hp, damage = raw.split("\n")
    return int(hp.split(": ")[-1]), int(damage.split(":")[-1])

class Spell:
    def __init__(self, spell: tuple):
        cost, name = spell
        self.name = name
        self.cost = cost
        self.damage = SPELLS_DATA[spell].get("damage", 0)
        self.armor = SPELLS_DATA[spell].get("armor", 0)
        self.mana = SPELLS_DATA[spell].get("mana", 0)
        self.heal = SPELLS_DATA[spell].get("heal", 0)
        self.timer = SPELLS_DATA[spell].get("timer", None)

    def __repr__(self) -> str:
        return f"{self.name} - {self.cost} - {self.timer}"

    def effects(self) -> None:
        if self.timer:
            self.timer -= 1

class Game:
    def __init__(self) -> None:
        self.hits = 50
        self.mana = 500
        self.boss_hits = HP
        self.boss_damage = DAMAGE
        self.active_spells = set()
        self.total = 0
        self.result = None

    def __repr__(self) -> str:
        return f"total: {self.total}, hits: {self.hits}, mana: {self.mana}, boss: {self.boss_hits}"

    def check_end(self) -> None:
        # Don't check mana here. You can win with 0 mana (see Poison)
        if self.hits <= 0:
            self.result = 0
        elif self.boss_hits <= 0:
            self.result = self.total

    def activate_spells(self, boss_turn: bool = False) -> None:
        for spell in self.active_spells:
            self.boss_hits -= spell.damage
            self.hits += spell.heal
            self.mana += spell.mana
            if boss_turn:
                # Can consider shield as heal on boss' turn
                self.hits += spell.armor
            spell.effects()
        self.active_spells = {spell for spell in self.active_spells if spell.timer}
        self.check_end()

    def my_turn(self, spell_key: tuple) -> None:
        self.activate_spells()
        if self.result is not None:
            return
        spell = Spell(spell_key)
        if len({s for s in self.active_spells if s.name == spell.name}):
            # Spell already active
            self.result = 0
            return
        self.mana -= spell.cost
        self.total += spell.cost
        if self.mana < 0:
            # Can't afford spell
            self.result = 0
            return
        if spell.timer is None:
            self.boss_hits -= spell.damage
            self.hits += spell.heal
        else:
            self.active_spells.add(spell)
        self.check_end()

    def boss_turn(self) -> None:
        self.activate_spells(boss_turn=True)
        if self.result is not None:
            return
        self.hits -= self.boss_damage
        self.check_end()

    def run(self, spell_key: tuple, min_mana: int, hard_mode: bool) -> None:
        """Handling my turn and boss' turn together to avoid keeping track of current player."""

        if self.total > min_mana:
            self.result = 0
            return
        if hard_mode:
            self.hits -= 1
            if self.hits <= 0:
                self.result = 0
                return
        self.my_turn(spell_key)
        if self.result is not None:
            return
        self.boss_turn()

def play(game: Game, min_mana: int, hard_mode: bool) -> int:
    for spell in SPELLS_DATA.keys():
        new_game = deepcopy(game)
        new_game.run(spell, min_mana, hard_mode)
        mana = new_game.result
        if mana is None:
            mana = play(new_game, min_mana, hard_mode)
        if mana and mana < min_mana:
            min_mana = mana
    return min_mana

if __name__ == "__main__":
    args = _parse_args()
    min_mana = 1000000
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}.txt").open("r") as file:
        HP, DAMAGE = parse_input(file.read().strip())
    print(play(Game(), min_mana, args.part == 2))
