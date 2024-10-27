import argparse

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

def get_infected_status(status: list) -> dict:
    result = dict()
    middle = len(status) // 2
    for i in range(len(status)):
        for j in range(len(status[i])):
            result[complex(j - middle, -(i - middle))] = status[i][j]
    return result

def burst(status: dict, direction: complex, current: complex) -> tuple:
    new_infected = 0
    if status.get(current, ".") == "#":
        direction *= -1j  # turn right
        status[current] = "."
    else:
        direction *= 1j  # turn left
        status[current] = "#"
        new_infected += 1
    return status, direction, current + direction, new_infected

def burst_evolved(status: dict, direction: complex, current: complex) -> tuple:
    new_infected = 0
    if status.get(current, ".") == "#":
        direction *= -1j  # turn right
        status[current] = "F"
    elif status.get(current, ".") == "F":
        direction *= -1  # reverse
        status[current] = "."
    elif status.get(current, ".") == "W":
        status[current] = "#"
        new_infected += 1
    else:
        direction *= 1j  # turn left
        status[current] = "W"
    return status, direction, current + direction, new_infected

if __name__ == "__main__":
    args = _parse_args()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().split("\n")
    infected = get_infected_status(data)
    i = 0
    infection_burst = 0
    direction = 1j
    current = 0 + 0j
    if args.part == 1:
        while i < 10000:
            infected, direction, current, infection = burst(infected, direction, current)
            i += 1
            infection_burst += infection
        print(infection_burst)
    else:
        while i < 10000000:
            infected, direction, current, infection = burst_evolved(infected, direction, current)
            i += 1
            infection_burst += infection
        print(infection_burst)
