from pathlib import Path

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
                seeds = [int(value) for value in line.split(": ")[-1].split(" ")]
            elif line.startswith("seed-to-soil"):
                current_map = seed_to_soil
            elif line.startswith("soil-to-fertilizer"):
                current_map = soil_to_fertilizer
            elif line.startswith("fertilizer-to-water"):
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

def map_item(map_to: dict, item: int) -> int:
    try:
        source = max([x for x in map_to.keys() if x <= item])
    except ValueError:
        return item
    delta = item - source
    destination, count = map_to[source]
    if delta >= count:
        return item
    return destination + delta

if __name__ == "__main__":
    seeds, seed_to_soil,  soil_to_fertilizer, fertilizer_to_water, water_to_light, \
    light_to_temperature, temperature_to_humidity, humidity_to_location = get_input()

    locations = [
        map_item(
            humidity_to_location,
            map_item(
                temperature_to_humidity,
                map_item(
                    light_to_temperature,
                    map_item(
                        water_to_light,
                        map_item(
                            fertilizer_to_water,
                            map_item(
                                soil_to_fertilizer,
                                map_item(
                                    seed_to_soil,
                                    seed,
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )
        for seed in seeds
    ]
    print(min(locations))
