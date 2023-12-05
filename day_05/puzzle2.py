from dataclasses import dataclass
from pathlib import Path

@dataclass
class Info():
    start: int
    count: int

def get_input() -> tuple:
    seed_to_soil = {}
    soil_to_fertilizer = {}
    fertilizer_to_water = {}
    water_to_light = {}
    light_to_temperature = {}
    temperature_to_humidity = {}
    humidity_to_location = {}
    with Path("day_05/input.txt").open("r") as file:
        current_map = None
        while line := file.readline():
            # would be better with a switch, but I'm in 3.9
            if line == "\n":
                continue
            elif line.startswith("seeds:"):
                raw_seeds = [int(value) for value in line.split(": ")[-1].split(" ")]
                seeds = []
                while raw_seeds:
                    start = raw_seeds.pop(0)
                    nb = raw_seeds.pop(0)
                    seeds.append(Info(start, nb))
            elif line.startswith("seed-to-soil"):
                current_map = seed_to_soil
            elif line.startswith("soil-to-fertilizer"):
                current_map = soil_to_fertilizer
            elif line.startswith("fertilizer-to-water"):
                # break
                current_map = fertilizer_to_water
            elif line.startswith("water-to-light"):
                current_map = water_to_light
            elif line.startswith("light-to-temperature"):
                current_map = light_to_temperature
            elif line.startswith("temperature-to-humidity"):
                current_map = temperature_to_humidity
            elif line.startswith("humidity-to-location"):
                current_map = humidity_to_location
            else:
                line_values = [int(value.strip()) for value in line.split(" ")]
                count = line_values[-1]
                init_source = line_values[1]
                init_dest = line_values[0]
                current_map[init_source] = (init_dest, count)
    return (
        seeds,
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
    )

def split_items(map_to: dict, items: list) -> list:
    splitted = []
    for item in items:
        while item.count > 0:
            try:
                source = max([x for x in map_to.keys() if x <= item.start])
                delta = item.start - source
                _, count = map_to[source]
                if delta >= count:
                    splitted.append(item)
                    break
                splitted.append(Info(item.start, min(item.count, count - delta)))
                item.start += min(item.count, count - delta)
                item.count -= min(item.count, count - delta)
            except ValueError:
                try:
                    next_source = min([x for x in map_to.keys() if x > item.start])
                except ValueError:
                    splitted.append(item)
                    break
                else:
                    delta = next_source - item.start
                    if item.start + item.count - 1 < next_source:
                        splitted.append(item)
                        break
                    splitted.append(Info(item.start, delta))
                    item.start += delta
                    item.count -= delta
    return splitted

def map_item(map_to: dict, item: Info) -> Info:
    try:
        source = max([x for x in map_to.keys() if x <= item.start])
    except ValueError:
        return item
    delta = item.start - source
    destination, count = map_to[source]
    if delta < count:
        item.start = destination + delta
    return item

if __name__ == "__main__":
    seeds, seed_to_soil,  soil_to_fertilizer, fertilizer_to_water, water_to_light, \
    light_to_temperature, temperature_to_humidity, humidity_to_location = get_input()

    locations = [
        map_item(humidity_to_location, humidity)
        for humidity in split_items(
            humidity_to_location,
            [
                map_item(temperature_to_humidity, temp)
                for temp in split_items(
                    temperature_to_humidity,
                    [
                        map_item(light_to_temperature, light)
                        for light in split_items(
                            light_to_temperature,
                            [
                                map_item(water_to_light, water)
                                for water in split_items(
                                    water_to_light,
                                    [
                                        map_item(fertilizer_to_water, fertilizer)
                                        for fertilizer in split_items(
                                            fertilizer_to_water,
                                            [
                                                map_item(soil_to_fertilizer, soil)
                                                for soil in split_items(
                                                    soil_to_fertilizer,
                                                    [
                                                        map_item(seed_to_soil, seed)
                                                        for seed in split_items(seed_to_soil, seeds)
                                                    ],
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
    ]
    print(min([loc.start for loc in locations]))
