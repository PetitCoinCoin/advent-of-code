from __future__ import annotations

import re

from dataclasses import dataclass
from pathlib import Path

@dataclass
class Module:
    name: str
    type: str
    destinations: list
    state_on: bool
    signal: str
    input_signals: dict

def format_module(raw: str) -> tuple:
    groups = re.findall(r"(%|&)*(\w+)\s->\s(.+)", raw)
    name = groups[0][1]
    mod_type = name if name == 'broadcaster' else groups[0][0]
    return name, Module(
        name=name,
        type=mod_type,
        destinations=groups[0][2].split(", "),
        state_on=mod_type != "%",
        signal="-" if name== "broadcaster" else "",
        input_signals={},
    )

def populate_parents(modules: dict) -> None:
    for name, mod in modules.items():
        for dest in mod.destinations:
            if modules.get(dest):
                modules[dest].input_signals[name] = "-"

def propagate_pulse(modules: dict, name: str, pulse: str, parent: str) -> list:
    current_mod = modules[name]
    current_mod.input_signals[parent] = pulse
    if current_mod.type == "broadcaster":
        current_mod.signal = pulse
    elif current_mod.type == "%":
        if pulse == "-":
            current_mod.state_on = not current_mod.state_on
            current_mod.signal = "+" if current_mod.state_on else "-"
        else:
            current_mod.signal = ""
    else:  # &
        current_mod.signal = "-"
        for memory in current_mod.input_signals.values():
            if memory == "-":
                current_mod.signal = "+"
                break
    if not current_mod.signal:
        return []
    return [(mod, current_mod.signal, current_mod.name) for mod in current_mod.destinations]

def loop(modules: dict) -> tuple:
    destinations = [("broadcaster", "-", "button")]
    low = 1
    high = 0
    while destinations:
        name, pulse, parent = destinations.pop(0)
        for dest in propagate_pulse(modules, name, pulse, parent):
            if dest[1] == "+":
                high += 1
            else:
                low += 1
            if dest[0] not in modules.keys():
                continue
            if modules[dest[0]].type == "&":
                idx = 0
                seen = False
                for i, item in enumerate(destinations):
                    if modules[item[0]].type != "&":
                        idx = i
                        break
                    else:
                        seen = True
                if seen:
                    destinations.append(dest)
                else:
                    destinations.insert(idx, dest)
            else:
                destinations.append(dest)
    return low, high

if __name__ == "__main__":
    with Path("day_20/input.txt").open("r") as file:
        modules = {}
        while line := file.readline():
            name, module = format_module(line)
            modules[name] = module
    populate_parents(modules)
    i = 0
    low = 0
    high = 0
    while i < 1000:
        loop_low, loop_high = loop(modules)
        low += loop_low
        high += loop_high
        i += 1
    print(low * high)