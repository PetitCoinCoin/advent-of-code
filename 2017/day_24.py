import argparse

from dataclasses import dataclass
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

@dataclass
class Bridge:
    components: list[tuple[int, int]]
    strength: int
    length: int
    current_out: int

    def __gt__(self, other_bridge):
        return self.length > other_bridge.length

def get_next_possible(components: dict, bridge: Bridge) -> list:
    return [
        key
        for key in components.keys()
        if bridge.current_out in key and key not in bridge.components
    ]

def build_bridge(components: dict, bridge: Bridge, *, is_part_two: bool=False) -> Bridge:
    next_possible = get_next_possible(components, bridge)
    if next_possible:
        max_bridge = bridge
        for next_component in next_possible:
            new_bridge = Bridge(
                components=bridge.components + [next_component],
                strength=bridge.strength + components[next_component],
                length=bridge.length + 1,
                current_out=next_component[0] if next_component[0] != bridge.current_out else next_component[1],
            )
            new_built = build_bridge(components, new_bridge, is_part_two=is_part_two)
            if is_part_two:
                if new_built.length > max_bridge.length or (new_built.length == max_bridge.length and new_built.strength > max_bridge.strength):
                    max_bridge = new_built
            else:
                if new_built.strength > max_bridge.strength:
                    max_bridge = new_built
        return max_bridge
    else:
        return bridge

if __name__ == "__main__":
    args = _parse_args()
    data = dict()
    start_components = []
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        while line := file.readline():
            elements = tuple(int(x) for x in line.strip().split("/"))
            data[elements] = sum(elements)
            if 0 in elements:
                start_components.append(elements)
    if args.part == 1:
        print(max(
            build_bridge(
                data,
                Bridge(
                    components=[component],
                    strength=data[component],
                    length=1,
                    current_out=data[component]
                ),
            ).strength
            for component in start_components
        ))
    else:
        print(max(
            build_bridge(
                data,
                Bridge(
                    components=[component],
                    strength=data[component],
                    length=1,
                    current_out=data[component]
                ),
                is_part_two=True,
            )
            for component in start_components
        ).strength)
